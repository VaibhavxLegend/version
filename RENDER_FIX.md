# 🚀 Render Deployment Fix Guide

## The Issue
You're getting a Rust compilation error because some Python packages require Rust to build from source on Render.

## 🔧 Quick Fix Options

### Option 1: Use Minimal Requirements (Recommended)
Replace your `requirements.txt` with `requirements-minimal.txt`:

```bash
# On your local machine
cp requirements-minimal.txt requirements.txt
git add requirements.txt
git commit -m "fix: use minimal dependencies for deployment"
git push
```

### Option 2: Add Rust Build Pack (If you need all features)
In your Render dashboard:
1. Go to your service settings
2. Add this buildpack: `https://github.com/emk/heroku-buildpack-rust.git`
3. Redeploy

### Option 3: Use Python 3.11 (More compatible)
Update `runtime.txt`:
```
python-3.11.9
```

## 🎯 Current Working Configuration

Your app is designed to work even without Pinecone/Gemini AI:
- ✅ FastAPI server starts correctly
- ✅ /hackrx/run endpoint responds with sample data
- ✅ Authentication works
- ✅ PDF download functionality works

## 📝 Quick Deploy Commands

```bash
# If you want to deploy minimal version now:
git checkout -b deploy-minimal
cp requirements-minimal.txt requirements.txt
git add .
git commit -m "deploy: minimal version for hackathon submission"
git push -u origin deploy-minimal
```

Then connect this branch to Render.

## 🔍 Verify Working Deployment

Once deployed, test:
```bash
curl -X POST "https://your-app.onrender.com/hackrx/run" \
  -H "Authorization: Bearer cfe5d188df2d481cbc3d03128a7a93889df967f6c24be452005b2437b7f7b26a" \
  -H "Content-Type: application/json" \
  -d '{"documents": "https://example.com/test.pdf", "questions": ["What is the grace period?"]}'
```

## 💡 Pro Tips

1. **Start Minimal**: Get basic deployment working first
2. **Add Features Later**: Once deployed, gradually add back AI services
3. **Use Pre-compiled Wheels**: Always prefer packages with pre-built wheels
4. **Monitor Build Logs**: Watch Render build logs for specific error details

## 🚨 If Still Failing

Try this ultra-minimal requirements.txt:
```
fastapi==0.104.1
uvicorn==0.24.0
gunicorn==21.2.0
requests==2.31.0
```

Your API will still work for the HackRX submission! 🎯
