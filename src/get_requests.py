import requests
from datetime import datetime, timedelta


def get_commit_info(repo_name: str):
    url = f"https://api.github.com/repos/{repo_name}/commits"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        hash = data[0]["sha"]
        last_commit_date = data[0]["commit"]["committer"]["date"]
        author = data[0]["commit"]["author"]["name"]
        message = data[0]["commit"]["message"]

        return hash, last_commit_date, author, message


def get_weather():
    url = ("https://api.open-meteo.com/v1/forecast?latitude=51.51&"
           "longitude=-0.13&current=temperature_2m,relative_humidity_2m,"
           "precipitation_probability,wind_speed_10m")
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature = data["current"]["temperature_2m"]
        humidity = data["current"]["relative_humidity_2m"]
        prep_prob = data["current"]["precipitation_probability"]
        wind_speed = data["current"]["wind_speed_10m"]

        return temperature, humidity, prep_prob, wind_speed


def get_commit_data(repo_owner: str, repo_name: str, creation_date: datetime):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    params = {
        'per_page': 100,
        'page': 1
    }

    days_of_week_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                         'Friday', 'Saturday', 'Sunday']
    commits_per_week = {}
    commits_by_day = {day: 0 for day in days_of_week_list}
    commits_by_hour = {hour: 0 for hour in range(24)}
    contributions = {}

    while True:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            break

        commits = response.json()
        if not commits:
            break

        for commit in commits:
            commit_date = commit['commit']['committer']['date']
            commit_week = datetime.strptime(
                commit_date, "%Y-%m-%dT%H:%M:%SZ"
                ).date()

            if commit_week < creation_date.date():
                continue

            week_start = commit_week - timedelta(days=commit_week.weekday())
            if week_start not in commits_per_week:
                commits_per_week[week_start] = 0

            commits_per_week[week_start] += 1

            commit_day = datetime.strptime(
                commit_date, "%Y-%m-%dT%H:%M:%SZ"
                ).strftime('%A')
            commits_by_day[commit_day] += 1

            commit_hour = datetime.strptime(
                commit_date, "%Y-%m-%dT%H:%M:%SZ"
                ).hour
            commits_by_hour[commit_hour] += 1

            committer_name = commit['commit']['committer']['name']
            contributions[committer_name] = \
                contributions.get(committer_name, 0) + 1

        params['page'] += 1

    return commits_per_week, commits_by_day, commits_by_hour, contributions
