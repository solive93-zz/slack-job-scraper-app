import functools
import operator
import os
from slack import WebClient
from slack.errors import SlackApiError
from bot.builder import construct_payload
from scraper.domestika import DomestikaScraper
from scraper.jooble import JoobleScraper
from scraper.stack_overflow import StackOverflowScraper


class BotMessager:
    SLACK_WEB_CLIENT = WebClient('xoxb-1621885880725-2004393380455-6dx93IiDYBofONYRJuZeYJs4')

    JOB_OFFERS_SCRAPPERS = [
        DomestikaScraper(),
        StackOverflowScraper(),
        JoobleScraper()
    ]

    def scrape_all_job_offers(self):
        job_offers = []
        for scraper in self.JOB_OFFERS_SCRAPPERS:
            job_offers.append(scraper.get_job_offers())

        return functools.reduce(operator.iconcat, job_offers, [])

    def post_job_offers_to_channel(self):
        blocks = [{
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":robot_face: Hey Terrassa Devs! Les ofertes que he trobat avui :point_down::point_down::point_down:"
            },
        }]

        for job_offer in self.scrape_all_job_offers():
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ':female-technologist: *'+job_offer['job_title']+'* - '+job_offer['company']+' \n:round_pushpin: ' + job_offer['location']
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": ":point_right: Veure oferta",
                        "emoji": True
                    },
                    "value": "click_me",
                    "url": job_offer['link'],
                    "action_id": "button_action"
                }
            })
            # blocks.append({
            #     "type": "divider"
            # })

        message = construct_payload(blocks)

        self.SLACK_WEB_CLIENT.chat_postMessage(**message)
