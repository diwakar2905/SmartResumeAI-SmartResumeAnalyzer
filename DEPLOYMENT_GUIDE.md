# Smart Resume Analyzer - Deployment Guide

## Backend Deployment to Render

### Prerequisites
- Render account (https://render.com)
- GitHub repository with your code

### Step 1: Prepare Backend for Render

1. **Update Environment Variables in `render.yaml`:**
   - The `render.yaml` file is already configured
   - Update `CORS_ORIGINS` to include your Vercel frontend URL

2. **Create `.env.production`:**
   ```
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   ```

### Step 2: Connect to Render

1. Go to https://render.com/dashboard
2. Click **"New Web Service"**
3. Choose **"Deploy an existing Git repository"**
4. Select your GitHub repository
5. Fill in the following:
   - **Name:** `smart-resume-analyzer-api`
   - **Runtime:** `Python 3.11`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free (or select your preferred plan)

6. **Add Environment Variables:**
   - Click **"Advanced"** → **"Add Environment Variable"**
   - Add:
     ```
     CORS_ORIGINS=https://your-vercel-app.vercel.app
     PYTHON_VERSION=3.11.4
     ```

7. Click **"Create Web Service"**

### Step 3: Get Backend URL

- Once deployed, copy the **URL** from Render (e.g., `https://smart-resume-analyzer-api.onrender.com`)
- You'll use this in the frontend

---

## Frontend Deployment to Vercel

### Option A: Deploy as Static Site (Recommended for HTML/CSS/JS)

#### Prerequisites
- Vercel account (https://vercel.com)
- GitHub repository

#### Step 1: Prepare Frontend

1. **Create frontend folder structure:**
   ```
   frontend/
   ├── public/
   │   ├── index.html
   │   ├── about.html
   │   ├── features.html
   │   ├── contact.html
   │   └── output.html
   ├── static/
   │   └── css/
   │       └── style.css
   └── package.json
   ```

2. **Create/update `frontend/package.json`:**
   ```json
   {
     "name": "smart-resume-analyzer-frontend",
     "version": "1.0.0",
     "description": "Frontend for Smart Resume Analyzer",
     "scripts": {
       "build": "echo 'No build step needed for static site'"
     }
   }
   ```

3. **Update API calls in frontend files:**
   - In all `.html` files, replace:
     ```javascript
     fetch('/analyze')
     ```
     with:
     ```javascript
     fetch('https://your-backend-url.onrender.com/analyze')
     ```

4. **Create `frontend/vercel.json`:**
   ```json
   {
     "buildCommand": "npm run build",
     "installCommand": "npm install",
     "outputDirectory": "public"
   }
   ```

#### Step 2: Deploy to Vercel

1. Push your frontend code to GitHub (in `frontend/` folder)
2. Go to https://vercel.com/new
3. Select your GitHub repository
4. Configure project:
   - **Framework Preset:** Other
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `public`

5. Click **"Deploy"**

---

### Option B: Deploy as Next.js App (For advanced features)

#### Step 1: Create Next.js Project

```bash
npx create-next-app@latest --typescript
```

#### Step 2: Copy Templates to Next.js

Copy your HTML files to `app/` directory and convert to React components.

#### Step 3: Update API Calls

```typescript
// In your Next.js component
const response = await fetch('https://your-backend-url.onrender.com/analyze', {
  method: 'POST',
  body: formData,
});
```

#### Step 4: Deploy

```bash
git push origin main
```

Vercel will automatically deploy on push.

---

## Testing After Deployment

### Test Backend API
```bash
curl -X POST https://your-backend-url.onrender.com/analyze \
  -F "resume_file=@path/to/resume.pdf"
```

### Test Frontend
1. Visit your Vercel URL
2. Upload a resume
3. Verify the analysis completes

---

## Environment Variables Setup

### Backend (Render)
```
CORS_ORIGINS=https://your-vercel-app.vercel.app
PYTHON_VERSION=3.11.4
```

### Frontend (Vercel)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
```

---

## Important Notes

1. **CORS Configuration:**
   - The backend is configured to accept CORS requests
   - Make sure the frontend URL is in the `CORS_ORIGINS` environment variable

2. **File Uploads:**
   - Vercel has a 4.5MB file upload limit on free tier
   - For larger files, upgrade or use a different file hosting service

3. **Cold Start:**
   - Render free tier may have cold starts (first request takes 30+ seconds)
   - Upgrade to paid tier for better performance

4. **Static Files:**
   - CSS and images should be served from the frontend (Vercel)
   - API calls should go to the backend (Render)

---

## Troubleshooting

### CORS Errors
- Check that frontend URL is added to backend `CORS_ORIGINS`
- Restart the backend service

### API Calls Timing Out
- Check if Render service is running
- Render free tier may be sleeping; first request wakes it up

### File Upload Issues
- Verify file size is under 4.5MB
- Check backend logs in Render dashboard

---

## Useful Commands

**View Render Logs:**
```
Visit Render dashboard → Your service → Logs
```

**View Vercel Logs:**
```
Visit Vercel dashboard → Your project → Deployments
```

**Test API Endpoint:**
```bash
curl -X GET https://your-backend-url.onrender.com/health
```
