import pymongo
from extract_text import _getDate, generateDailyReport
import os
import dotenv

"""
This script generates a news feed for the current day and adds the news feed to the database.

Possible uses:
1. Use this with Cloud function or Azure function, configure to run everyday at a specified time, so you can have a fresh news feed everyday.
2. Use this locally and run it when you want to update the news feed.

After the script is executed, the user will see the fresh news feed when entering the site.
"""

dotenv.load_dotenv()

# Get DB instance
db_str = os.environ.get('MONGO_STR')

print("MongoSTR below")
print(db_str)

connection = pymongo.MongoClient(db_str)
db = connection['Summarizer']

# Scheduled function to run everyday at a specified time 
def generate_daily_report():
    date = _getDate()

    collection_list = db.list_collection_names()
    if date not in collection_list:
        print("Creating a report")
        # If date not in DB, create report
        article_data = generateDailyReport("Technology")
        today_collection = db[date]

        for article in article_data.items():
            today_collection.insert_one(
                {
                    "title": article[1]['title'],
                    "abstract": article[1]['abstract'],
                    "url": article[1]['url'],
                    "summary": article[1]['summary']
                }
            )

generate_daily_report()