# 🚀 Deployment Guide for The Greeters Ministry App

## Quick Start - Railway (Recommended)

### Step 1: Prepare Your Code
1. **Push to GitHub**: Make sure your code is in a GitHub repository
2. **Environment Variables**: You'll need to set these in Railway:
   - `FLASK_SECRET_KEY`: A random secret key (generate one at https://randomkeygen.com/)
   - `DATABASE_URL`: Railway will provide this automatically

### Step 2: Deploy on Railway
1. **Go to**: https://railway.app
2. **Sign up** with your GitHub account
3. **Click "New Project"** → **"Deploy from GitHub repo"**
4. **Select your repository**
5. **Railway will automatically detect** it's a Python app
6. **Add Environment Variables**:
   - `FLASK_SECRET_KEY`: `your-secret-key-here`
7. **Click "Deploy"**
8. **Wait 2-3 minutes** for deployment
9. **Your app will be live** at a URL like `https://your-app-name.railway.app`

### Step 3: Set Up Database
1. **Go to your Railway project dashboard**
2. **Click "Add Service"** → **"Database"** → **"PostgreSQL"**
3. **Railway will automatically set** the `DATABASE_URL` environment variable
4. **Redeploy your app** (Railway will do this automatically)

### Step 4: Create Admin User
1. **Visit your live app URL**
2. **Create your first admin user** through the normal signup process
3. **You're ready to go!**

---

## Alternative: Render

### Step 1: Prepare Your Code
Same as Railway - push to GitHub

### Step 2: Deploy on Render
1. **Go to**: https://render.com
2. **Sign up** with GitHub
3. **Click "New"** → **"Web Service"**
4. **Connect your GitHub repository**
5. **Configure**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: `Python 3`
6. **Add Environment Variables**:
   - `FLASK_SECRET_KEY`: `your-secret-key-here`
7. **Click "Create Web Service"**

### Step 3: Add Database
1. **In Render dashboard**, click **"New"** → **"PostgreSQL"**
2. **Copy the database URL**
3. **Go back to your web service**
4. **Add environment variable**: `DATABASE_URL` = your database URL
5. **Redeploy**

---

## Environment Variables Explained

| Variable | Purpose | Example |
|----------|---------|---------|
| `FLASK_SECRET_KEY` | Encrypts sessions and cookies | `your-random-secret-key-123` |
| `DATABASE_URL` | Database connection string | `postgresql://user:pass@host:port/db` |

---

## Important Notes

### 🔒 Security
- **Never commit** your `.env` file to GitHub
- **Use strong secret keys** in production
- **The app will automatically use PostgreSQL** in production (better than SQLite)

### 📊 Database
- **SQLite** is used locally for development
- **PostgreSQL** is used in production (more reliable)
- **Your data will persist** on the cloud platform

### 🔄 Updates
- **Push to GitHub** to automatically redeploy
- **Most platforms auto-deploy** when you push changes
- **Database changes** require a new deployment

---

## Troubleshooting

### App Won't Start
- Check that all environment variables are set
- Look at the deployment logs in your platform's dashboard
- Make sure `gunicorn` is in requirements.txt

### Database Issues
- Ensure `DATABASE_URL` is set correctly
- Check that PostgreSQL service is running
- Try redeploying the app

### Can't Access Admin
- Make sure you've created an admin user
- Check that the database is properly initialized

---

## Cost Comparison

| Platform | Free Tier | Paid Plans | Best For |
|----------|-----------|------------|----------|
| **Railway** | ✅ Yes | $5/month | Beginners |
| **Render** | ✅ Yes | $7/month | Reliability |
| **Heroku** | ❌ No | $5-7/month | Advanced features |
| **DigitalOcean** | ❌ No | $5/month | More control |

---

## Need Help?

1. **Check the logs** in your platform's dashboard
2. **Verify environment variables** are set correctly
3. **Make sure your code is pushed** to GitHub
4. **Try redeploying** if something seems wrong

Your app should be live and accessible to anyone with the URL! 🎉
