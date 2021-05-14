import datetime
from bs4 import BeautifulSoup
import requests
import functools
import operator
import json

from scraper.i_scraper import Scraper


class StackOverflowScraper(Scraper):
    def scrape(self, criteria):
        target_url = 'https://stackoverflow.com/jobs?l=' + criteria + '&d=20&u=Km'

        source = requests.get(target_url).text
        soup = BeautifulSoup(source, 'html5lib')

        title_tags = soup.find_all('a', class_="s-link stretched-link")
        company_parent_tag = soup.find_all('h3', class_='fc-black-700 fs-body1 mb4')
        published_dates_tags = soup.find_all('ul', class_='mt4 fs-caption fc-black-500 horizontal-list')
        published_dates = []
        for date in published_dates_tags:
            published_dates.append(date.find('span').text.strip())

        job_offers = []
        for index, x in enumerate(title_tags, start=0):
            if 'h' in published_dates[index]:
                job_offers.append({
                    'job_title': title_tags[index].text.strip(),
                    'company': company_parent_tag[index].findChild().text.strip(),
                    'location': 'Barcelona',
                    'link': 'https://stackoverflow.com/' + title_tags[index].get('href'),
                    'published_at': published_dates[index],
                })

        return job_offers

    def get_job_offers(self):
        return self.scrape('Barcelona')
