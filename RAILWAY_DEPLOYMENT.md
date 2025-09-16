# Railway Deployment Guide

## 🚀 Quick Setup

1. **Connect your GitHub repo to Railway**
2. **Add PostgreSQL database** in Railway dashboard
3. **Set environment variables** in Railway dashboard:
   - `FLASK_SECRET_KEY` - Generate a random secret key
   - `ADMIN_USERNAME` - Your admin username (e.g., "admin")
   - `ADMIN_PASSWORD` - Your admin password (e.g., "admin123")

## 🔧 After Deployment

1. **Deploy your app** - Railway will automatically use the PostgreSQL database
2. **Initialize admin user** by visiting: `https://your-app.railway.app/init-admin`
3. **Login** with your admin credentials

## 🗄️ Database Persistence

- Railway PostgreSQL database persists between deployments
- Your data (users, members, assignments) will be preserved
- No more data loss on redeployment!

## 🔄 Environment Variables

Railway will automatically provide:
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Application port

You need to set:
- `FLASK_SECRET_KEY` - Random secret key for sessions
- `ADMIN_USERNAME` - Admin login username  
- `ADMIN_PASSWORD` - Admin login password

## 🛠️ Troubleshooting

If you need to reset the database:
1. Go to Railway dashboard
2. Delete the PostgreSQL service
3. Create a new PostgreSQL service
4. Redeploy your app
5. Visit `/init-admin` to recreate admin user

## 📝 Notes

- The app automatically creates database tables on startup
- Admin user is created via `/init-admin` endpoint
- All data persists between deployments with PostgreSQL
