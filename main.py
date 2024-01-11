import random
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def distribute_task(long_url):
    worker_nodes = ["http://127.0.0.1:5001/", "http://127.0.0.1:5002/"]  # Update with your worker nodes
    random_worker = random.choice(worker_nodes)
    response = requests.post(f"{random_worker}/process_long_url", json={"long_url": long_url})
    return response.json(), random_worker

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        result, worker_node = distribute_task(long_url)
        shortened_url = result.get("short_url", "Error")

        return render_template("index.html", shortened_url=f"{worker_node}{shortened_url}")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)