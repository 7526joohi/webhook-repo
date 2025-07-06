from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["github_events"]
collection = db["events"]

@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if not data:
        return jsonify({"message": "No data received"}), 400

    print(f"\n>>> Received event: {event_type}")
    print(data)

    doc = {
        "event_type": event_type,
        "timestamp": datetime.utcnow()
    }

    if event_type == "push":
        doc.update({
            "author": data.get('pusher', {}).get('name', 'unknown'),
            "to_branch": data.get('ref', '').split("/")[-1]
        })

    elif event_type == "pull_request":
        action = data.get('action')
        pr = data.get('pull_request', {})
        merged = pr.get('merged', False)

        if action in ["opened", "reopened"]:
            doc.update({
                "event_type": "pull_request",
                "author": pr.get('user', {}).get('login', 'unknown'),
                "from_branch": pr.get('head', {}).get('ref'),
                "to_branch": pr.get('base', {}).get('ref')
            })
        elif action == "closed" and merged:
            doc.update({
                "event_type": "merge",
                "author": pr.get('user', {}).get('login', 'unknown'),
                "from_branch": pr.get('head', {}).get('ref'),
                "to_branch": pr.get('base', {}).get('ref')
            })
        else:
            print(">>> ❌ Ignored PR action (not opened, reopened, or merged)")
            return jsonify({"message": "Ignored pull request action"}), 200
    else:
        print(">>> ❌ Unhandled event type")
        return jsonify({"message": "Unhandled event type"}), 200

    collection.insert_one(doc)
    print(">>> ✅ Event stored in MongoDB")
    return jsonify({"message": "Event stored"}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(10))
    return jsonify(events)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
