FROM python:3.8-buster
COPY ./ /app/news_discovery_app

WORKDIR /app

RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
RUN apt-get install apt-transport-https -y
RUN echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-7.x.list
RUN apt-get update && apt-get install metricbeat

RUN pip install --upgrade pip
RUN pip install -r news_discovery_app/requirements.txt

COPY ./tools_config/metricbeat.yml /etc/metricbeat/metricbeat.yml

CMD service metricbeat start && export PYTHONPATH=${PYTHONPATH}:/app/news_discovery_app && python ./news_discovery_app/worker/main.py -p DOCKER