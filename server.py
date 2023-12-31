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

print("MongoSTR below")
print(db_str)

connection = pymongo.MongoClient(db_str)
db = connection['Summarizer']

app = Flask(__name__)

def get_recent_report_date():
    def date_key(date_str):
        return int(date_str)
    
    dates = db.list_collection_names()
    most_recent_date = max(dates, key=date_key)
    return most_recent_date

def format_date(date):
    return datetime.strptime(date, "%Y%m%d").strftime("%B %d, %Y")

@app.route("/status")
def status():
    return "ALIVE"

@app.route("/")
def serve():
    most_recent_date = get_recent_report_date()
            
    cursor = db[most_recent_date].find()
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
    return render_template("daily_report.html", articles=data, date=format_date(most_recent_date))

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
            return render_template("daily_report.html", articles=data, date = format_date(report_date))
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
schedule.every().day.at("11:10:00").do(generate_daily_report)

if __name__ == '__main__':
    # Start the scheduled task in a separate thread
    def scheduled_task():
        while True:
            schedule.run_pending()
            time.sleep(60)  # Sleep for 60 seconds

    scheduler_thread = threading.Thread(target=scheduled_task)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    app.run(host = "0.0.0.0", port=35000, debug=False)

        
        
    
    
    