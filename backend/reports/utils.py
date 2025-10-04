"""
Utility functions for reporter identification and session management.
"""
import hashlib
import uuid
from django.utils import timezone
from datetime import timedelta

def generate_reporter_id(request):
    """
    Generate a unique reporter ID based on request characteristics.
    This creates a pseudo-anonymous identifier for users without authentication.
    """
    # Get various request characteristics
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    accept_encoding = request.META.get('HTTP_ACCEPT_ENCODING', '')
    
    # Get IP address (be careful with privacy)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    
    # Create a fingerprint from browser characteristics
    fingerprint_data = f"{user_agent}|{accept_language}|{accept_encoding}"
    fingerprint_hash = hashlib.md5(fingerprint_data.encode()).hexdigest()[:8]
    
    # Create reporter ID
    reporter_id = f"reporter_{fingerprint_hash}"
    
    return reporter_id

def get_or_create_session_reporter(request):
    """
    Get or create a session-based reporter ID.
    This stores the reporter ID in the session for consistency.
    """
    session_key = 'reporter_id'
    
    if session_key not in request.session:
        # Generate new reporter ID
        reporter_id = generate_reporter_id(request)
        request.session[session_key] = reporter_id
        request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
    else:
        reporter_id = request.session[session_key]
    
    return reporter_id

def get_anonymous_reporter_id():
    """
    Generate a completely anonymous reporter ID.
    Use this when you want to allow completely anonymous reporting.
    """
    return f"anonymous_{uuid.uuid4().hex[:8]}"

def validate_reporter_id(reporter_id):
    """
    Validate that a reporter ID follows the expected format.
    """
    if not reporter_id:
        return False
    
    # Check if it starts with 'reporter_' or 'anonymous_'
    valid_prefixes = ['reporter_', 'anonymous_']
    return any(reporter_id.startswith(prefix) for prefix in valid_prefixes)
