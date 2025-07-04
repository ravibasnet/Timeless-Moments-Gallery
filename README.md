# Timeless Moments Django Project

## Setup

1. Clone the repo:
   ```
   git clone <your-repo-url>
   cd timeless_moments
   ```
2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root (see `.env.example` for required variables).
4. Run migrations and collect static files:
   ```
   python manage.py migrate
   python manage.py collectstatic
   ```
5. Run locally:
   ```
   python manage.py runserver
   ```

## Deploying to Render

1. Push your code to GitHub.
2. Create a new Web Service on Render and connect your repo.
3. Set environment variables in the Render dashboard:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-app.onrender.com`
   - `SECURE_SSL_REDIRECT=True`
   - (Render will set `DATABASE_URL` for you if using PostgreSQL)
4. Set build and start commands:
   - Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start: `gunicorn timeless_moments.wsgi:application`
5. Deploy and enjoy your live Django app! 