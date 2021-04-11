# news-discovery-app
News discovery application

### Local running

Run the parent's repo dev docker compose.

#### NLP celery worker
Inside the application folder run:
```
export PYTHONPATH={FULL_PATH_TO_APPLICATION_FOLDER}
pip install -r requirements.txt
python worker/main.py -p LOCAL
```
```
export PYTHONPATH={FULL_PATH_TO_APPLICATION_FOLDER}
pip install -r requirements-beat.txt
python worker/beat.py -p LOCAL
```