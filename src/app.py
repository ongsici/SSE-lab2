import math
import requests
import os
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

def is_square(n):
    return int(math.sqrt(n)) ** 2 == n


def is_cube(n):
    return int(round(n ** (1/3))) ** 3 == n


def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def process_query(input):
    plus_count = input.count("plus")
    if plus_count == 2:
        new_input = input.replace("?", "")
        value1 = int(new_input.split(" ")[2])
        value2 = int(new_input.split(" ")[4])
        value3 = int(new_input.split(" ")[6])
        return str(value1+value2+value3)

    if "numbers are primes" in input:
        input = input.replace("?", "")
        value = input.split(":")[-1].split(",")
        result = []
        for number in value:
            number = number.strip()
            if is_prime(int(number)):
                result.append(number)
        return ",".join(result)

    if "minus" in input:
        new_input = input.replace("?", "")
        value1 = int(new_input.split(" ")[2])
        value2 = int(new_input.split(" ")[4])
        return str(value1-value2)

    if "multiplied by" in input:
        new_input = input.replace("?", "")
        value1 = int(new_input.split(" ")[2])
        value2 = int(new_input.split(" ")[5])
        return str(value1*value2)

    if "square and a cube" in input:
        input = input.replace("?", "")
        value = input.split(":")[-1].split(",")
        result = []
        for number in value:
            number = number.strip()
            if is_square(int(number)) and is_cube(int(number)):
                result.append(number)
        return ",".join(result)

    if plus_count == 1:
        new_input = input.replace("?", "")
        value1 = int(new_input.split(" ")[2])
        value2 = int(new_input.split(" ")[4])
        return str(value1+value2)

    if "numbers is the largest" in input:
        input = input.replace("?", "")
        value = input.split(":")[-1].split(",")
        return max(value)

    if "your name" in input:
        return "SiCi"

    if input == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    else:
        return "Unknown"


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
    
@app.route("/api_submit", methods=["POST"])
def api_submit():
    github_name = request.form.get("name")
    repositories: List[RepoInfo] = []  
    url = f"https://api.github.com/users/{github_name}/repos"
    response = requests.get(url, headers=headers)

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
                           data=repositories)


@app.route("/query", methods=["GET"])
def query():
    q = request.args.get("q", "")
    return process_query(q)
