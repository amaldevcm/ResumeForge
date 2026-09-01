# ResumeForge

ResumeForge is a job-search assistant that uses retrieval-augmented matching to find your best-fit resume for a given job description, then helps you customize it and generate a cover letter with an LLM.

## How it works

1. You upload one or more versions of your resume (PDF, DOCX, or TXT).
2. Each resume is parsed to text, embedded with `sentence-transformers` (`all-MiniLM-L6-v2`), and:
   - the vector is stored in **Pinecone**,
   - the extracted text and metadata are stored in **PostgreSQL** (hosted on Supabase),
   - the original file is stored in a **Supabase Storage** bucket.
3. When you pick a job description, ResumeForge embeds it the same way and queries Pinecone for the resume with the highest cosine similarity, scoped to your account.
4. From there you can use the built-in LLM integration (Groq) to tailor the matched resume to the job description and generate a cover letter.

## Architecture

```
Frontend/   React 19 + TypeScript + Vite + Tailwind CSS
Backend/    Flask REST API
```

The frontend talks to the backend exclusively over `VITE_SERVER_URL` (see [Environment variables](#environment-variables)). There is no server-side rendering — the Flask app is a pure JSON API (plus the Google OAuth redirect flow).

### Backend layout

```
Backend/
  app.py                 # Flask app: routes only, delegates to Services/
  DB.py                  # SQLAlchemy engine/session + Supabase client
  CreateTable.py         # One-time script to (re)create DB tables
  Models/Models.py        # SQLAlchemy models: User, Document
  Services/
    UserService.py        # Auth, profile, password, account deletion
    DocumentService.py    # Resume upload, parsing, embeddings, grading
    PineconeService.py    # Vector CRUD + cosine-similarity search
    JobService.py         # Job search (JSearch API) + job detail lookup
  Prompts/
    LLM.py                # Groq client wrapper
    ResumeReview.py        # Improvement-suggestion prompt
    customResume.py        # Resume customization / cover-letter prompt
```

### Frontend layout

```
Frontend/src/
  Pages/          One component per route (Login, Signup, JobList, JobDetails,
                  ResumeList, NewResumeEntry, Feedback, Profile)
  Components/     Shared UI (Navbar, Spinner)
  AppRouter.tsx   Route table
```

## Features

- Email/password signup & login, plus Google OAuth
- Profile management: view/edit profile, change password, delete account
- Upload multiple resume versions per user
- RAG-based resume ranking against a job description (Pinecone cosine similarity)
- Job search via the JSearch API
- LLM-powered resume customization and cover letter generation (Groq)

## Getting started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Accounts/keys for: Pinecone, Supabase (Postgres + Storage), Google Cloud OAuth client, Groq, RapidAPI (JSearch)

### Backend setup

```bash
cd Backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

Create `Backend/.env` with the variables listed below, then create the database tables **once**:

```bash
python CreateTable.py
```

> ⚠️ `CreateTable.py` drops all existing tables before recreating them. Only run it on first setup, or you will lose data.

Start the dev server:

```bash
flask --app app run --port 5000
```

### Frontend setup

```bash
cd Frontend
npm install
```

Create `Frontend/.env`:

```
VITE_SERVER_URL="http://localhost:5000"
```

Start the dev server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173`.

## Environment variables

### `Backend/.env`

| Variable | Purpose |
|---|---|
| `PINECONE_API_KEY`, `PINECONE_HOST`, `PINECONE_INDEX_NAME` | Pinecone vector index |
| `POSTGRES_URL` / `user`, `password`, `host`, `port`, `dbname` | PostgreSQL connection (Supabase-hosted) |
| `SUPABASE_URL`, `SUPABASE_KEY` | Supabase client (Storage + Postgres) |
| `OAUTH_CLIENT_ID`, `OAUTH_SECRET` | Google OAuth client credentials |
| `FLASK_SECRET_KEY` | Signs the session cookie — required for login/signup to work |
| `FRONTEND_ORIGIN` | Frontend URL, used for CORS and post-OAuth redirects (default `http://localhost:5173`) |
| `IS_PRODUCTION` | Set to `true` once deployed behind HTTPS with the frontend on a different domain than the backend. Switches the session cookie to `SameSite=None; Secure` so login persists across the cross-site requests a split frontend/backend deployment makes — without this, login will appear to succeed but the session won't stick. Leave unset (`false`) for local dev. |
| `GROQ_API_KEY` | Groq LLM API access |
| `RAPIDAPI_KEY` | JSearch API (job search) |

### `Frontend/.env`

| Variable | Purpose |
|---|---|
| `VITE_SERVER_URL` | Base URL of the backend API |

### Google OAuth setup

In [Google Cloud Console → APIs & Services → Credentials](https://console.cloud.google.com/apis/credentials), add an **Authorized redirect URI** matching your backend host, e.g.:

```
http://localhost:5000/login/google/authorized
```

## Known limitations

- The resume grading/feedback flow (`/api/grade`, the Feedback page) is not fully wired up yet.
- Deleting a user does not cascade-delete their resumes, Pinecone vectors, or Supabase-stored files.
- No automated test suite yet.
