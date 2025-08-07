# 🚀 Deploy HackRX API to Cloud (Free Hosting)

## 🌟 **Option 1: Render.com (Recommended)**

### Steps:
1. **Create GitHub Repository**
   - Go to github.com and create a new repository
   - Upload all your code files

2. **Deploy to Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `hackrx-llm-api`
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

3. **Add Environment Variables**
   ```
   PINECONE_API_KEY=your-key-here
   PINECONE_ENVIRONMENT=us-east-1
   GEMINI_API_KEY=your-key-here
   DEBUG=false
   ```

4. **Deploy!**
   - Your API will be available at: `https://hackrx-llm-api.onrender.com`

---

## 🌟 **Option 2: Railway.app**

### Steps:
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables
6. Deploy!

---

## 🌟 **Option 3: Heroku (If you have credits)**

### Steps:
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create hackrx-llm-api`
4. Set env vars: `heroku config:set PINECONE_API_KEY=your-key`
5. Deploy: `git push heroku main`

---

## 📝 **Your Public API Endpoints After Deployment**

### Base URL: `https://your-app-name.onrender.com`

### Endpoints:
- **Health Check**: `GET /health`
- **HackRX Health**: `GET /hackrx/health`
- **Main Endpoint**: `POST /hackrx/run`
- **API Docs**: `GET /docs`

### Example Usage:
```bash
curl -X POST "https://your-app-name.onrender.com/hackrx/run" \
  -H "Authorization: Bearer cfe5d188df2d481cbc3d03128a7a93889df967f6c24be452005b2437b7f7b26a" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": ["What is the grace period?"]
  }'
```

---

## 🔧 **Files Created for Deployment**

- ✅ `Procfile` - Tells the server how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ Updated `app/main.py` - Production ready with port handling
- ✅ `requirements.txt` - Already optimized for deployment

---

## 🚨 **Important Notes**

1. **Free Tier Limits**:
   - Render: App sleeps after 15 min of inactivity
   - Railway: 500 hours/month free
   - First request may be slow (cold start)

2. **Environment Variables**:
   - Set your real API keys in the hosting platform
   - Never commit real keys to GitHub

3. **URL for Submission**:
   - Give them: `https://your-app-name.onrender.com/hackrx/run`
   - Include the Bearer token for authentication

---

## ⚡ **Quick Start (Render.com)**

1. Push code to GitHub
2. Go to render.com → New Web Service
3. Connect GitHub repo
4. Use start command: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
5. Add your API keys as environment variables
6. Deploy!

**Your API will be live at**: `https://your-app-name.onrender.com/hackrx/run`

🎉 **Ready for HackRX submission!**
