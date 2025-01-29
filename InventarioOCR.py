import cv2
import pytesseract
from flask import Flask, request, jsonify
import numpy as np
import re

# Configuración de Flask
app = Flask(__name__)

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Asegúrate de tener la ruta correcta

# Cargar el modelo YOLO
net = cv2.dnn.readNet("C:/Users/Pablo/darknet/cfg/yolov3.weights", "C:/Users/Pablo/darknet/cfg/yolov3.cfg")  # Rutas de los archivos de YOLO
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Cargar las clases (si tienes un archivo .names con los objetos, debes cargarlo aquí)
# Al ser una POC con una etiqueta, tal vez no necesites clases predefinidas, pero podrías definir "label" o "tag"
# con un archivo .names si tienes etiquetas específicas.
# classes = open("coco.names").read().strip().split("\n")  # Si tienes un archivo .names

@app.route('/extract_code', methods=['POST'])
def extract_code():
    # Cargar la imagen desde la solicitud
    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # 1. Usar YOLO para detectar la etiqueta
    height, width, channels = image.shape
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Filtramos las detecciones (usamos el umbral de confianza para detectar la etiqueta)
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  # Filtro de confianza para detectar etiquetas
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Aplicamos Non-maxima suppression para eliminar las detecciones redundantes
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Si se detectó una caja que contiene la etiqueta, recortamos la imagen
    if len(indexes) > 0:
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label_img = image[y:y + h, x:x + w]  # Recortar la etiqueta detectada

                # 2. Preprocesamiento de la imagen recortada (etiqueta detectada)
                gray = cv2.cvtColor(label_img, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                _, thresh = cv2.threshold(blurred, 160, 255, cv2.THRESH_BINARY_INV)

                # 3. OCR para extraer el código de la etiqueta
                custom_config = "--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$-"
                extracted_text = pytesseract.image_to_string(thresh, config=custom_config)

                # 4. Filtrar solo el código con expresiones regulares
                pattern = r'([A-Z0-9]+[-$]?[A-Z0-9]+)'
                match = re.search(pattern, extracted_text)

                if match:
                    return jsonify({'code': match.group(0)})

    return jsonify({'error': 'No se encontró un código válido'}), 400

if __name__ == '__main__':
    app.run(debug=True)
