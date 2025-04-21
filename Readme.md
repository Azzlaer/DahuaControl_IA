# Sistema de Detección de Patentes de Autos

Este es un sistema de detección de patentes de autos utilizando una cámara de seguridad IP, procesamiento en tiempo real con YOLOv8 y OCR con Tesseract.

## Descripción

El sistema captura en tiempo real las imágenes de los autos que pasan frente a la cámara, detecta las patentes utilizando YOLO para identificar los vehículos y Tesseract OCR para extraer las patentes. Los resultados se guardan en imágenes y se pueden almacenar en una base de datos SQLite. Además, se envían notificaciones a Discord si se desea.

### Funcionalidades

- **Detección en tiempo real**: Procesamiento de la transmisión de video en vivo desde la cámara IP.
- **OCR para Patentes**: Extrae la patente del vehículo utilizando Tesseract.
- **Guardado de imágenes**: Las imágenes capturadas se guardan en una carpeta local.
- **Notificación a Discord**: Opcionalmente, se puede configurar para que las patentes y las imágenes se envíen a un canal de Discord.

## Requisitos

1. Python 3.x
2. Librerías de Python:
   - `opencv-python`
   - `pytesseract`
   - `ultralytics`
   - `onvif-zeep`
   - `requests`
   - `flask`
   - `sqlite3`
3. Tesseract OCR instalado

### Instalación

1. Instalar las dependencias utilizando `pip`:
pip install -r requirements.txt

Asegúrate de que Tesseract OCR esté instalado en tu máquina. Puedes descargarlo desde aquí.

Configura la cámara IP en el archivo config.ini. Asegúrate de incluir la IP, usuario, contraseña y canal de la cámara.

Ejecuta el script main.py:
python main.py


Configuración
El archivo config.ini debe tener el siguiente formato:

[CAMARA]
ip = 192.168.0.4
usuario = teclado
password = 123456teclado
canal = 2

[DETECCION]
modelo = yolov8n.pt
frame_interval = 5

[GUARDADO]
carpeta = capturas

[VISUALIZACION]
resolucion_ancho = 800
resolucion_alto = 600

[PTZ]
habilitar = true

[DISCORD]
webhook_url = https://discord.com/api/webhooks/tu_webhook_aqui
notificaciones = true
Notificaciones a Discord
Puedes configurar el webhook de Discord para recibir notificaciones en tiempo real sobre las patentes detectadas y las imágenes capturadas.

Estructura del Proyecto
/proyecto
│
├── main.py               # Script principal para detección y manejo de cámara
├── config.ini            # Archivo de configuración
├── requirements.txt      # Dependencias necesarias
├── capturas/             # Carpeta donde se guardan las imágenes capturadas
├── eventos.db            # Base de datos SQLite con los eventos
└── templates/            # Archivos HTML para interfaz web (si se utiliza Flask)

Contribuciones
Las contribuciones son bienvenidas. Si tienes alguna sugerencia o mejora, siéntete libre de abrir un pull request.