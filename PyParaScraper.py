#!/usr/bin/env python3

from PPS import scraper, notify
import time
import yaml

def main():
    while True:
        try:
            scraper.set_filters()
            scraper.get_random_user_agent()
            scraper.get_listings()
            scraper.compare_listings()

            if scraper.found_new_listings == True:
                scraper.write_new_listings_to_file()

                for listing in scraper.new_listings:
                    notify.msg = 'New apartment available!\n' + 'https://pararius.nl' + listing[76:].split('\"')[0]
                    print(notify.msg)
                    if chat_platform == "telegram":
                        notify.send_telegram_msg()
                    elif chat_platform == "discord":
                        notify.send_discord_msg()
        except Exception:
            notify.msg = "Scraper encountered an error."
        finally:
            time.sleep(interval_in_seconds)

if __name__ == "__main__":
    # load the config.yml file
    try:
        with open('config.yml') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except:
        print("[x] Could not find the 'config.yml' config file.\n    Copy the 'config.yml.example' file and setup the values.")
        exit(0)

    # start a new instance of scraper
    scraper = scraper()
    scraper.city = config['scraper']['city']
    scraper.neighborhoods = config['scraper']['neighborhoods']
    scraper.residence_type = config['scraper']['residence_type']
    scraper.min_price = config['scraper']['min_price']
    scraper.max_price = config['scraper']['max_price']
    scraper.min_rooms = config['scraper']['min_rooms']
    scraper.min_bedrooms = config['scraper']['min_bedrooms']
    scraper.interior_type = config['scraper']['interior_type']
    scraper.min_m2 = config['scraper']['min_m2']
    interval_in_seconds = config['scraper']['interval_in_seconds']

    # start a new instance of notify
    notify = notify()
    notify.discord_webhook_url = config['notify']['discord_webhook_url']
    notify.telegram_api_token = config['notify']['telegram_api_token']
    notify.telegram_chat_id = config['notify']['telegram_chat_id']
    chat_platform = config['notify']['chat_platform']

    # Run main
    main()
