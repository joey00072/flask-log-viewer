from flask import Flask, render_template, request, redirect
import json
import pytz
import datetime

app = Flask(__name__)


india_timezone = pytz.timezone("Asia/Kolkata")


def convert_to_india_time(asctime):
    datetime_object = datetime.datetime.strptime(asctime, "%Y-%m-%d %H:%M:%S,%f")
    return datetime_object.astimezone(india_timezone).strftime("%d %b %Y %H:%M:%S")


@app.route("/")
def view_logs():
    with open("pybot.log", "r") as f:
        log_entries = []
        for line in f:
            try:
                log_entries.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return render_template(
        "view_logs.html",
        log_entries=log_entries[::-1],
        convert_to_india_time=convert_to_india_time,
    )


@app.route("/level/<level>")
def view_logs_by_level(level):
    with open("pybot.log", "r") as f:
        log_entries = []
        for line in f:
            try:
                entry = json.loads(line)
                if entry["level"] == level:
                    log_entries.append(entry)
            except json.JSONDecodeError:
                pass
    return render_template(
        "view_logs.html",
        log_entries=log_entries[::-1],
        convert_to_india_time=convert_to_india_time,
    )


@app.route("/level", methods=["POST"])
def filter_logs():
    level = request.form["level"]
    if level:
        return redirect(f"/level/{level}")
    else:
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5656)
