build_chart:
	cat VERSION | xargs -I {} helm package -u --version {} --app-version {} helm/news-discovery

run_news_discovery:
	nohup metricbeat -e -c /etc/metricbeat/metricbeat.yml &
	nohup filebeat -e -c /etc/filebeat/filebeat.yml &
	python app/news_discovery_runner.py -s $(SOURCE_NAME)
