from flask import Flask, jsonify, render_template
import pymongo
from extract_text import _getDate, generateDailyReport
import os
import dotenv
from datetime import datetime
import threading
import schedule
import time

dotenv.load_dotenv()

# Get DB instance
db_str = os.environ.get('MONGO_STR')
connection = pymongo.MongoClient(db_str)
db = connection['Summarizer']

app = Flask(__name__)

@app.route("/")
def serve():
    date = _getDate()
    today_date_str = datetime.now().strftime("%A, %B %d, %Y")
    
    collection_list = db.list_collection_names()
    if date not in collection_list:
        print("Creating a report")
        # If date not in DB, create report
        article_data = generateDailyReport("Technology")
        today_collection = db[date]

        for article in article_data.items():
            today_collection.insert_one(
                {
                    "title" : article[1]['title'],
                    "abstract" : article[1]['abstract'],
                    "url" : article[1]['url'],
                    "summary" : article[1]['summary']
                }
            )
            
    cursor = db[date].find()
    data = {}
    for document in cursor:
        url = document['url']
        data[url] = {}
        data[url]['summary'] = document['summary']
        data[url]['abstract'] = document['abstract']
        data[url]['title'] = document['title']
        data[url]['url'] = url
    
    # Article data is returned here.
    #return jsonify(data)
    return render_template("daily_report.html", articles=data, date=today_date_str)

def convert_date_string(date_str):
    return datetime.strptime(date_str, "%Y%m%d").date().strftime("%Y%m%d")

# Route to display a daily report for a specific date
@app.route("/daily_report/<date>")
def view_daily_report(date):
    try:
        # Convert the date string to a datetime object
        report_date = (convert_date_string(date))
        collection_list = db.list_collection_names()
        print(report_date)
        
        today_date_str = datetime.now().strftime("%A, %B %d, %Y")
        
        # Check if a report exists for the specified date
        if report_date in collection_list:
            # Render the daily_report.html template with the report data
            cursor = db[report_date].find()
            data = {}
            for document in cursor:
                url = document['url']
                data[url] = {}
                data[url]['summary'] = document['summary']
                data[url]['abstract'] = document['abstract']
                data[url]['title'] = document['title']
                data[url]['url'] = url
            return render_template("daily_report.html", articles=data, date = today_date_str)
        else:
            # Render an error page if the report doesn't exist
            return render_template("error.html", message="No report available for this date.")
    except ValueError:
        # Handle the case where an invalid date format is provided
        return render_template("error.html", message="Invalid date format. Please use YYYYMMDD.")

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

# Schedule the function to run daily at 12:00 PM
schedule.every().day.at("20:16").do(generate_daily_report)

if __name__ == '__main__':
    # Start the scheduled task in a separate thread
    def scheduled_task():
        while True:
            schedule.run_pending()
            time.sleep(60)  # Sleep for 60 seconds

    scheduler_thread = threading.Thread(target=scheduled_task)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    app.run(port=5000, debug=False)

        
        
    
    
    