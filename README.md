# Zoominfo Interview: Company Data Scrapy Spider

A scrapy Spider for that crawls [sos.nd.gov](https://firststop.sos.nd.gov/search/business)
## Local Run

```bash
#source yourvenv/bin/activate
pip install -r requirements.txt
```

```bash
#specify your Search Letter and items, logfile output file
scrapy crawl company_search_spider -a startswith='X' -O items.json --logfile output.log
```
<br>

## Docker Run

```bash
docker build -t myspider .
```

```bash
docker run myspider
```

## Info about crawler
Crawler outputs data in json format in `items.json`, all the data it can find that start with argument `startswith`
