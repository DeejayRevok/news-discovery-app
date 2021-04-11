# news-discovery-app
News discovery application

[![News Discovery App](https://github.com/DeejayRevok/news-discovery-app/actions/workflows/pythonapp.yml/badge.svg?branch=develop)](https://github.com/DeejayRevok/news-discovery-app/actions/workflows/pythonapp.yml)
[![codecov](https://codecov.io/gh/DeejayRevok/news-discovery-app/branch/develop/graph/badge.svg?token=5IMQQ2B7QP)](https://codecov.io/gh/DeejayRevok/news-discovery-app)

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
