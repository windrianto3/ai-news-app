# ai-news-app
A news app delivering short summaries of NYT articles published today.

## Technologies Used
* New York Times API: used to acquire URLs of news articles published on today's date.  
* Python library `requests`: used to obtain the HTML files of news articles using URLs pulled from the New York Times API.  
* Beautiful Soup 4: used to extract article body text from the HTML files.  
* OpenAI API: used to summarize article body text.  
* Flask: used to serve templated HTML containing the news reports to the user.  
* Microsoft Azure: used to host the Flask server persistently.

## Environment Variables
This project requires three environment variables defined in `.env` of the root directory.
1. `NYT_API_KEY`: Used to acquire URLs and metadata of New York Times articles published on the current day
2. `OPENAI_API_KEY`: Used to summarize New York Times articles using a large language model
3. `MONGO_STR`: Used to connect the Flask server to a MongoDB database for persistent storage of news summaries 
