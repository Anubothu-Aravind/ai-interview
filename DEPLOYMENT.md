# Deployment Guide

This guide covers deploying the AI Interview System to production.

## Prerequisites

- Python 3.12+
- Node.js 16+
- PostgreSQL database (Supabase recommended)
- OpenAI API key
- Domain name (optional)
- SSL certificate (for HTTPS)

## Backend Deployment

### Option 1: Deploy to a VPS (DigitalOcean, AWS EC2, etc.)

1. **Clone the repository**:
```bash
git clone https://github.com/Anubothu-Aravind/ai-interview.git
cd ai-interview
```

2. **Set up Python environment**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment variables**:
```bash
cp ../.env.example ../.env
# Edit .env with your production credentials
```

4. **Set up database**:
- Create a Supabase project or PostgreSQL database
- Run the SQL schema from `/api/v1/database/schema`
- Update `.env` with database credentials

5. **Install Gunicorn**:
```bash
pip install gunicorn
```

6. **Run with Gunicorn**:
```bash
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

7. **Set up systemd service** (Linux):
Create `/etc/systemd/system/ai-interview-backend.service`:
```ini
[Unit]
Description=AI Interview Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/ai-interview
Environment="PATH=/path/to/ai-interview/backend/venv/bin"
ExecStart=/path/to/ai-interview/backend/venv/bin/gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Start the service:
```bash
sudo systemctl enable ai-interview-backend
sudo systemctl start ai-interview-backend
```

8. **Set up Nginx as reverse proxy**:
Create `/etc/nginx/sites-available/ai-interview-backend`:
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/ai-interview-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

9. **Set up SSL with Let's Encrypt**:
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com
```

### Option 2: Deploy to Heroku

1. **Install Heroku CLI**:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login to Heroku**:
```bash
heroku login
```

3. **Create Procfile** in project root:
```
web: cd backend && gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

4. **Create app and deploy**:
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
heroku config:set SUPABASE_URL=your_url
heroku config:set SUPABASE_SERVICE_ROLE_KEY=your_key
git push heroku main
```

### Option 3: Deploy to Railway/Render

1. Connect your GitHub repository
2. Set environment variables
3. Configure build command: `pip install -r backend/requirements.txt`
4. Configure start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

## Frontend Deployment

### Option 1: Deploy to Vercel

1. **Install Vercel CLI**:
```bash
npm i -g vercel
```

2. **Build the frontend**:
```bash
cd frontend
npm run build
```

3. **Deploy**:
```bash
vercel
```

4. **Set environment variables** in Vercel dashboard:
```
REACT_APP_API_URL=https://api.yourdomain.com
```

### Option 2: Deploy to Netlify

1. **Build the frontend**:
```bash
cd frontend
npm run build
```

2. **Deploy with Netlify CLI**:
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=build
```

3. **Set environment variables** in Netlify dashboard:
```
REACT_APP_API_URL=https://api.yourdomain.com
```

### Option 3: Serve from Nginx

1. **Build the frontend**:
```bash
cd frontend
npm run build
```

2. **Copy build to server**:
```bash
scp -r build/* user@server:/var/www/ai-interview
```

3. **Configure Nginx**:
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    root /var/www/ai-interview;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=sk-...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

### Frontend (.env)
```
REACT_APP_API_URL=https://api.yourdomain.com
```

## Database Setup

1. Create tables in Supabase SQL Editor:
```sql
-- Get schema from: https://your-backend-url/api/v1/database/schema
```

2. Enable RLS (Row Level Security) if needed
3. Set up proper indexes for performance

## Security Checklist

- [ ] Use HTTPS for both frontend and backend
- [ ] Set proper CORS origins in backend config
- [ ] Use strong secrets and rotate regularly
- [ ] Enable rate limiting on API endpoints
- [ ] Set up database backups
- [ ] Monitor API usage and costs
- [ ] Use environment variables for all secrets
- [ ] Enable Supabase RLS policies
- [ ] Set up monitoring and alerting

## Monitoring

### Backend Monitoring
- Use tools like Sentry for error tracking
- Set up application performance monitoring (APM)
- Monitor API response times
- Track OpenAI API usage and costs

### Frontend Monitoring
- Use Google Analytics or similar
- Monitor user flows and dropoff points
- Track errors with Sentry

## Scaling

### Backend Scaling
- Increase Gunicorn workers: `-w 8`
- Use load balancer (AWS ALB, nginx)
- Cache responses where possible
- Optimize database queries

### Frontend Scaling
- Use CDN for static assets
- Enable gzip compression
- Optimize images and assets
- Implement code splitting

## Maintenance

- Regularly update dependencies
- Monitor logs for errors
- Back up database regularly
- Test in staging before production
- Keep documentation updated

## Troubleshooting

### Backend won't start
- Check Python version (3.12+)
- Verify all environment variables are set
- Check logs: `journalctl -u ai-interview-backend -f`

### Frontend API errors
- Verify CORS settings in backend
- Check API URL in frontend .env
- Verify backend is accessible

### Database connection issues
- Check Supabase credentials
- Verify network connectivity
- Check database logs

## Support

For deployment issues, refer to:
- Backend README: `/backend/README.md`
- Frontend README: `/frontend/README.md`
- Main README: `/README.md`
