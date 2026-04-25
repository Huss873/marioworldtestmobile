# app.py
from flask import Flask, request, jsonify
import logging
import json

app = Flask(__name__)

# Configurar logging para Vercel
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/api/log', methods=['POST'])
def log_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados inválidos"}), 400
        
        # Registrar dados em logs do Vercel
        logging.info(f"Dados recebidos: {json.dumps(data)}")
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.error(f"Erro ao processar dados: {str(e)}")
        return jsonify({"error": "Erro interno"}), 500

if __name__ == '__main__':
    app.run(debug=True)
