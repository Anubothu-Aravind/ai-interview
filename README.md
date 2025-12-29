# ai-interview
ai-interview/
│
├── main.py                 # Streamlit entry point
├── app/
│   ├── __init__.py
│   ├── config.py           # Page config, CSS, env loading
│   ├── state.py            # Session state initialization
│   ├── database.py         # Supabase DB manager
│   ├── openai_client.py    # OpenAI init + AI functions
│   ├── audio.py            # TTS / STT helpers
│   ├── utils.py            # PDF + generic helpers
│   ├── ui.py               # UI components (setup, interview, results)
│   └── history.py          # Interview history screen
│
├── pyproject.toml
├── .env
└── README.md
