<?php
// Cargar el archivo INI
$config = parse_ini_file('config.ini', true);

// Leer las configuraciones
$ip_camara = $config['CAMARA']['ip'];
$usuario_camara = $config['CAMARA']['usuario'];
$contraseña_camara = $config['CAMARA']['password'];
$canal_camara = $config['CAMARA']['canal'];

$modelo_yolo = $config['DETECCION']['modelo'];
$frame_intervalo = $config['DETECCION']['frame_interval'];

$carpeta_guardado = $config['GUARDADO']['carpeta'];

$resolucion_ancho = $config['VISUALIZACION']['resolucion_ancho'];
$resolucion_alto = $config['VISUALIZACION']['resolucion_alto'];

$habilitar_ptz = $config['PTZ']['habilitar'];

$webhook_url_discord = $config['DISCORD']['webhook_url'];
$notificaciones_discord = $config['DISCORD']['notificaciones'];
$subir_imagen_discord = $config['DISCORD']['subir_imagen'];

// Conectar a la base de datos SQLite
try {
    $db = new PDO('sqlite:eventos.db');
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("No se pudo conectar a la base de datos: " . $e->getMessage());
}

// Consultar los eventos de patente desde la base de datos
$query = "SELECT patente, fecha FROM eventos ORDER BY fecha DESC LIMIT 10";
$stmt = $db->query($query);
$eventos = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Configuración y Eventos - Detección de Patentes</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f9;
        }
        h1 {
            color: #333;
        }
        .config, .eventos {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .config p, .eventos p {
            font-size: 18px;
            color: #555;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Configuración y Eventos del Sistema de Detección de Patentes</h1>

    <!-- Configuración de la Cámara -->
    <div class="config">
        <h2>Configuración de la Cámara</h2>
        <p><strong>IP:</strong> <?php echo $ip_camara; ?></p>
        <p><strong>Usuario:</strong> <?php echo $usuario_camara; ?></p>
        <p><strong>Contraseña:</strong> <?php echo $contraseña_camara; ?></p>
        <p><strong>Canal:</strong> <?php echo $canal_camara; ?></p>
    </div>

    <!-- Configuración de Detección -->
    <div class="config">
        <h2>Configuración de Detección</h2>
        <p><strong>Modelo YOLO:</strong> <?php echo $modelo_yolo; ?></p>
        <p><strong>Intervalo de frames:</strong> <?php echo $frame_intervalo; ?> frames</p>
    </div>

    <!-- Configuración de Guardado -->
    <div class="config">
        <h2>Configuración de Guardado</h2>
        <p><strong>Carpeta de Guardado:</strong> <?php echo $carpeta_guardado; ?></p>
    </div>

    <!-- Configuración de Visualización -->
    <div class="config">
        <h2>Configuración de Visualización</h2>
        <p><strong>Resolución (Ancho x Alto):</strong> <?php echo $resolucion_ancho . " x " . $resolucion_alto; ?></p>
    </div>

    <!-- Configuración PTZ -->
    <div class="config">
        <h2>Configuración PTZ</h2>
        <p><strong>Habilitar PTZ:</strong> <?php echo ($habilitar_ptz == 'true' ? 'Sí' : 'No'); ?></p>
    </div>

    <!-- Configuración de Discord -->
    <div class="config">
        <h2>Configuración de Discord</h2>
        <p><strong>Webhook URL:</strong> <?php echo $webhook_url_discord; ?></p>
        <p><strong>Notificaciones:</strong> <?php echo ($notificaciones_discord == 'true' ? 'Activadas' : 'Desactivadas'); ?></p>
        <p><strong>Subir Imagen:</strong> <?php echo ($subir_imagen_discord == 'true' ? 'Sí' : 'No'); ?></p>
    </div>

    <!-- Mostrar los últimos eventos (detalles de las patentes) -->
    <div class="eventos">
        <h2>Últimos Eventos de Patentes</h2>
        <?php if (count($eventos) > 0): ?>
            <table>
                <thead>
                    <tr>
                        <th>Patente</th>
                        <th>Fecha</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($eventos as $evento): ?>
                        <tr>
                            <td><?php echo htmlspecialchars($evento['patente']); ?></td>
                            <td><?php echo htmlspecialchars($evento['fecha']); ?></td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        <?php else: ?>
            <p>No se encontraron eventos registrados.</p>
        <?php endif; ?>
    </div>

</body>
</html>
