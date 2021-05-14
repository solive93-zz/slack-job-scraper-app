import datetime
from bs4 import BeautifulSoup
import requests
import functools
import operator
import json

from scraper.i_scraper import Scraper


class DomestikaScraper(Scraper):
    AREA_CRITERIA = [
        '7-desarrollo-de-software',
        '57-desarrollo-web',
        '169-desarrollo-de-apps',
        '125-diseno-mobile',
        '130-css',
        '56-diseno-web'
    ]

    LOCATION_CRITERIA = [
        '122-barcelona-espana',
        '127-barcelona-espana',
        'remote',
    ]

    def scrape(self, criteria):
        area = criteria[0]
        location = criteria[1]
        target_url = 'https://www.domestika.org/es/jobs/area/'+area+'/where/'+location

        source = requests.get(target_url).text
        soup = BeautifulSoup(source, 'html5lib')

        job_titles = soup.find_all('a', class_='job-title')
        companies = soup.find_all('h3', class_='job-item__company')
        contract_types = soup.find_all('div', class_='circle-badge')
        locations = soup.find_all('div', class_='job-item__city')
        published_dates = soup.find_all('div', class_='job-item__date')
        # img_urls = soup.find_all('img', class_=' lazyloaded')
        # print(len(img_urls))
        y_datetime = datetime.date.today() - datetime.timedelta(days=1)
        yesterday = '{:02d}'.format(y_datetime.day)+'/'+'{:02d}'.format(y_datetime.month)+'/'+str(y_datetime.year)[-2:]

        job_offers = []
        for index, x in enumerate(job_titles, start=0):
            if yesterday == published_dates[index].text.strip():
                job_title = job_titles[index].text.strip()
                target_terms = ['Developer', 'Programador', 'Software', 'Software Engineer', 'Devops', 'Full-Stack', 'Data Engineer', 'Data Analyst']
                if any(target_term in job_title.strip() for target_term in target_terms):
                    job_offers.append({
                        'job_title': job_title,
                        'company': companies[index].text.strip(),
                        'contract': contract_types[index].text.strip(),
                        'location': locations[index].text.strip(),
                        'link': job_titles[index].get('href'),
                        # 'img_url': img_url[index],
                        'published_at': published_dates[index].text.strip(),
                    })

        return job_offers

    def get_job_offers(self):
        all_job_offers = []
        for area in self.AREA_CRITERIA:
            for location in self.LOCATION_CRITERIA:
                all_job_offers.append(self.scrape([area, location]))

        return functools.reduce(operator.iconcat, all_job_offers, [])
