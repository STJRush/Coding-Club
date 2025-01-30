# voting_site.py
# A Flask app for knowledge-based voting.
# Each user can earn 0–10 votes based on quiz performance.
# Admin can create/edit topics and quizzes. Users can take quizzes and vote.
# Uses CSV for data. Python 3 + Flask.
#
# Now, we load "users.csv" for credentials
# (username, password, role) instead of hardcoding users in a dictionary.

import csv
import json
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secretkey'

# Path to CSV for storing topics
TOPICS_CSV = 'topics.csv'
# Path to CSV for storing users
USERS_CSV = 'users.csv'

# We'll store the topics and users in memory after loading.
# 'topics' is loaded from topics.csv, 'users' from users.csv
users = {}
topics = []

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
        pass
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
# User CSV helper
# ---------------------------

def load_users():
    """
    Load users from USERS_CSV into a dictionary:
    {
      'username1': {'password': '...', 'role': '...'},
      'username2': {'password': '...', 'role': '...'},
      ...
    }
    """
    loaded = {}
    try:
        with open(USERS_CSV, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                username = row.get('username')
                password = row.get('password')
                role = row.get('role')
                if username:
                    loaded[username] = {
                        'password': password,
                        'role': role
                    }
                print(reader)
    except FileNotFoundError:
        pass
    return loaded

# ---------------------------
# Helpers
# ---------------------------

def get_current_user():
    # uses the global 'users' dict
    if 'username' in session:
        username = session['username']
        if username in users:
            return {'username': username, 'role': users[username]['role']}
    return None

def is_admin():
    cu = get_current_user()
    return (cu and cu['role'] == 'admin')

def calculate_votes_from_score(score, total):
    if total == 0:
        return 0
    percentage = (score / total) * 100
    return int(round((percentage / 100) * 10))

# ---------------------------
# Routes for authentication
# ---------------------------

@app.route('/')
def home():
    global topics
    current_user = get_current_user()
    topics = load_topics()
    return render_template_string(index_html, user=current_user, topics=topics)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Check credentials in our loaded 'users' dict
        if username in users and users[username]['password'] == password:
            session['username'] = username
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
                'votes': {'Yes': 0, 'No': 0, 'voted_users': []}
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

    if 'voted_users' not in topic['votes']:
        topic['votes']['voted_users'] = []
        save_topics(topics)

    user_best = 0
    if current_user and 'scores' in session:
        user_scores = session['scores']
        user_best = user_scores.get(str(topic_id), 0)

    user_has_voted = False
    if current_user:
        user_has_voted = (current_user['username'] in topic['votes']['voted_users'])

    return render_template_string(topic_html,
                                  topic=topic,
                                  user=current_user,
                                  user_best=user_best,
                                  user_has_voted=user_has_voted)

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
        if 'scores' not in session:
            session['scores'] = {}
        user_scores = session['scores']
        best_so_far = user_scores.get(str(topic_id), 0)
        if votes_earned > best_so_far:
            user_scores[str(topic_id)] = votes_earned
        session['scores'] = user_scores

        return render_template_string(quiz_result_html,
                                      topic=topic,
                                      score=score,
                                      total=total,
                                      votes_earned=votes_earned)
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

    if 'voted_users' not in topic['votes']:
        topic['votes']['voted_users'] = []

    if current_user['username'] in topic['votes']['voted_users']:
        return "You have already voted on this topic!"

    choice = request.form.get('choice')
    if choice not in ['Yes', 'No']:
        return 'Invalid choice'

    votes_to_cast = 0
    if 'scores' in session:
        user_scores = session['scores']
        votes_to_cast = user_scores.get(str(topic_id), 0)

    topic['votes'][choice] += votes_to_cast
    topic['votes']['voted_users'].append(current_user['username'])

    save_topics(topics)
    return redirect(url_for('view_topic', topic_id=topic_id))

# ---------------------------
# HTML Templates (inline)
# ---------------------------
# Tailwind used for styling + minor animations
# user_best is displayed on the topic page next to "Votes to cast".
# user_has_voted is used to disable or hide the vote form if they've already voted.

index_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Knowledge-Based Voting</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
      .fade-in {
        animation: fadeIn 0.7s ease-in forwards;
        opacity: 0;
      }
      @keyframes fadeIn {
        to { opacity: 1; }
      }
      .btn-animate {
        transition: transform 0.2s ease;
      }
      .btn-animate:hover {
        transform: scale(1.05);
      }
    </style>
  </head>
  <body class="bg-gray-100 text-gray-800 p-4">
    <div class="max-w-3xl mx-auto bg-white shadow-lg p-6 rounded-lg fade-in">
      <h1 class="text-2xl font-bold mb-4">Welcome to the Voting Site</h1>
      {% if user %}
        <p>Logged in as <span class="font-semibold">{{ user.username }}</span> (role: {{ user.role }})</p>
        <p class="my-2"><a class="text-blue-600 underline" href="{{ url_for('logout') }}">Logout</a></p>
        <h2 class="text-xl mt-4 mb-2">Available Topics</h2>
        <ul class="list-disc list-inside">
          {% for t in topics %}
            <li>
              <a class="text-blue-600 underline" href="{{ url_for('view_topic', topic_id=t.id) }}">
                {{ t.title }}
              </a>
            </li>
          {% endfor %}
        </ul>
        {% if user.role == 'admin' %}
          <a class="inline-block bg-blue-500 text-white px-4 py-2 mt-4 rounded btn-animate" href="{{ url_for('admin_page') }}">
            Admin Page
          </a>
        {% endif %}
      {% else %}
        <p><a class="text-blue-600 underline" href="{{ url_for('login') }}">Login</a></p>
      {% endif %}
    </div>
  </body>
</html>
"""

login_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body class="bg-gray-100 text-gray-800 p-4">
    <div class="max-w-md mx-auto bg-white shadow-lg p-6 rounded-lg">
      <h1 class="text-2xl font-bold mb-4">Login</h1>
      {% if error %}
        <p class="text-red-500">{{ error }}</p>
      {% endif %}
      <form method="post" action="" class="space-y-4">
        <div>
          <label class="block font-semibold">Username:</label>
          <input type="text" name="username" class="border p-2 w-full"/>
        </div>
        <div>
          <label class="block font-semibold">Password:</label>
          <input type="password" name="password" class="border p-2 w-full"/>
        </div>
        <input class="bg-blue-500 text-white px-4 py-2 rounded btn-animate" type="submit" value="Login"/>
      </form>
    </div>
  </body>
</html>
"""

admin_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Admin Page</title>
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body class="bg-gray-100 text-gray-800 p-4">
    <div class="max-w-3xl mx-auto bg-white shadow-lg p-6 rounded-lg">
      <h1 class="text-2xl font-bold mb-4">Admin Panel</h1>
      <p><a class="text-blue-600 underline" href="{{ url_for('home') }}">Home</a></p>
      <h2 class="text-xl mt-4 mb-2">Create Topic</h2>
      <p>
        <a class="inline-block bg-blue-500 text-white px-4 py-2 rounded btn-animate" href="{{ url_for('create_topic') }}">
          Create a new topic
        </a>
      </p>
      <h2 class="text-xl mt-4 mb-2">Existing Topics</h2>
      <ul class="list-disc list-inside">
        {% for t in topics %}
          <li>
            {{ t.title }} -
            <a class="text-blue-600 underline" href="{{ url_for('edit_quiz', topic_id=t.id) }}">Edit Quiz</a>
          </li>
        {% endfor %}
      </ul>
    </div>
  </body>
</html>
"""

create_topic_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Create Topic</title>
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body class="bg-gray-100 text-gray-800 p-4">
    <div class="max-w-md mx-auto bg-white shadow-lg p-6 rounded-lg">
      <h1 class="text-2xl font-bold mb-4">Create a New Topic</h1>
      <form method="post" action="" class="space-y-4">
        <div>
          <label class="block font-semibold">Title:</label>
          <input type="text" name="title" class="border p-2 w-full"/>
        </div>
        <input class="bg-blue-500 text-white px-4 py-2 rounded btn-animate" type="submit" value="Create"/>
      </form>
    </div>
  </body>
</html>
"""

edit_quiz_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Edit Quiz</title>
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body class="bg-gray-100 text-gray-800 p-4">
    <div class="max-w-3xl mx-auto bg-white shadow-lg p-6 rounded-lg">
      <h1 class="text-2xl font-bold mb-4">Edit Quiz for {{ topic.title }}</h1>
      <p>
        <a class="text-blue-600 underline" href="{{ url_for('admin_page') }}">Back to Admin Page</a>
      </p>
      <h2 class="text-xl mt-4 mb-2">Current Questions</h2>
      <ol class="list-decimal list-inside">
        {% for q in topic.quiz %}
        <li class="mb-2">
          <strong>{{ q.question }}</strong><br>
          Choices: {{ q.choices }} <br>
          Correct index: {{ q.correct_index }}
        </li>
        {% endfor %}
      </ol>
      <h2 class="text-xl mt-4 mb-2">Add a New Question</h2>
      <form method="post" action="" class="space-y-4">
        <div>
          <label class="block font-semibold">Question:</label>
          <input type="text" name="question" class="border p-2 w-full"/>
        </div>
        <div>
          <label class="block font-semibold">Choice 1:</label>
          <input type="text" name="choice1" class="border p-2 w-full"/>
        </div>
        <div>
          <label class="block font-semibold">Choice 2:</label>
          <input type="text" name="choice2" class="border p-2 w-full"/>
        </div>
        <div>
          <label class="block font-semibold">Choice 3:</label>
          <input type="text" name="choice3" class="border p-2 w-full"/>
        </div>
        <div>
          <label class="block font-semibold">Choice 4:</label>
          <input type="text" name="choice4" class="border p-2 w-full"/>
        </div>
        <div>
          <label class="block font-semibold">Correct Choice Index (0-3):</label>
          <input type="text" name="correct_index" class="border p-2 w-full"/>
        </div>
        <input class="bg-blue-500 text-white px-4 py-2 rounded btn-animate" type="submit" value="Add Question"/>
      </form>
    </div>
  </body>
</html>
"""

topic_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>{{ topic.title }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
      .btn-animate {
        transition: transform 0.2s ease;
      }
      .btn-animate:hover {
        transform: scale(1.05);
      }
    </style>
  </head>
  <body class="bg-gray-100 text-gray-800 p-4">
    <div class="max-w-3xl mx-auto bg-white shadow-lg p-6 rounded-lg">
      <h1 class="text-2xl font-bold mb-4">{{ topic.title }}</h1>
      <p><a class="text-blue-600 underline" href="{{ url_for('home') }}">Home</a></p>

      <h2 class="text-xl mt-4 mb-2">Current Vote Results</h2>
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
              backgroundColor: [
                'rgba(75, 192, 192, 0.2)',
                'rgba(255, 99, 132, 0.2)'
              ],
              borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(255, 99, 132, 1)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: { beginAtZero: true }
            }
          }
        });
      </script>

      {% if user %}
        <div class="mt-6">
          <h2 class="text-xl font-semibold">Take the Quiz</h2>
          <a class="inline-block bg-blue-500 text-white px-4 py-2 mt-2 rounded btn-animate"
             href="{{ url_for('take_quiz', topic_id=topic.id) }}">
            Go to Quiz
          </a>
        </div>
        <div class="mt-6">
          <h2 class="text-xl font-semibold">Vote</h2>
          {% if user_has_voted %}
            <p class="text-green-600 mt-2">You have already voted on this topic!</p>
          {% else %}
            <form method="post" action="{{ url_for('cast_vote', topic_id=topic.id) }}" class="mt-2">
              <label class="block mb-2">Choose your vote:</label>
              <select name="choice" class="border p-2 rounded">
                <option value="Yes">Yes</option>
                <option value="No">No</option>
              </select>
              <br><br>
              <p class="text-gray-700">
                Votes to cast (your best quiz result):
                <span class="font-bold">{{ user_best }}</span>
              </p>
              <button class="bg-blue-500 text-white px-4 py-2 mt-2 rounded btn-animate" type="submit">
                Submit Vote
              </button>
            </form>
          {% endif %}
        </div>
      {% else %}
        <p class="mt-4">
          You must
          <a class="text-blue-600 underline" href="{{ url_for('login') }}">login</a>
          to vote.
        </p>
      {% endif %}
    </div>
  </body>
</html>
"""

take_quiz_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Take Quiz</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
      .btn-animate {
        transition: transform 0.2s ease;
      }
      .btn-animate:hover {
        transform: scale(1.05);
      }
    </style>
  </head>
  <body class="bg-gray-100 text-gray-800 p-4">
    <div class="max-w-3xl mx-auto bg-white shadow-lg p-6 rounded-lg">
      <h1 class="text-2xl font-bold mb-4">Quiz for {{ topic.title }}</h1>
      <p>
        <a class="text-blue-600 underline" href="{{ url_for('view_topic', topic_id=topic.id) }}">
          Back to Topic
        </a>
      </p>
      <form method="post" action="" class="mt-4">
        {% for i in range(topic.quiz|length) %}
          {% set q = topic.quiz[i] %}
          <div class="mb-4">
            <p class="font-semibold">Question {{ i + 1 }}: {{ q.question }}</p>
            {% for j in range(q.choices|length) %}
              <label class="block">
                <input type="radio" name="q{{ i }}" value="{{ j }}" class="mr-2">
                {{ q.choices[j] }}
              </label>
            {% endfor %}
          </div>
        {% endfor %}
        <button class="bg-blue-500 text-white px-4 py-2 rounded btn-animate" type="submit">
          Submit Quiz
        </button>
      </form>
    </div>
  </body>
</html>
"""

quiz_result_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Quiz Results</title>
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body class="bg-gray-100 text-gray-800 p-4">
    <div class="max-w-md mx-auto bg-white shadow-lg p-6 rounded-lg">
      <h1 class="text-2xl font-bold mb-4">Quiz Results for {{ topic.title }}</h1>
      <p>
        Your Score:
        <span class="font-semibold">{{ score }}/{{ total }}</span>
      </p>
      <p>
        You earned
        <span class="font-semibold">{{ votes_earned }}</span>
        votes based on your quiz performance.
      </p>
      <p class="mt-2">
        (We automatically keep your best quiz result for voting.)
      </p>
      <p class="mt-4">
        <a class="text-blue-600 underline" href="{{ url_for('view_topic', topic_id=topic.id) }}">
          Back to Topic
        </a>
      </p>
    </div>
  </body>
</html>
"""

if __name__ == '__main__':
    # Load users from CSV
    users = load_users()
    # Load topics from CSV
    topics = load_topics()

    # If CSV is empty, add a sample topic
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
            # Initialize 'voted_users' to block repeat votes
            'votes': {'Yes': 0, 'No': 0, 'voted_users': []}
        }
        topics.append(sample_topic)
        save_topics(topics)

    print('Starting server on http://127.0.0.1:5000/')
    app.run(debug=True)
