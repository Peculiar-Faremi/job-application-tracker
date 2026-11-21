A backend API for keeping track of the jobs you've applied to. You add an application, move its status along as things happen (applied, interviewing, and so on), and look things up by the company when you need to.

I built it while teaching myself backend development. It's deployed, so you can actually try it instead of just reading about it.

[!WARNING] PLEASE READ THIS BEFORE YOU TRY IT!!!

This is a demo running on free hosting, and I'm still changing things. So:
- Don't enter anything sensitive. No ID numbers, phone numbers, home addresses, or private details about an employer or an interview. Made-up or low-stakes job info is perfect.
- Don't reuse a password you use anywhere else. Pick something throwaway.
- Your data can be wiped at any time while I'm testing and fixing things.
- If something breaks or feels confusing, tell me. That's the whole reason I'm sharing it.
 
TRY IT
What	                                           Link
Live API       	                     https://job-application-tracker-6y8v.onrender.com
Interactive docs (Swagger)	         https://job-application-tracker-6y8v.onrender.com/docs
Health check	                     https://job-application-tracker-6y8v.onrender.com/health
Frontend                             https://scintillating-bavarois-6721d2.netlify.app                          

The easiest way to play with it right now is the frontend app above. Register a user, log in, press Authorize at the top right, and then you can create and edit applications straight from the browser.

The server sleeps when nobody is using it. I have a monitor pinging it to keep it awake, but if your first request is slow, give it a minute.

WHAT IT DOES
- Sign up and log in. Logins use JWT access and refresh tokens, and you only see your own applications.
- Add an application with a job title, company, link, where you found it, and a status.
- List your applications with pagination and a search.
- Filter by company.
- Update the status of an application as it moves along.
- Delete an application.
- Company names get cleaned up on the way in (extra spaces trimmed, Title Case), so " acme ltd " and "Acme Ltd" end up the same.
- Repeated reads are served from a Redis cache, and requests are rate limited so one person can't hammer the API.

BUILT WITH
FastAPI, SQLAlchemy, Alembic for migrations, Pydantic, PostgreSQL, Redis, JWT auth, pytest, Docker, GitHub Actions, Prisma for database hosting and Render for hosting.

The main endpoints
Method	Path	What it does
POST	/applications/create	Add a new application
GET	/applications/getall	List your applications. Optional skip, limit (default 10, max 100) and search
GET	/applications/company?company_name=Acme	Find your applications for one company
PATCH	/applications/{id}/status	Change the status of an application

There are also routes for registering, logging in and deleting. Everything is listed in /docs, which is always more up to date than this table.

Example body for creating an application:

json
{
  "job_title": "Backend Developer",
  "company": "Acme Ltd"
}

job_link, source, custom_source and status are optional. If you leave out the status it starts as Applied.

Run it on your own machine
You'll need Python, a PostgreSQL database, and a Redis server. The quickest Redis is Docker:

bash
docker run -p 6379:6379 redis
Then:
bash
git clone https://github.com/Peculiar-Faremi/job-application-tracker.git
cd job-application-tracker
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac / Linux

pip install -r requirements.txt

Copy .env.example to .env and fill in your own values (table below). Then create the tables and start the server:

bash
alembic upgrade head
uvicorn app.main:app --reload

Open http://127.0.0.1:8000/docs and you're in.

ENVIRONMENT VARIABLES
Name	What it's for
DATABASE_URL	Your Postgres connection string
REDIS_URL	Your Redis connection string
SECRET_KEY	Signs the login tokens. Make it long and random
ALGORITHM	Token signing algorithm (HS256)
ACCESS_TOKEN_EXPIRE_MINUTES	How long an access token lasts
REFRESH_TOKEN_EXPIRE_DAYS	How long a refresh token lasts
TEST_DATABASE_URL	A separate database used only by the tests
TEST_REDIS_URL	A separate Redis database used only by the tests

Never commit your real .env. It's in .gitignore for a reason.

Tests
bash
pytest

The tests wipe their database and flush Redis before each run, so TEST_DATABASE_URL and TEST_REDIS_URL must point at throwaway ones, never your real data.

HOW IT'S DEPLOYED
API: a Docker web service on Render (free plan, Frankfurt).
Database: Prisma Postgres, in the same region so queries stay fast.
Cache: Upstash Redis (free tier).
Keeping it awake: an UptimeRobot monitor calls /health every 5 minutes. That route doesn't touch the database or Redis, so it's cheap.
CI: GitHub Actions runs the test suite on every push. Render only deploys once the checks pass.

A FEW DECISIONS I MADE
Cached lists expire after 60 seconds and are cleared whenever an application changes, so you don't see stale data after an edit.
The tests run against a separate database and Redis, because they drop tables and flush the cache. I didn't want that anywhere near real data.
/health exists only for Render and the uptime monitor. It answers right away without calling anything else.

WHAT'S NEXT
A frontend, so you don't need Swagger to use it
 
WHO MADE THIS
Built by Peculiar Faremi (@Peculiar-Faremi). If you've tried the app and have thoughts, open an issue on this repo or message me.