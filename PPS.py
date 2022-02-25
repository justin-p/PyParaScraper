from bs4 import BeautifulSoup
import requests
import os
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

class scraper:
    def __init__(self):
        # setup initial default values
        self.last_30_listings = None
        self.new_listings = None
        self.found_new_listings = False
        self.city = None
        self.neighborhoods = []
        self.residence_type = None
        self.valid_residence_types = ["huis","appartement","studio","kamer"]
        self.min_price = None
        self.max_price = None
        self.min_rooms = None
        self.min_bedrooms = None
        self.interior_type = None
        self.valid_interior_types = ["kaal", "gemeubileerd", "gestoffeerd"]
        self.min_m2 = None
        self.base_url = "https://www.pararius.nl/huurwoningen/"
        self.url_filters = None
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        self.output_filename = "scraped_listings.txt"

    # set filters
    def set_filters(self):
        # set city
        try:
            if self.city is None:
                raise RuntimeError('self.city is set to None.')
            else:
                self.url_filters = self.city + '/'
        except:
            raise

        # add neighborhoods
        d = ","
        if len(self.neighborhoods) != 0:
            self.url_filters = self.url_filters + "wijk-" + d.join(self.neighborhoods) + "/"

        # add residence type
        if self.residence_type is not None:
            if self.residence_type not in self.valid_residence_types:
                raise RuntimeError('self.residence_type is set to invalid value. Valid types are: ' + ', '.join(self.valid_residence_types))
            self.url_filters = self.url_filters + self.residence_type + "/"

        # add min/max price
        if self.min_price is not None:
            self.url_filters = self.url_filters + str(self.min_price)
            if self.max_price is not None:
                self.url_filters = self.url_filters + '-' + str(self.max_price) + "/"
            else:
                self.url_filters = self.url_filters + '-' + "60000/"
        elif self.max_price is not None:
            self.url_filters = self.url_filters + "0-" + str(self.max_price) + "/"
        
        # add min rooms
        if self.min_rooms is not None:
            self.url_filters = self.url_filters + str(self.min_rooms) + "-aantalkamers/"

        # add min bedrooms
        if self.min_bedrooms is not None:
            self.url_filters = self.url_filters + str(self.min_bedrooms) + "-slaapkamers/"

        # add interior type
        if self.interior_type is not None:
            if self.interior_type not in self.valid_interior_types:
                raise RuntimeError('self.interior_type is set to invalid value. Valid types are: ' + ', '.join(self.valid_interior_types))
            self.url_filters = self.url_filters + self.interior_type + "/"

        # add min square meters
        if self.min_m2 is not None:
            self.url_filters = self.url_filters + str(self.min_m2) + "m2/"

        self.url = self.base_url + self.url_filters

    # get random user agent
    def get_random_user_agent(self):
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value]  
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
        self.user_agent = user_agent_rotator.get_random_user_agent()

    # scrape Pararius page and get the first 30 listings
    def get_listings(self):
        headers = {'User-Agent': self.user_agent}
        content = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(content.text, features='html.parser')
        # check if we got captha'd
        captha = soup.find_all('p', class_='header')
        try:
            if captha != []:
                raise RuntimeError('Pararius is throwing the following error: ' + str(captha) + '\nIf Pararius thinks you are a bot try using the get_random_user_agent function.')
            else:
                # Search for the a-tag containing the listings
                self.last_30_listings = soup.find_all('a', class_='listing-search-item__link listing-search-item__link--title')
        except:
            raise

    # check whether given listings have already been found in a previous run
    def compare_listings(self):
        # clear previous run
        self.new_listings = None
        self.found_new_listings = False

        if not os.path.exists(self.output_filename):
            open(self.output_filename, 'w').close()
        with open(self.output_filename, 'r+') as f:
            known_listings = [line.rstrip() for line in f]
            listings = [str(listing) for listing in self.last_30_listings]
            new_listings = list(set(listings) - set(known_listings))
                
            if new_listings:
                self.new_listings = new_listings
                self.found_new_listings = True
    
    # write new listings to local file
    def write_new_listings_to_file(self):
        with open(self.output_filename, 'r+') as f:
            for listing in self.new_listings:
                f.write(str(listing) + '\n')

from discord_webhook import DiscordWebhook
import telegram

class notify:
    def __init__(self):
        # setup initial default values
        self.msg = None
        self.telegram_api_token = None
        self.telegram_chat_id = None # Start a chat with your bot, then visit https://api.telegram.org/bot<YourBOTToken>/getUpdates to see your token
        self.discord_webhook_url = None

    def send_telegram_msg(self):
        bot = telegram.Bot(token=self.telegram_api_token)
        bot.send_message(chat_id=self.telegram_chat_id, text=self.msg)

    def send_discord_msg(self):
        webhook = DiscordWebhook(url=self.discord_webhook_url, content=self.msg, rate_limit_retry=True)
        webhook.execute()