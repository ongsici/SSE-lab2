import math
import requests
import os
from process_query import process_query
from datetime import datetime
from typing import List
from flask import Flask, render_template, request
from data_model.data_model import RepoInfo
from dotenv import load_dotenv
app = Flask(__name__)


load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/api")
def hello_api():
    return render_template("api_form.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    input_gender = request.form.get("gender")
    input_happiness = request.form.get("happy")
    if int(input_happiness) >= 0:
        return render_template("happy.html",
                               name=input_name,
                               age=input_age,
                               gender=input_gender,
                               happy=input_happiness)
    else:
        return render_template("sad.html",
                               name=input_name,
                               age=input_age,
                               gender=input_gender,
                               happy=input_happiness)
    
def get_commit_info(repo_name):
    url = f"https://api.github.com/repos/{repo_name}/commits"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        hash = data[0]["sha"]
        last_commit_date = data[0]["commit"]["committer"]["date"]
        author = data[0]["commit"]["author"]["name"]
        message = data[0]["commit"]["message"]

    return hash, last_commit_date, author, message

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=51.51&longitude=-0.13&current=temperature_2m,relative_humidity_2m,precipitation_probability,wind_speed_10m"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature= data["current"]["temperature_2m"]
        humidity = data["current"]["relative_humidity_2m"]
        prep_prob = data["current"]["precipitation_probability"]
        wind_speed = data["current"]["wind_speed_10m"]

        return temperature, humidity, prep_prob, wind_speed
    
@app.route("/api_submit", methods=["POST"])
def api_submit():
    github_name = request.form.get("name")
    repositories: List[RepoInfo] = []  
    url = f"https://api.github.com/users/{github_name}/repos"
    response = requests.get(url, headers=headers)

    curr_temp, curr_humidity, curr_prep_prob, curr_wind_speed = get_weather()

    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            hash, last_commit_date, author, message = get_commit_info(repo["full_name"])
            repo_info = RepoInfo(
                repo_name=repo["full_name"],
                last_updated=datetime.fromisoformat(last_commit_date.replace("Z", "+00:00")),
                hash = hash,
                author = author,
                message = message                
            )
            repositories.append(repo_info) 

    return render_template("github.html",
                           name=github_name,
                           data=repositories,
                           temperature=curr_temp,
                           humidity = curr_humidity,
                           prep_prob = curr_prep_prob,
                           wind_speed = curr_wind_speed)


@app.route("/query", methods=["GET"])
def query():
    q = request.args.get("q", "")
    return process_query(q)
