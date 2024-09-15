from flask import Flask, request, jsonify
import sqlite3
from textblob import TextBlob

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('mental_health.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS moods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT,
            strategy TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Get personalized strategies based on mood
def get_strategy(mood):
    strategies = {
        'positive': "Great! Keep it up! Try meditation to maintain your positive mood.",
        'negative': "It seems you're feeling down. Try some breathing exercises or talk to a friend.",
        'neutral': "Your mood seems neutral. How about a short walk or some light reading?"
    }
    return strategies.get(mood, "Stay strong and take care of yourself!")

# Sentiment analysis to detect mood
def detect_mood(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'

# Route to save mood and strategy
@app.route('/track_mood', methods=['POST'])
def track_mood():
    user_input = request.json.get('text')
    mood = detect_mood(user_input)
    strategy = get_strategy(mood)

    # Save to database
    conn = sqlite3.connect('mental_health.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO moods (mood, strategy) VALUES (?, ?)", (mood, strategy))
    conn.commit()
    conn.close()

    return jsonify({"mood": mood, "strategy": strategy}), 200

# Route to retrieve all moods
@app.route('/moods', methods=['GET'])
def get_moods():
    conn = sqlite3.connect('mental_health.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM moods")
    moods = cursor.fetchall()
    conn.close()

    return jsonify(moods), 200

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
