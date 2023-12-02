import os
from flask import Flask, render_template, request
from bot import process_input

app = Flask(__name__)

port = os.getenv("PORT")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = process_input(userText)
    return str(response)

if __name__ == "__main__":
    # If the app is running locally
	if port is None:
    # Use port 5000
		app.run(host='0.0.0.0', port=3000, debug=True)
	else:
    # Else use cloud foundry default port
		app.run(host='0.0.0.0', port=int(port), debug=True)