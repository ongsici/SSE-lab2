import requests
from datetime import datetime
from typing import List
from flask import Flask, render_template, request
from src.process_query import process_query
from src.data_model.data_model import RepoInfo, RepoInfoDetails
from src.get_requests import get_commit_data, get_commit_info, get_weather
# from dotenv import load_dotenv

app = Flask(__name__)


# load_dotenv()
# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# headers = {
#     "Authorization": f"token {GITHUB_TOKEN}"
# }


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


@app.route("/api_submit", methods=["POST"])
def api_submit():
    github_name = request.form.get("name")
    repositories: List[RepoInfo] = []
    url = f"https://api.github.com/users/{github_name}/repos"
    response = requests.get(url)

    curr_temp, curr_humidity, curr_prep_prob, curr_wind_speed = get_weather()

    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            hash, last_commit_date, author, message = get_commit_info(
                repo["full_name"]
            )
            repo_info = RepoInfo(
                repo_name=repo["full_name"],
                last_updated=datetime.fromisoformat(
                    last_commit_date.replace("Z", "+00:00")
                ),
                hash=hash,
                author=author,
                message=message
            )
            repositories.append(repo_info)

    return render_template("github.html",
                           name=github_name,
                           data=repositories,
                           temperature=curr_temp,
                           humidity=curr_humidity,
                           prep_prob=curr_prep_prob,
                           wind_speed=curr_wind_speed)


@app.route("/api_repo_info/<name>/<repo_name>", methods=["GET"])
def fetch_repo_info(name: str, repo_name: str):
    repo_full_name = f"{name}/{repo_name}"
    repo_url = f"https://api.github.com/repos/{repo_full_name}"
    repo_response = requests.get(repo_url)

    if repo_response.status_code == 200:
        repo_data = repo_response.json()
        creation_date = datetime.fromisoformat(
            repo_data["created_at"].replace("Z", "+00:00")
        )

        per_week, by_day, by_hour, by_contributor = get_commit_data(
            name, repo_name, creation_date
        )

        week_labels = []
        commits_by_week = []

        for week_start in sorted(per_week.keys()):
            week_labels.append(f"{week_start.strftime('%Y-%m-%d')}")
            commits_by_week.append(per_week[week_start])

        commits_by_day_counts = [by_day[day] for day in
                                 ['Monday', 'Tuesday', 'Wednesday',
                                  'Thursday', 'Friday', 'Saturday',
                                  'Sunday']]

        commits_by_hour_counts = [by_hour[hour] for hour in range(24)]

        contributors = list(by_contributor.keys())
        contribution_counts = list(by_contributor.values())
        creation_date_str = creation_date.isoformat()

        repo_info_details = RepoInfoDetails(
            repo_name=repo_full_name,
            creation_date=creation_date_str,
            weekly_commit_num=commits_by_week,
            week_label=week_labels,
            commits_by_day_counts=commits_by_day_counts,
            commits_by_hour_counts=commits_by_hour_counts,
            contributions_by_contributors=contributors,
            contribution_counts=contribution_counts,
        )

        return render_template("repo_info.html",
                               name=repo_name,
                               repo_info=repo_info_details,
                               week_labels=week_labels,
                               weekly_commit_num=commits_by_week,
                               commits_by_day_counts=commits_by_day_counts,
                               commits_by_hour_counts=commits_by_hour_counts,
                               contributions_by_contributors=contributors,
                               contribution_counts=contribution_counts)


@app.route("/query", methods=["GET"])
def query():
    q = request.args.get("q", "")
    return process_query(q)
