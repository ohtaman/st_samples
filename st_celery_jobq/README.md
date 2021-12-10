```
env $(cat .env) poetry run watchmedo auto-restart -d . -p '*py' -- celery --app=worker.app worker

env $(cat .env) poetry run streamlit run --server.runOnSave true app.py
```