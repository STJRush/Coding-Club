# voting_site.py
# A simple Flask app demonstrating knowledge-based voting.
# Each user can earn from 0 to 10 votes based on quiz performance.
# Admin can create/edit topics and quizzes. Users can take quizzes and vote.
# Modified to store topics data in a CSV file.
# Updated for Python 3, ensuring:
#   - Correct child loop indexing so correct quiz answers are recognized.
#   - Each user's best quiz result is stored in session (scores).
#   - The user automatically uses their best quiz-based votes, not a manual input.

import csv
import json
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secretkey'

# Path to our CSV file for storing topics.
TOPICS_CSV = 'topics.csv'

users = {
    'admin': {'password': 'admin', 'role': 'admin'},
    'user': {'password': 'user', 'role': 'user'}
}

# We'll keep a global in-memory list of topics, but read/write them from CSV.
topics = []  # Each element is a dict with: id, title, quiz, votes

# ---------------------------
# CSV helper functions
# ---------------------------

def load_topics():
    loaded_topics = []
    try:
        with open(TOPICS_CSV, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                loaded_topics.append({
                    'id': int(row['id']),
                    'title': row['title'],
                    'quiz': json.loads(row['quiz']),
                    'votes': json.loads(row['votes'])
                })
    except FileNotFoundError:
        pass  # If no file yet, just return an empty list.
    return loaded_topics

def save_topics(topics_list):
    with open(TOPICS_CSV, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['id', 'title', 'quiz', 'votes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in topics_list:
            writer.writerow({
                'id': t['id'],
                'title': t['title'],
                'quiz': json.dumps(t['quiz']),
                'votes': json.dumps(t['votes'])
            })

# ---------------------------
# Helper Functions
# ---------------------------

def get_current_user():
    if 'username' in session:
        username = session['username']
        if username in users:
            return {'username': username, 'role': users[username]['role']}
    return None

def is_admin():
    current_user = get_current_user()
    return (current_user and current_user['role'] == 'admin')

def calculate_votes_from_score(score, total):
    # Convert quiz score to 0-10 votes
    if total == 0:
        return 0
    percentage = (score / total) * 100
    votes = int(round((percentage / 100) * 10))
    return votes

# ---------------------------
# Routes for authentication
# ---------------------------

@app.route('/')
def home():
    global topics
    current_user = get_current_user()
    topics = load_topics()  # Refresh from CSV
    # Pass 'topics' to template so the user sees the available topics
    if current_user:
        return render_template_string(index_html, user=current_user, topics=topics)
    else:
        return render_template_string(index_html, user=None, topics=topics)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username]['password'] == password:
            session['username'] = username
            # Create or confirm a place to track each user's best quiz scores
            if 'scores' not in session:
                session['scores'] = {}
            return redirect(url_for('home'))
        else:
            return render_template_string(login_html, error='Invalid credentials')
    return render_template_string(login_html, error=None)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# ---------------------------
# Admin routes
# ---------------------------

@app.route('/admin')
def admin_page():
    global topics
    if not is_admin():
        return 'Access denied'
    topics = load_topics()
    return render_template_string(admin_html, topics=topics)

@app.route('/admin/create_topic', methods=['GET', 'POST'])
def create_topic():
    global topics
    if not is_admin():
        return 'Access denied'
    topics = load_topics()
    if request.method == 'POST':
        title = request.form.get('title')
        if title:
            new_id = len(topics)
            topics.append({
                'id': new_id,
                'title': title,
                'quiz': [],
                'votes': {'Yes': 0, 'No': 0}
            })
            save_topics(topics)
            return redirect(url_for('admin_page'))
    return render_template_string(create_topic_html)

@app.route('/admin/edit_quiz/<int:topic_id>', methods=['GET', 'POST'])
def edit_quiz(topic_id):
    global topics
    if not is_admin():
        return 'Access denied'

    topics = load_topics()
    topic = next((t for t in topics if t['id'] == topic_id), None)
    if not topic:
        return 'Topic not found'

    if request.method == 'POST':
        question = request.form.get('question')
        choice1 = request.form.get('choice1')
        choice2 = request.form.get('choice2')
        choice3 = request.form.get('choice3')
        choice4 = request.form.get('choice4')
        correct_index = request.form.get('correct_index')
        try:
            correct_index = int(correct_index)
        except:
            correct_index = 0
        if question and choice1 and choice2 and choice3 and choice4:
            new_question = {
                'question': question,
                'choices': [choice1, choice2, choice3, choice4],
                'correct_index': correct_index
            }
            topic['quiz'].append(new_question)
        save_topics(topics)
        return redirect(url_for('edit_quiz', topic_id=topic_id))

    return render_template_string(edit_quiz_html, topic=topic)

# ---------------------------
# User routes
# ---------------------------

@app.route('/topic/<int:topic_id>')
def view_topic(topic_id):
    global topics
    topics = load_topics()
    topic = next((t for t in topics if t['id'] == topic_id), None)
    if not topic:
        return 'Topic not found'
    current_user = get_current_user()
    return render_template_string(topic_html, topic=topic, user=current_user)

@app.route('/topic/<int:topic_id>/quiz', methods=['GET', 'POST'])
def take_quiz(topic_id):
    global topics
    topics = load_topics()
    topic = next((t for t in topics if t['id'] == topic_id), None)
    if not topic:
        return 'Topic not found'
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        answers = request.form
        score = 0
        total = len(topic['quiz'])
        for i, question in enumerate(topic['quiz']):
            chosen = answers.get('q' + str(i))
            if chosen is not None:
                chosen_index = int(chosen)
                if chosen_index == question['correct_index']:
                    score += 1
        votes_earned = calculate_votes_from_score(score, total)

        # Store best quiz result in session, so user can't override
        if 'scores' not in session:
            session['scores'] = {}
        user_scores = session['scores']
        topic_key = str(topic_id)
        current_best = user_scores.get(topic_key, 0)
        if votes_earned > current_best:
            user_scores[topic_key] = votes_earned
        session['scores'] = user_scores

        return render_template_string(quiz_result_html, topic=topic, score=score, total=total, votes_earned=votes_earned)

    return render_template_string(take_quiz_html, topic=topic)

@app.route('/topic/<int:topic_id>/vote', methods=['POST'])
def cast_vote(topic_id):
    global topics
    topics = load_topics()
    topic = next((t for t in topics if t['id'] == topic_id), None)
    if not topic:
        return 'Topic not found'
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))

    choice = request.form.get('choice')  # 'Yes' or 'No'

    # Retrieve best quiz-based votes from session
    votes_to_cast = 0
    if 'scores' in session:
        user_scores = session['scores']
        topic_key = str(topic_id)
        votes_to_cast = user_scores.get(topic_key, 0)

    if choice not in ['Yes', 'No']:
        return 'Invalid choice'

    topic['votes'][choice] += votes_to_cast
    save_topics(topics)

    return redirect(url_for('view_topic', topic_id=topic_id))

# ---------------------------
# HTML Templates
# ---------------------------

index_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Knowledge-Based Voting</title>
  </head>
  <body>
    <h1>Welcome to the Voting Site</h1>
    {% if user %}
      <p>Logged in as {{ user.username }}</p>
      <p>Role: {{ user.role }}</p>
      <p><a href="{{ url_for('logout') }}">Logout</a></p>
      <h2>Available Topics</h2>
      <ul>
        {% for t in topics %}
          <li><a href="{{ url_for('view_topic', topic_id=t.id) }}">{{ t.title }}</a></li>
        {% endfor %}
      </ul>
      {% if user.role == 'admin' %}
        <a href="{{ url_for('admin_page') }}">Admin Page</a>
      {% endif %}
    {% else %}
      <p><a href="{{ url_for('login') }}">Login</a></p>
    {% endif %}
  </body>
</html>
"""

login_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Login</title>
  </head>
  <body>
    <h1>Login</h1>
    {% if error %}
      <p style='color:red;'>{{ error }}</p>
    {% endif %}
    <form method="post" action="">
      <label>Username: <input type="text" name="username"></label><br>
      <label>Password: <input type="password" name="password"></label><br>
      <input type="submit" value="Login">
    </form>
  </body>
</html>
"""

admin_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Admin Page</title>
  </head>
  <body>
    <h1>Admin Panel</h1>
    <p><a href="{{ url_for('home') }}">Home</a></p>
    <h2>Create Topic</h2>
    <p><a href="{{ url_for('create_topic') }}">Create a new topic</a></p>
    <h2>Existing Topics</h2>
    <ul>
      {% for t in topics %}
        <li>{{ t.title }} - <a href="{{ url_for('edit_quiz', topic_id=t.id) }}">Edit Quiz</a></li>
      {% endfor %}
    </ul>
  </body>
</html>
"""

create_topic_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Create Topic</title>
  </head>
  <body>
    <h1>Create a New Topic</h1>
    <form method="post" action="">
      <label>Title: <input type="text" name="title"></label><br><br>
      <input type="submit" value="Create">
    </form>
  </body>
</html>
"""

edit_quiz_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Edit Quiz</title>
  </head>
  <body>
    <h1>Edit Quiz for {{ topic.title }}</h1>
    <p><a href="{{ url_for('admin_page') }}">Back to Admin Page</a></p>
    <h2>Current Questions</h2>
    <ol>
      {% for q in topic.quiz %}
      <li>
        {{ q.question }} <br>
        Choices: {{ q.choices }} <br>
        Correct index: {{ q.correct_index }}
      </li>
      {% endfor %}
    </ol>
    <h2>Add a New Question</h2>
    <form method="post" action="">
      <label>Question: <input type="text" name="question"></label><br><br>
      <label>Choice 1: <input type="text" name="choice1"></label><br>
      <label>Choice 2: <input type="text" name="choice2"></label><br>
      <label>Choice 3: <input type="text" name="choice3"></label><br>
      <label>Choice 4: <input type="text" name="choice4"></label><br>
      <label>Correct Choice Index (0-3): <input type="text" name="correct_index"></label><br><br>
      <input type="submit" value="Add Question">
    </form>
  </body>
</html>
"""

topic_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>{{ topic.title }}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  </head>
  <body>
    <h1>{{ topic.title }}</h1>
    <p><a href="{{ url_for('home') }}">Home</a></p>

    <h2>Current Vote Results</h2>
    <canvas id="resultsChart" width="400" height="200"></canvas>
    <script>
      var ctx = document.getElementById('resultsChart').getContext('2d');
      var resultsChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Yes', 'No'],
          datasets: [{
            label: 'Votes',
            data: [{{ topic.votes['Yes'] }}, {{ topic.votes['No'] }}],
            backgroundColor: ['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)'],
            borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)'],
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    </script>

    {% if user %}
      <h2>Take the Quiz</h2>
      <p><a href="{{ url_for('take_quiz', topic_id=topic.id) }}">Go to Quiz</a></p>

      <h2>Vote</h2>
      <form method="post" action="{{ url_for('cast_vote', topic_id=topic.id) }}">
        <label>Choose your vote: </label>
        <select name="choice">
          <option value="Yes">Yes</option>
          <option value="No">No</option>
        </select><br><br>
        <p>Votes to cast: (Automatically uses your best quiz result.)</p>
        <input type="submit" value="Submit Vote">
      </form>
    {% else %}
      <p>You must <a href="{{ url_for('login') }}">login</a> to vote.</p>
    {% endif %}
  </body>
</html>
"""

take_quiz_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Take Quiz</title>
  </head>
  <body>
    <h1>Quiz for {{ topic.title }}</h1>
    <p><a href="{{ url_for('view_topic', topic_id=topic.id) }}">Back to Topic</a></p>
    <form method="post" action="">
      {% for i in range(topic.quiz|length) %}
        {% set q = topic.quiz[i] %}
        <div>
          <p>Question {{ i + 1 }}: {{ q.question }}</p>
          {% for j in range(q.choices|length) %}
            <label>
              <input type="radio" name="q{{ i }}" value="{{ j }}">
              {{ q.choices[j] }}
            </label><br>
          {% endfor %}
        </div>
        <br>
      {% endfor %}
      <input type="submit" value="Submit Quiz">
    </form>
  </body>
</html>
"""



quiz_result_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Quiz Results</title>
  </head>
  <body>
    <h1>Quiz Results for {{ topic.title }}</h1>
    <p>Your Score: {{ score }} / {{ total }}</p>
    <p>You earned {{ votes_earned }} votes based on your quiz performance.</p>
    <p>(We automatically keep your best quiz result for voting.)</p>
    <p><a href="{{ url_for('view_topic', topic_id=topic.id) }}">Back to Topic</a></p>
  </body>
</html>
"""

if __name__ == '__main__':
    topics = load_topics()

    # If CSV was empty, add a sample topic for demonstration
    if not topics:
        sample_topic = {
            'id': 0,
            'title': 'Should we have a uniform?',
            'quiz': [
                {
                    'question': 'Which is a common reason for uniforms?',
                    'choices': ['Fashion statement', 'School identity', 'Personal choice', 'Holiday wear'],
                    'correct_index': 1
                },
                {
                    'question': 'Uniforms are often said to promote...',
                    'choices': ['Distraction in class', 'Bullying', 'Equality', 'Higher costs'],
                    'correct_index': 2
                }
            ],
            'votes': {'Yes': 0, 'No': 0}
        }
        topics.append(sample_topic)
        save_topics(topics)

    print('Starting server on http://127.0.0.1:5000/')
    app.run(debug=True)
