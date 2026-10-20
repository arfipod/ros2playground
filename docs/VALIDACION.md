# Estado de validación de la entrega

Fecha: 20 de octubre de 2026.

## Ejecutado en el entorno de creación

- 17 pruebas de algoritmos de la referencia, todas correctas: cinemática, intersecciones, sector del lidar y gate ante límites, caducidad, enclavamiento y entradas no finitas.
- 3 pruebas del limitador usando la solución proporcionada, todas correctas.
- Compilación de sintaxis Python con `compileall` sin importar dependencias ROS.
- Análisis de sintaxis Bash de los scripts de entorno, construcción, setup y diagnóstico.
- Lectura y validación estructural de JSON, YAML y XML/SDF; esto no sustituye los esquemas o validadores específicos de ROS, RViz o SDFormat.
- Comprobación de enlaces locales Markdown y presencia de 12 prácticas.

## Preparado, pero no ejecutado aquí

El entorno de creación no dispone de Docker ni ROS. Por tanto, no se ha ejecutado la construcción de la imagen, la compilación de los paquetes C++/interfaces con colcon, la prueba de integración ROS, el escritorio noVNC, RViz ni Gazebo.

No se presenta el entorno como probado de extremo a extremo. La configuración está preparada para arrancarlo y resolver esos puntos en Codespaces. El workflow de GitHub se ejecutará al subir el repositorio; todavía no existe un resultado de CI asociado a esta entrega.

## Primera validación en Codespaces

1. Espera a que termine `postCreateCommand` sin errores.
2. Abre una terminal nueva en la raíz y ejecuta `bash scripts/doctor.sh`.
3. Sin otras demos ejecutándose, lanza `ROS_DOMAIN_ID=73 python3 scripts/check_runtime.py`. Debe imprimir PASS y cerrar sus procesos.
4. Abre 6080 en modo Private y arranca `ros2 launch lab_py course.launch.py`. Comprueba RViz y los servicios de modo/parada.
5. Detén esa demo y arranca `ros2 launch lab_py gazebo.launch.py gui:=false`. Comprueba `/clock` y `/odom`, envía una orden breve y después un Twist cero.
6. Si funciona el servidor de Gazebo, prueba también el cliente gráfico y valora el rendimiento de ese Codespace.

Las dos comprobaciones siguientes son diferentes: la integración ROS verifica comunicación y comportamiento básico, mientras la prueba del escritorio y Gazebo verifica además dependencias gráficas y recursos. Si una falla, conserva el log y consulta `DIAGNOSTICO.md`.
