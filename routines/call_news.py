from newsapi.articles import Articles
import json
from time import sleep
from datetime import datetime
from threading import Thread


class call_news(object):
    def __init__(self, bot, interval=3600):
        self.interval = interval
        self.bot = bot

        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            a = Articles(API_KEY=self.bot.newsapi_key)
            try:
                data = a.get(source='bbc-news', sort_by='top')
            except:
                print(
                    'News-API Error: Either server didn\'t respond or has resulted in zero results'
                )
            else:
                if data["status"] == "error":
                    print(data["message"])
                else:
                    data["update"] = f"[Updated {datetime.utcnow()} (UTC)]"
                    profile = open('bot_data/news.json', "w")
                    json.dump(data, profile)
                    print(f'News Updated {data["update"]}')
                    profile.close()
            finally:
                sleep(self.interval)
