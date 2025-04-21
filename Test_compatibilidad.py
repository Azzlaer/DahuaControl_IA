import cv2
import pytesseract
from ultralytics import YOLO
from onvif import ONVIFCamera
import logging
import datetime

# Configurar logging
log_file = "test_log.txt"
logging.basicConfig(
    filename=log_file,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def log_and_print(message, level="info"):
    print(message)
    if level == "info":
        logging.info(message)
    elif level == "error":
        logging.error(message)

def test_opencv():
    try:
        version = cv2.__version__
        log_and_print(f"[✓] OpenCV versión: {version}")
    except Exception as e:
        log_and_print(f"[✗] Error con OpenCV: {e}", "error")

def test_tesseract():
    try:
        version = pytesseract.get_tesseract_version()
        log_and_print(f"[✓] Tesseract versión: {version}")
    except Exception as e:
        log_and_print(f"[✗] Error con Tesseract: {e}", "error")

def test_yolo():
    try:
        model = YOLO("yolov8n.pt")
        log_and_print("[✓] YOLO cargado correctamente")
    except Exception as e:
        log_and_print(f"[✗] Error con YOLO: {e}", "error")

def test_onvif():
    try:
        cam = ONVIFCamera("127.0.0.1", 80, "admin", "admin")  # Dummy data
        log_and_print("[✓] ONVIF importado correctamente (simulado)")
    except Exception as e:
        log_and_print(f"[✗] Error con ONVIF: {e}", "error")

if __name__ == "__main__":
    log_and_print("🔍 Iniciando test del entorno...\n")

    test_opencv()
    test_tesseract()
    test_yolo()
    test_onvif()

    log_and_print("\n✅ Test finalizado.")

    input("\nPresiona ENTER para cerrar...")  # Pausa final para que puedas ver el resultado
