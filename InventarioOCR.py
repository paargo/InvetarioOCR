import cv2
import pytesseract
from flask import Flask, request, jsonify
import re
import numpy as np  # Asegúrate de importar numpy

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract_info():
    # Cargar la imagen desde la solicitud
    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Preprocesar la imagen (opcional)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Otras operaciones de preprocesamiento...

    # Usar Tesseract para extraer texto
    text = pytesseract.image_to_string(gray)

    # Definir expresión regular para extraer información
    pattern = r'(?P<code>[A-Z0-9]+)\s+\$(?P<price>\d+)?\s+(?P<description>.+?)\s+\1'
    match = re.search(pattern, text)

    if match:
        return jsonify({
            'code': match.group('code'),
            'price': match.group('price') if match.group('price') else 'N/A',
            'description': match.group('description')
        })
    else:
        return jsonify({'error': 'No se encontró información válida'}), 400

if __name__ == '__main__':
    app.run(debug=True)
