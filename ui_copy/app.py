from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get')
def get_bot_response():
    userText = request.args.get('msg')
    # Here, you can add your chatbot logic to generate a response and a timestamp
    response_text = f"You said: {userText}"
    timestamp = 10  # Example timestamp; replace with actual logic to determine the time
    response = {
        "response": response_text,
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
