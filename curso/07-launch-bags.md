# 07 · Arranques repetibles y grabación de datos

**Objetivo:** lanzar varios componentes de forma declarativa y reproducir datos grabados. **Tiempo:** 60 minutos.

## Launch no es una shell larga

El launch file reúne procesos, argumentos, configuración y condiciones. El sistema se puede recrear sin recordar cinco terminales. Lee `course.launch.py`: el argumento `rviz` controla solo la visualización; el simulador sigue publicando datos aunque no abras ventanas. Los parámetros de patrulla se cargan desde un YAML instalado con el paquete.

```bash
ros2 launch lab_py course.launch.py --show-args
ros2 launch lab_py course.launch.py rviz:=false
```

La opción sin RViz es útil para pruebas automáticas. No borres la visualización del código para ejecutar una prueba en servidor: usa un argumento.

## Nombres y remapeos

Detén el launch y prueba:

```bash
ros2 run lab_py sensor --ros-args -r __ns:=/bench -r telemetry:=power
# Otra terminal:
ros2 run lab_cpp monitor --ros-args -r __ns:=/bench -r telemetry:=power
ros2 topic info /bench/power -v
```

Los nodos de referencia usan nombres relativos para los topics de aplicación. Bajo ese namespace, `telemetry` se resolvería como `/bench/telemetry`; el remapeo lo convierte en `/bench/power`. En cambio, un nombre que empieza por `/` ya es absoluto. Los frames de TF son identificadores de coordenadas y no se renombran automáticamente por cambiar el namespace ROS: dos robots requieren también una estrategia de nombres de frames.

## Graba una ejecución

Detén sensor y monitor aislados y vuelve a lanzar el curso. En otra terminal:

```bash
mkdir -p recordings
ros2 bag record -o recordings/patrol_01 /telemetry /odom /scan /tf /cmd_vel
```

En otra terminal inicia PATROL y déjalo unos 20 segundos. Para la grabación con `Ctrl+C` y después para el launch. Inspecciona:

```bash
ros2 bag info recordings/patrol_01
ros2 bag play recordings/patrol_01
# Otra terminal:
ros2 topic echo /telemetry --once
```

La carpeta de salida no debe existir previamente. Para otra grabación usa un nombre nuevo. No reproduzcas un bag de órdenes junto a una aplicación que pueda ejecutarlas: en este laboratorio también causarías conflictos entre productores de `/cmd_vel`. El playback reproduce mensajes; no reconstruye mágicamente el estado interno de cada nodo original.

## Ejercicio

Añade a una copia de `course.launch.py` un argumento `monitor`, que permita desactivar el proceso C++ igual que `rviz`. Comprueba con `ros2 node list` que el resto sigue vivo. Después prepara un segundo YAML de parámetros con una velocidad de 0.1 y documenta cómo seleccionarlo en el launch.

## Comprueba

Entrega el comando de arranque, una descripción de tu remapeo y el resumen `ros2 bag info`. No hace falta subir el bag al repositorio: ocupa espacio y está ignorado. Guarda una nota de las condiciones del experimento, que tiene más valor que un archivo sin contexto.

**Pregunta:** ¿la repetición del bag garantiza reproducir exactamente el scheduling del sistema original? No. Conservas los datos grabados y su secuencia temporal de reproducción, pero el procesamiento sigue dependiendo del entorno y de los consumidores.
