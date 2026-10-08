<div align="center">

# 🧭 DBPilot

**Talk to your database in plain language.**
An AI database analyst that inspects your schema, runs SQL, builds charts and exports reports.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white)

</div>

---

## ✨ Features

- 💬 **Natural-language queries** – ask "what dishes do we have?" or "sales this month?" and get a complete answer
- 🔌 **Multi-database support** – PostgreSQL, MySQL and SQLite
- 📊 **Auto charts** – bar, line and pie charts chosen from the shape of the data
- 📁 **File export** – PDF, Excel, Word, HTML or CSV, only when you ask for it
- 🌍 **Multilingual** – replies in the language of your latest message (Uzbek, Russian, English…)
- 🔐 **Authentication** – sign up / login with hashed passwords and JWT
- 🛡️ **Safe by design** – no schema-changing statements, confirmation for risky updates, secrets and personal data protected

## 🏗️ Architecture

```
┌──────────────┐   HTTP    ┌──────────────┐   SQL    ┌──────────────┐
│  Streamlit   │ ───────▶ │   FastAPI    │ ───────▶ │  Your DB     │
│  (frontend)  │ ◀─────── │  + AI Agent  │ ◀─────── │ PG/MySQL/SQLite │
└──────────────┘           └──────────────┘          └──────────────┘
```

## 📂 Project structure

| File | Purpose |
|---|---|
| `app.py` | Streamlit UI: auth, DB connection sidebar, chat and charts |
| `main.py` | FastAPI backend and API routes |
| `ai_models.py` | AI agent (`chat_agent`) and chat history |
| `prompt.py` | DBPilot system prompt (`AGENT_PROMPT`) |
| `db_conn.py` | App database engine, session and connection check |
| `models.py` / `schemas.py` | SQLAlchemy models and Pydantic schemas |
| `hashing_password.py` | Password hashing and session ID generation |
| `creating_files/` | Generated reports available for download |

## 🚀 Quick start

```bash
# 1. Clone
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export SECRET_KEY="your-secret-key"
# + the API key of your LLM provider (see ai_models.py)

# 4. Create the folder for generated files
mkdir -p creating_files

# 5. Run the backend  → http://localhost:8000
python main.py

# 6. Run the frontend → http://localhost:8501
streamlit run app.py
```

## 🔗 API endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/signin` | Create a new user |
| `POST` | `/login` | Log in and receive a JWT cookie |
| `POST` | `/check_db` | Test a database connection |
| `POST` | `/chat_agent` | Send a question to the AI agent |
| `GET` | `/get_chat_history` | Get chat history by `session_id` |
| `GET` | `/creating_files/{file}` | Download a generated file |

Interactive API docs are available at `http://localhost:8000/docs`.

## 🧑‍💻 How it works

1. Sign up or log in.
2. Choose the database type and connect from the sidebar.
3. Ask anything about your data in the chat.
4. The agent inspects the schema, runs verified SQL and returns an answer with a chart and, if requested, a downloadable file.

## ⚠️ Notes

- Currently intended for local development; restrict CORS and use HTTPS before deploying.
- Never commit your `SECRET_KEY`, API keys or database credentials.

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
