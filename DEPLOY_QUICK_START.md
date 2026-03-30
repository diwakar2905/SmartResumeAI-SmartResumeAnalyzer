# Quick Start: Deploy to Render + Vercel

## 1️⃣ Backend to Render (5 minutes)

1. Push code to GitHub
2. Go to https://render.com → New Web Service
3. Connect GitHub repo
4. Fill in:
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Build Command:** `pip install -r requirements.txt`
5. Add Environment Variable:
   - `CORS_ORIGINS=https://your-vercel-app.vercel.app`
6. Click "Deploy"
7. ✅ Copy the backend URL (e.g., `https://smart-resume-analyzer-api.onrender.com`)

---

## 2️⃣ Frontend to Vercel (5 minutes)

### Setup:
1. Go to https://vercel.com → Add New → Project
2. Select your GitHub repository
3. Configure:
   - **Root Directory:** Leave blank or `frontend/` if separate
4. Click "Deploy"
5. ✅ You get your frontend URL

### update frontend API calls:
In your HTML files, find all `fetch('/analyze'` and replace with:
```javascript
fetch('https://your-render-backend.onrender.com/analyze'
```

Or create an `api-config.js`:
```javascript
export const API_URL = 'https://your-render-backend.onrender.com';
```

Then use in your fetch:
```javascript
fetch(`${API_URL}/analyze`, ...)
```

---

## 3️⃣ Final Steps

- ✅ Test: Upload a resume in the frontend
- ✅ Check: Backend processes it without CORS errors
- ✅ Share your Vercel URL!

---

## Important URLs to Remember

- **Backend API:** https://your-backend-url.onrender.com
- **API Docs:** https://your-backend-url.onrender.com/docs
- **Frontend:** https://your-vercel-frontend.vercel.app

---

## If You Get CORS Errors

1. Check backend is running on Render
2. Update `CORS_ORIGINS` environment variable
3. Restart the backend service
4. Clear browser cache and try again

---

## File Limits

- **Vercel:** 4.5MB max upload (free tier)
- **Render:** Check database limits for logs

For larger files, upgrade or use external file storage (AWS S3, etc.)
