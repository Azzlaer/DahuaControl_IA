import cv2
import pytesseract
from ultralytics import YOLO
from onvif import ONVIFCamera
import configparser
import os
import logging
from datetime import datetime

# Configurar log
logging.basicConfig(
    filename="camera_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Leer configuración
config = configparser.ConfigParser()
config.read('config.ini')

IP = config['CAMARA']['ip']
USUARIO = config['CAMARA']['usuario']
PASSWORD = config['CAMARA']['password']
CANAL = config['CAMARA']['canal']

# Leer resolución
res_ancho = int(config['CAMARA'].get('resolucion_ancho', 800))
res_alto = int(config['CAMARA'].get('resolucion_alto', 600))

# Crear carpeta de imágenes
if not os.path.exists("images"):
    os.makedirs("images")

# Verificar conexión
def verificar_conexion(ip):
    try:
        cap = cv2.VideoCapture(f"rtsp://{USUARIO}:{PASSWORD}@{ip}/cam/realmonitor?channel={CANAL}&subtype=0")
        if not cap.isOpened():
            logging.error("❌ No se pudo conectar a la cámara.")
            print("❌ No se pudo conectar a la cámara.")
            return False
        cap.release()
        logging.info("✅ Conexión exitosa con la cámara.")
        print("✅ Conexión exitosa con la cámara.")
        return True
    except Exception as e:
        logging.exception(f"Error verificando conexión: {e}")
        return False

if not verificar_conexion(IP):
    exit()

# Cargar modelo YOLO
model = YOLO("yolov8n.pt")

# Iniciar cámara
cap = cv2.VideoCapture(f"rtsp://{USUARIO}:{PASSWORD}@{IP}/cam/realmonitor?channel={CANAL}&subtype=0")

while True:
    ret, frame = cap.read()
    if not ret:
        logging.warning("⚠️ No se pudo leer el frame.")
        break

    # Redimensionar a lo que dice el config.ini
    frame_resized = cv2.resize(frame, (res_ancho, res_alto))

    # Mostrar en ventana
    cv2.imshow("Vista Cámara", frame_resized)

    # Salir con Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
