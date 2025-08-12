from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Flask in Minikube! 🚀"

@app.route('/health')
def health():
    return {"status": "healthy", "message": "Flask app is running successfully"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)