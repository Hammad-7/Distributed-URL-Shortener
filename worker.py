import os
import json
import string
import random
from flask import Flask, request,redirect
import sys

app = Flask(__name__)
worker_storage = {}

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

def load_worker_storage():
    if os.path.exists(f"worker_storage_{sys.argv[1]}.json"):
        with open(f"worker_storage_{sys.argv[1]}.json", "r") as f:
            return json.load(f)
    return {}

def save_worker_storage():
    with open(f"worker_storage_{sys.argv[1]}.json", "w") as f:
        json.dump(worker_storage, f)

@app.route("/process_long_url", methods=["POST"])
def process_long_url():
    data = request.json
    long_url = data.get("long_url")

    short_url = generate_short_url()
    while short_url in worker_storage:
        short_url = generate_short_url()

    worker_storage[short_url] = long_url
    save_worker_storage()

    return {"short_url": short_url}

def load_shortened_urls():
    storage_file = f"worker_storage_{sys.argv[1]}.json"
    if os.path.exists(storage_file):
        with open(storage_file, "r") as f:
            return json.load(f)
    return {}

@app.route("/<short_url>")
def redirect_url(short_url):
    global worker_storage
    worker_storage = load_worker_storage()
    print(worker_storage)
    long_url = worker_storage.get(short_url, None)
    if long_url is None:
        return f"URL {short_url} doesn't exist", 404
    return redirect(long_url)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python worker.py <port>")
        sys.exit(1)
    
    port = sys.argv[1]
    worker_storage = load_worker_storage()
    app.run(debug=True, port=int(sys.argv[1]))