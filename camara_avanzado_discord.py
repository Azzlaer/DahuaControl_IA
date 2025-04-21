import cv2
import pytesseract
import time
import os
from ultralytics import YOLO
import requests
from configparser import ConfigParser

# Ruta a tesseract (ajústala según tu instalación)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Cargar configuraciones desde config.ini
config = ConfigParser()
config.read('config.ini')

# Configuración de la cámara
usuario = config.get('CAMARA', 'usuario')
contraseña = config.get('CAMARA', 'password')
ip_dvr = config.get('CAMARA', 'ip')
canal = config.get('CAMARA', 'canal')
rtsp_url = f"rtsp://{usuario}:{contraseña}@{ip_dvr}:554/cam/realmonitor?channel={canal}&subtype=0"

# Modelo YOLOv8 preentrenado (automóviles)
modelo_path = config.get('DETECCION', 'modelo')
modelo = YOLO(modelo_path)

# Configuración de la carpeta de guardado
output_folder = config.get('GUARDADO', 'carpeta')
os.makedirs(output_folder, exist_ok=True)

# Configuración de la visualización
resolucion_ancho = int(config.get('VISUALIZACION', 'resolucion_ancho'))
resolucion_alto = int(config.get('VISUALIZACION', 'resolucion_alto'))

# Función para enviar notificaciones a Discord
def enviar_webhook_discord(mensaje, imagen_path=None):
    url = config.get('DISCORD', 'webhook_url', fallback=None)
    notificaciones_activadas = config.getboolean('DISCORD', 'notificaciones', fallback=True)
    subir_imagen = config.getboolean('DISCORD', 'subir_imagen', fallback=True)

    if not url or not notificaciones_activadas:
        return

    data = {
        "content": mensaje
    }

    files = None
    if subir_imagen and imagen_path and os.path.exists(imagen_path):
        files = {
            "file": open(imagen_path, "rb")
        }

    try:
        response = requests.post(url, data=data, files=files)
        if response.status_code != 204:
            print(f"[!] Error al enviar a Discord: {response.status_code} - {response.text}")
        else:
            print("[✓] Notificación enviada a Discord")
    except Exception as e:
        print(f"[✗] Falló el envío del webhook: {e}")

# Configuración de la cámara PTZ
habilitar_ptz = config.getboolean('PTZ', 'habilitar', fallback=False)

cap = cv2.VideoCapture(rtsp_url)
frame_count = 0

# Configuración del intervalo de frames para procesamiento
frame_interval = int(config.get('DETECCION', 'frame_interval', fallback=5))

print("Iniciando detección en tiempo real...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se puede acceder al stream")
        break

    # Cambiar la resolución de visualización
    frame = cv2.resize(frame, (resolucion_ancho, resolucion_alto))

    frame_count += 1

    if frame_count % frame_interval == 0:  # procesa 1 de cada 'frame_interval' frames para no saturar
        resultados = modelo(frame)[0]

        for box in resultados.boxes:
            cls = resultados.names[int(box.cls)]
            conf = float(box.conf)

            if cls in ["car", "truck", "bus"] and conf > 0.5:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                auto = frame[y1:y2, x1:x2]

                # OCR sobre posible patente (puedes mejorar este paso con crop más preciso)
                patente_texto = pytesseract.image_to_string(auto, config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                patente_texto = patente_texto.strip().replace(" ", "")

                # Guardar imagen
                timestamp = int(time.time())
                nombre_archivo = f"{patente_texto or 'auto'}_{timestamp}.jpg"
                path = os.path.join(output_folder, nombre_archivo)
                cv2.imwrite(path, frame)
                print(f"[✓] Auto detectado - Guardado: {nombre_archivo} - Patente: {patente_texto}")

                # Dibujar cuadro y texto
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Auto: {patente_texto}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # Enviar notificación a Discord
                enviar_webhook_discord(
                    mensaje=f"🚗 Auto detectado\nPatente: {patente_texto}\nArchivo: {nombre_archivo}",
                    imagen_path=path
                )

                # Si el PTZ está habilitado, mover la cámara (esto es solo un ejemplo y se debe adaptar al controlador ONVIF)
                if habilitar_ptz:
                    print("[✓] Mover cámara PTZ")
                    # Aquí iría el código para mover la cámara PTZ si fuera necesario, utilizando la API ONVIF.

    # Mostrar video en vivo
    cv2.imshow("Camara Canal 2", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
