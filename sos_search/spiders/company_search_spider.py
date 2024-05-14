import json
from scrapy import Request, Spider
from scrapy.http import Response
import numpy as np


class CompanySearchSpider(Spider):
    name = "company_search_spider"
    allowed_domains = ["sos.nd.gov"]

    def __init__(self, startswith='X', *args, **kwargs):
        super(CompanySearchSpider, self).__init__(*args, **kwargs)
        self.startswith = startswith
        self.HEADERS = {
            'authority': 'firststop.sos.nd.gov',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': 'undefined',
            'content-type': 'application/json',
            'origin': 'https://firststop.sos.nd.gov',
            'referer': 'https://firststop.sos.nd.gov/search/business',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        }

    def start_requests(self):
        body = {
            # apparently the startswith filter on the website doesn't filter quite good, so we can filter our items later if we require to
            'SEARCH_VALUE': self.startswith,
            'STARTS_WITH_YN': 'true',  # startswith
            'ACTIVE_ONLY_YN': 'true',  # active only
        }
        r = Request(
            url='https://firststop.sos.nd.gov/api/Records/businesssearch',
            method='POST',
            headers=self.HEADERS,
            body=json.dumps(body),
            callback=self.parse_company)
        self.logger.info(
            "Calling Initial Request with params: {0}".format(body))

        return [r]

    def parse_company(self, response: Response):
        if response.status == 200:
            companies_data = json.loads(response.body)

            for key, company_row in companies_data['rows'].items():
                yield Request(
                    url='https://firststop.sos.nd.gov/api/FilingDetail/business/{0}/false'.format(
                        key),
                    method='GET',
                    headers=self.HEADERS,
                    meta={'company_row': company_row},
                    callback=self.parse_filing)

    def parse_filing(self, response: Response):
        company_details = {}

        if response.meta.get('company_row', ''):
            company_row = response.meta['company_row']
            company_details.update(company_row)

        if response.status == 200:
            filing_details = json.loads(response.body)
            filing_details = filing_details.get('DRAWER_DETAIL_LIST', {})

            if filing_details:
                for detail in filing_details:
                    company_details.update({detail['LABEL']: detail['VALUE']})
            else:
                self.logger.info(
                    "parse_filing:: failed to obtain filing_details for {0}".format(response.url))

            # Splitting title field from title and sector
            title_field = company_details['TITLE']
            company_details['TITLE'] = title_field[0] if len(
                title_field) > 1 else title_field
        return company_details