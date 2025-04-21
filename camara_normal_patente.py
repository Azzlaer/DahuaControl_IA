import cv2
import pytesseract
import time
import os
from ultralytics import YOLO

# Ruta a tesseract (ajústala según tu instalación)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Modelo YOLOv8 preentrenado (automóviles)
modelo = YOLO('yolov8n.pt')  # puedes usar yolov8m.pt para más precisión

# Configura tu DVR
usuario = "teclado"
contraseña = "123456teclado"
ip_dvr = "192.168.0.4"
rtsp_url = f"rtsp://{usuario}:{contraseña}@{ip_dvr}:554/cam/realmonitor?channel=2&subtype=0"

# Carpeta de guardado
output_folder = "capturas_detectadas"
os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(rtsp_url)
frame_count = 0

print("Iniciando detección en tiempo real...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se puede acceder al stream")
        break

    frame_count += 1

    if frame_count % 5 == 0:  # procesa 1 de cada 5 frames para no saturar
        resultados = modelo(frame)[0]

        for box in resultados.boxes:
            cls = resultados.names[int(box.cls)]
            conf = float(box.conf)

            if cls in ["car", "truck", "bus"] and conf > 0.5:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                auto = frame[y1:y2, x1:x2]

                # OCR sobre posible patente (solo caracteres alfanuméricos)
                patente_texto = pytesseract.image_to_string(auto, config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                patente_texto = patente_texto.strip().replace(" ", "")

                # Asegurarse de que el texto capturado es una patente válida (solo letras y números)
                if patente_texto:
                    # Guardar imagen
                    timestamp = int(time.time())
                    nombre_archivo = f"{patente_texto or 'auto'}_{timestamp}.jpg"
                    path = os.path.join(output_folder, nombre_archivo)
                    cv2.imwrite(path, frame)
                    print(f"[✓] Auto detectado - Guardado: {nombre_archivo} - Patente: {patente_texto}")

                    # Dibujar cuadro y texto de la patente en la imagen
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"Patente: {patente_texto}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Mostrar video en vivo
    cv2.imshow("Camara Canal 2", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
