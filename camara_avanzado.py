import cv2
import pytesseract
import time
import os
import configparser
from ultralytics import YOLO

# =======================
# Leer configuración INI
# =======================
config = configparser.ConfigParser()
config.read('config.ini')

ip_dvr = config['CAMARA']['ip']
usuario = config['CAMARA']['usuario']
contraseña = config['CAMARA']['password']
canal = config['CAMARA'].getint('canal', 2)
modelo_path = config['DETECCION'].get('modelo', 'yolov8n.pt')
frame_interval = config['DETECCION'].getint('frame_interval', 5)
output_folder = config['GUARDADO'].get('carpeta', 'capturas_detectadas')
res_ancho = config['VISUALIZACION'].getint('resolucion_ancho', 800)
res_alto = config['VISUALIZACION'].getint('resolucion_alto', 600)

# ========================
# Inicializaciones
# ========================
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
modelo = YOLO(modelo_path)

rtsp_url = f"rtsp://{usuario}:{contraseña}@{ip_dvr}:554/cam/realmonitor?channel={canal}&subtype=0"
os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(rtsp_url)
frame_count = 0

print("🎥 Iniciando detección en tiempo real...")

# ========================
# Bucle principal
# ========================
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ No se puede acceder al stream")
        break

    frame = cv2.resize(frame, (res_ancho, res_alto))
    frame_count += 1

    if frame_count % frame_interval == 0:
        resultados = modelo(frame)[0]

        for box in resultados.boxes:
            cls = resultados.names[int(box.cls)]
            conf = float(box.conf)

            if cls in ["car", "truck", "bus"] and conf > 0.5:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                auto = frame[y1:y2, x1:x2]

                # OCR
                patente_texto = pytesseract.image_to_string(
                    auto,
                    config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                ).strip().replace(" ", "")

                timestamp = int(time.time())
                nombre_archivo = f"{patente_texto or 'auto'}_{timestamp}.jpg"
                path = os.path.join(output_folder, nombre_archivo)
                cv2.imwrite(path, frame)

                print(f"[✓] Auto detectado - Guardado: {nombre_archivo} - Patente: {patente_texto}")

                # Dibujar cuadro y texto
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Auto: {patente_texto}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Camara Canal 2", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
