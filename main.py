import os
import openai
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

# Set your OpenAI API key
openai.api_key = "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"

app = Flask(__name__)

# Function to get the summary from OpenAI
def generate_summary(text):
    model_engine = "text-davinci-002"
    prompt = (f"Please summarize what this company does:\n{text}")
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = completions.choices[0].text.strip()
    return message

# Function to scrape the website and get the relevant text
def scrape_website(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    text = ""
    for p in soup.find_all("p"):
        text += p.get_text()
    return text

# Define the route for the home page
@app.route("/")
def home():
    return render_template("index.html")

# Define the route for the summary page
@app.route("/summary", methods=["POST"])
def summary():
    url = request.form["url"]
    text = scrape_website(url)
    summary = generate_summary(text)
    return render_template("summary.html", summary=summary)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get('PORT', 5000))

