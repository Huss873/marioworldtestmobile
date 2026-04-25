# app.py
from flask import Flask, request
import logging

app = Flask(__name__)

@app.route('/api/log', methods=['POST'])
def log_data():
    data = request.get_json()
    logging.info(f"Dados recebidos: {data}")
    return "Dados registrados", 200

if __name__ == '__main__':
    app.run(debug=True)
