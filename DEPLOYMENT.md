# Deployment Guide

## Backend Deployment to Render

### 1. Environment Variables
Set these environment variables in your Render dashboard:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=disaster-report-map.onrender.com
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority
MONGODB_NAME=disaster_response
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,http://localhost:5173,http://localhost:3000
FILE_UPLOAD_MAX_MEMORY_SIZE=10485760
DATA_UPLOAD_MAX_MEMORY_SIZE=10485760
```

### 2. Deployment Settings
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `./start.sh`
- **Python Version**: 3.10.12 (specified in runtime.txt)
- **Runtime**: python-3.10 (specified in render.yaml)

### 3. Important Notes
- **Python Version**: Must use Python 3.10.x (Django 3.2.25 only supports Python 3.6-3.10)
- **Runtime File**: The `runtime.txt` file specifies Python 3.10.12
- **Alternative**: You can also use the `Procfile` instead of `start.sh`

## Frontend Deployment

### 1. Environment Variables
Create a `.env` file in the frontend directory:

```
VITE_API_BASE_URL=https://disaster-report-map.onrender.com/api
```

### 2. Build and Deploy
```bash
cd frontend
npm install
npm run build
```

## Production URLs
- **Backend API**: `https://disaster-report-map.onrender.com/api`
- **Frontend**: Your frontend deployment URL

## Important Notes
- Make sure to update `CORS_ALLOWED_ORIGINS` with your actual frontend domain
- Update `ALLOWED_HOSTS` with your actual backend domain
- Ensure MongoDB Atlas allows connections from Render's IP ranges
- Cloudinary credentials must be valid and active

## Troubleshooting

### Python Version Issues
If you get `ModuleNotFoundError: No module named 'cgi'`:
- This happens when Django 3.2.25 runs on Python 3.11+
- Solution: Use Python 3.10.x (specified in `runtime.txt`)
- Django 3.2.25 only supports Python 3.6-3.10

### Alternative Deployment Methods
1. **Using render.yaml**: Full configuration with start.sh script
2. **Using render-simple.yaml**: Simplified configuration with inline commands
3. **Using Procfile**: Alternative start command
4. **Manual**: Set build/start commands in Render dashboard

### Deployment Options
- **Option 1**: Use `render.yaml` (recommended for full control)
- **Option 2**: Use `render-simple.yaml` (simpler, no start.sh needed)
- **Option 3**: Use `Procfile` (Heroku-style deployment)

### Common Issues
- **CORS Errors**: Update `CORS_ALLOWED_ORIGINS` with your frontend URL
- **Database Connection**: Ensure MongoDB URI is correct and accessible
- **Static Files**: Make sure `collectstatic` runs successfully
