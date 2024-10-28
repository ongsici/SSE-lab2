from flask import Flask, render_template, request
app = Flask(__name__)


def process_query(input):
    if "plus" in input:
        new_input = input.replace("?", "")
        value1 = int(new_input.split(" ")[2])
        value2 = int(new_input[:-1].split(" ")[4])
        return str(value1+value2)
    if "numbers is the largest" in input:
        input = input.replace("?", "")
        value = input[:-1].split(":")[-1].split(",")
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


@app.route("/query", methods=["GET"])
def query():
    q = request.args.get("q", "")
    return process_query(q)
