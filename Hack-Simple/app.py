from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)

EVENTS_FILE = 'data/events.json'
PREDICTIONS_FILE = 'data/predictions.json'

START_COINS = 100

# JSON helpers
def read_json(file):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([], f)
    with open(file, 'r') as f:
        return json.load(f)

def write_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# Helper: Get user coins
def get_user_coins(username):
    predictions = read_json(PREDICTIONS_FILE)
    coins = START_COINS
    for p in predictions:
        if p['username'] == username and p.get('won') is not None:
            if p['won']:
                coins += 10
            else:
                coins -= 5
    return coins

# Home page: show events & voting
@app.route('/')
def index():
    events = read_json(EVENTS_FILE)
    return render_template('index.html', events=events)

# Vote route
@app.route('/vote/<int:event_id>', methods=['POST'])
def vote(event_id):
    username = request.form['username'].strip()
    vote = request.form['vote']  # yes or no
    if not username:
        return "Please enter a username.", 400

    predictions = read_json(PREDICTIONS_FILE)

    # Prevent double vote on same event
    for p in predictions:
        if p['username'] == username and p['event_id'] == event_id:
            return "You already voted on this event.", 400

    predictions.append({
        "username": username,
        "event_id": event_id,
        "vote": vote,
        "won": None
    })
    write_json(PREDICTIONS_FILE, predictions)
    return redirect(url_for('index'))

# Admin sets event outcome
@app.route('/set_outcome/<int:event_id>/<outcome>')
def set_outcome(event_id, outcome):
    events = read_json(EVENTS_FILE)
    predictions = read_json(PREDICTIONS_FILE)

    # Update event
    found = False
    for event in events:
        if event['id'] == event_id:
            event['status'] = 'done'
            event['outcome'] = outcome
            found = True
            break
    if not found:
        return f"Event {event_id} not found.", 404

    # Update predictions
    for p in predictions:
        if p['event_id'] == event_id:
            p['won'] = (p['vote'] == outcome)

    write_json(EVENTS_FILE, events)
    write_json(PREDICTIONS_FILE, predictions)
    return f"Outcome for event {event_id} set to {outcome}!"

# Leaderboard page
@app.route('/leaderboard')
def leaderboard():
    predictions = read_json(PREDICTIONS_FILE)
    users = {}
    for p in predictions:
        username = p['username']
        if username not in users:
            users[username] = START_COINS
        if p.get('won') is not None:
            users[username] += 10 if p['won'] else -5
    leaderboard = sorted(users.items(), key=lambda x: x[1], reverse=True)
    return render_template('leaderboard.html', leaderboard=leaderboard)

# User history page
@app.route('/history/<username>')
def history(username):
    predictions = read_json(PREDICTIONS_FILE)
    user_preds = [p for p in predictions if p['username'] == username]
    coins = get_user_coins(username)
    return render_template('history.html', username=username, predictions=user_preds, coins=coins)

if __name__ == '__main__':
    app.run(debug=True)
