from flask import Flask, request, render_template_string, jsonify
from datetime import datetime

app = Flask(__name__)

# Almacenamiento en memoria (se borra si el servidor se reinicia)
webhooks_received = []

# Plantilla HTML simple integrada para no necesitar archivos extra
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Webhook Viewer</title>
    <style>
        body { font-family: sans-serif; margin: 40px; background: #f4f4f9; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
        th { background: #333; color: white; }
        tr:nth-child(even) { background: #eee; }
        .badge { padding: 5px; border-radius: 4px; background: #007bff; color: white; font-size: 0.8em; }
    </style>
</head>
<body>
    <h1>Mensajes Recibidos (Webhooks)</h1>
    <p>Total registrados: {{ messages|length }}</p>
    <table>
        <thead>
            <tr>
                <th>Fecha Registro</th>
                <th>Evento</th>
                <th>Email</th>
                <th>Asunto</th>
                <th>ID Mensaje</th>
            </tr>
        </thead>
        <tbody>
            {% for msg in messages[::-1] %}
            <tr>
                <td>{{ msg.local_ts }}</td>
                <td><span class="badge">{{ msg.event }}</span></td>
                <td>{{ msg.email }}</td>
                <td>{{ msg.subject }}</td>
                <td>{{ msg['message-id'] }}</td>
                <td>{{ msg['auth'] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    # Muestra la lista de mensajes recibidos
    return render_template_string(HTML_TEMPLATE, messages=webhooks_received)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Intentar obtener el JSON del payload
    data = request.json
    
    if data:
        # Añadimos un timestamp local para saber cuándo llegó a nuestra app
        data['local_ts'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Guardar en la lista en memoria
        webhooks_received.append(data)
        
        print(f"Webhook recibido de: {data.get('email')}")
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "No data received"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)