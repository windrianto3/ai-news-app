# AI-summarized News Feed
A news app delivering short summaries (by AI) of NYT articles published today, powered by New York Times API and OpenAI API. Currently, the app grabs at most 10 articles (or less depending on how many were published today) relating to technology and displays them to the user.
  
Check out a sample deployment at:  
https://flask-ai-app.azurewebsites.net/

Each section of the page corresponds to a news article published today, which includes the corresponding title header, abstract, AI-generated summary, and a link to the original article if the reader desires to read more.

## Technologies Used
* New York Times API: used to acquire URLs of news articles published on today's date.  
* Python library `requests`: used to obtain the HTML files of news articles using URLs pulled from the New York Times API.  
* Beautiful Soup 4: used to extract article body text from the HTML files.  
* OpenAI API: used to summarize article body text.  
* Flask: used to serve templated HTML containing the news reports to the user.
* MongoDB: used to store all the daily news feeds in JSON-like format
* Microsoft Azure: used to host the Flask server persistently.

## Environment Variables
This project requires three environment variables defined in `.env` of the root directory.
1. `NYT_API_KEY`: Used to acquire URLs and metadata of New York Times articles published on the current day
2. `OPENAI_API_KEY`: Used to summarize New York Times articles using a large language model
3. `MONGO_STR`: Used to connect the Flask server to a MongoDB database for persistent storage of news summaries 
