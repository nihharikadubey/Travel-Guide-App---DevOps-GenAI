from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import socket

app = Flask(__name__)

# In-memory storage for demo purposes
todos = []
visit_counter = 0

# HTML Templates
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Interactive Flask App 🚀</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .container { max-width: 800px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 10px; }
        .card { background: rgba(255,255,255,0.2); padding: 20px; margin: 15px 0; border-radius: 8px; }
        .button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .button:hover { background: #45a049; }
        input[type="text"] { padding: 10px; margin: 5px; border: none; border-radius: 5px; width: 300px; }
        .todo-item { background: rgba(255,255,255,0.3); padding: 10px; margin: 5px 0; border-radius: 5px; }
        .info { background: rgba(0,0,0,0.2); padding: 15px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Interactive Flask App in Minikube</h1>
        
        <div class="card">
            <h2>📊 App Info</h2>
            <div class="info">
                <p><strong>🏠 Hostname:</strong> {{ hostname }}</p>
                <p><strong>🕐 Current Time:</strong> {{ current_time }}</p>
                <p><strong>👥 Total Visits:</strong> {{ visits }}</p>
                <p><strong>🐍 Python Version:</strong> {{ python_version }}</p>
            </div>
        </div>

        <div class="card">
            <h2>🎲 Random Quote Generator</h2>
            <p id="quote">{{ quote }}</p>
            <button class="button" onclick="getNewQuote()">Get New Quote</button>
        </div>

        <div class="card">
            <h2>📝 Todo List</h2>
            <form method="POST" action="/add_todo">
                <input type="text" name="todo" placeholder="Enter a new todo..." required>
                <button type="submit" class="button">Add Todo</button>
            </form>
            <div id="todos">
                {% for todo in todos %}
                <div class="todo-item">
                    ✅ {{ todo.text }} 
                    <small>(Added: {{ todo.timestamp }})</small>
                    <a href="/delete_todo/{{ loop.index0 }}" style="color: #ff6b6b; text-decoration: none; float: right;">❌</a>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="card">
            <h2>🧮 Simple Calculator</h2>
            <form method="POST" action="/calculate">
                <input type="number" name="num1" placeholder="First number" required>
                <select name="operation">
                    <option value="+">+</option>
                    <option value="-">-</option>
                    <option value="*">×</option>
                    <option value="/">÷</option>
                </select>
                <input type="number" name="num2" placeholder="Second number" required>
                <button type="submit" class="button">Calculate</button>
            </form>
            {% if result %}
            <p><strong>Result:</strong> {{ result }}</p>
            {% endif %}
        </div>

        <div class="card">
            <h2>🔗 API Endpoints</h2>
            <p>Try these endpoints:</p>
            <ul>
                <li><a href="/api/status" style="color: #87CEEB;">/api/status</a> - API Status</li>
                <li><a href="/api/random" style="color: #87CEEB;">/api/random</a> - Random Number</li>
                <li><a href="/api/todos" style="color: #87CEEB;">/api/todos</a> - Todos as JSON</li>
                <li><a href="/health" style="color: #87CEEB;">/health</a> - Health Check</li>
            </ul>
        </div>
    </div>

    <script>
        function getNewQuote() {
            fetch('/api/quote')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('quote').innerHTML = data.quote;
                })
                .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
'''

QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Innovation distinguishes between a leader and a follower. - Steve Jobs",
    "Life is what happens to you while you're busy making other plans. - John Lennon",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "It is during our darkest moments that we must focus to see the light. - Aristotle",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "The way to get started is to quit talking and begin doing. - Walt Disney",
    "Don't let yesterday take up too much of today. - Will Rogers",
    "You learn more from failure than from success. Don't let it stop you. - Unknown",
    "If you are working on something that you really care about, you don't have to be pushed. - Steve Jobs"
]

@app.route('/')
def home():
    global visit_counter
    visit_counter += 1
    
    return render_template_string(HOME_TEMPLATE, 
                                hostname=socket.gethostname(),
                                current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                visits=visit_counter,
                                python_version=f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
                                quote=random.choice(QUOTES),
                                todos=todos,
                                result=None)

@app.route('/add_todo', methods=['POST'])
def add_todo():
    todo_text = request.form.get('todo')
    if todo_text:
        todos.append({
            'text': todo_text,
            'timestamp': datetime.datetime.now().strftime("%H:%M:%S")
        })
    return home()

@app.route('/delete_todo/<int:index>')
def delete_todo(index):
    if 0 <= index < len(todos):
        todos.pop(index)
    return home()

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        num1 = float(request.form.get('num1'))
        num2 = float(request.form.get('num2'))
        operation = request.form.get('operation')
        
        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                result = "Error: Division by zero!"
        else:
            result = "Error: Invalid operation!"
            
        return render_template_string(HOME_TEMPLATE, 
                                    hostname=socket.gethostname(),
                                    current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    visits=visit_counter,
                                    python_version=f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
                                    quote=random.choice(QUOTES),
                                    todos=todos,
                                    result=result)
    except ValueError:
        return render_template_string(HOME_TEMPLATE, 
                                    hostname=socket.gethostname(),
                                    current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    visits=visit_counter,
                                    python_version=f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
                                    quote=random.choice(QUOTES),
                                    todos=todos,
                                    result="Error: Invalid numbers!")

# API Endpoints
@app.route('/api/status')
def api_status():
    return jsonify({
        "status": "healthy",
        "message": "Flask app is running successfully",
        "hostname": socket.gethostname(),
        "timestamp": datetime.datetime.now().isoformat(),
        "visits": visit_counter
    })

@app.route('/api/random')
def api_random():
    return jsonify({
        "random_number": random.randint(1, 1000),
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/quote')
def api_quote():
    return jsonify({
        "quote": random.choice(QUOTES),
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/todos')
def api_todos():
    return jsonify({
        "todos": todos,
        "count": len(todos),
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "message": "Flask app is running successfully",
        "uptime": "Running in Kubernetes",
        "hostname": socket.gethostname()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
