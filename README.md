# news-discovery-app
News discovery application

[![News Discovery App](https://github.com/DeejayRevok/news-discovery-app/actions/workflows/pythonapp.yml/badge.svg?branch=develop)](https://github.com/DeejayRevok/news-discovery-app/actions/workflows/pythonapp.yml)
[![codecov](https://codecov.io/gh/DeejayRevok/news-discovery-app/branch/develop/graph/badge.svg?token=5IMQQ2B7QP)](https://codecov.io/gh/DeejayRevok/news-discovery-app)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DeejayRevok_news-discovery-app&metric=alert_status)](https://sonarcloud.io/dashboard?id=DeejayRevok_news-discovery-app)

### Local running

Run the parent's repo dev docker compose.

#### NLP celery worker
Inside the application folder run:
```
export PYTHONPATH={FULL_PATH_TO_APPLICATION_FOLDER}
pip install -r requirements-prod.txt
python worker/main.py -c ./configs/config_local.yml
```
```
export PYTHONPATH={FULL_PATH_TO_APPLICATION_FOLDER}
pip install -r requirements-beat.txt
python worker/beat.py -c ./configs/config_local.yml
```
