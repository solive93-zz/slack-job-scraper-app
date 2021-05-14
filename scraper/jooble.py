import datetime
from bs4 import BeautifulSoup, NavigableString
import requests
import functools
import operator
import json

from scraper.i_scraper import Scraper


class JoobleScraper(Scraper):
    POSITION_CRITERIA = ['developer', 'programador', 'software']

    def scrape(self, criteria):
        target_url = 'https://es.jooble.org/SearchResult?date=8&p=3&rgns=Barcelona&ukw='+criteria

        source = requests.get(target_url).text
        soup = BeautifulSoup(source, 'html5lib')

        job_cards = soup.find_all('article')

        job_offers = []
        for index, card in enumerate(job_cards, start=0):
            a_tag = card.find('a', class_='_9d1c6 _0314c _70395')
            job_title_parent_tag = a_tag.find('span', class_='a7df9')

            job_title = ''
            for child in job_title_parent_tag.children:
                if not isinstance(child, NavigableString):
                    job_title += child.text

            company_tag = card.find('p', class_='_786d5') or ''
            if company_tag:
                publish_date = card.find('div', class_='caption _67a6a').text.strip()
                if not 'días' in publish_date:
                    if not any(job['job_title'] == job_title.strip() for job in job_offers) and not any(job['company'] == company_tag.text.strip() for job in job_offers):
                        target_terms = ['Developer', 'Programador', 'Software', 'Software Engineer', 'Devops', 'Full-Stack', 'Data Engineer', 'Data Analyst']
                        if any(target_term in job_title.strip() for target_term in target_terms):
                            job_offers.append({
                                'job_title': job_title.strip(),
                                'company': company_tag.text.strip(),
                                'location': 'Barcelona',
                                'link': 'https://es.jooble.org' + a_tag.get('href'),
                                'published_at': publish_date
                            })

        return job_offers

    def get_job_offers(self):
        all_job_offers = []
        for criteria in self.POSITION_CRITERIA:
            all_job_offers.append(self.scrape(criteria))

        return functools.reduce(operator.iconcat, all_job_offers, [])
