# Estado de validación de la entrega

Fecha: 20 de octubre de 2026.

## Ejecutado en el entorno de creación

- 17 pruebas de algoritmos de la referencia, todas correctas: cinemática, intersecciones, sector del lidar y gate ante límites, caducidad, enclavamiento y entradas no finitas.
- 3 pruebas del limitador usando la solución proporcionada, todas correctas.
- Compilación de sintaxis Python con `compileall` sin importar dependencias ROS.
- Análisis de sintaxis Bash de los scripts de entorno, construcción, setup y diagnóstico.
- Lectura y validación estructural de JSON, YAML y XML/SDF; esto no sustituye los esquemas o validadores específicos de ROS, RViz o SDFormat.
- Comprobación de enlaces locales Markdown y presencia de 12 prácticas.

## Ejecutado después en GitHub Actions

La primera ejecución de [ROS 2 course checks](https://github.com/arfipod/ros2playground/actions/runs/39394845561), sobre el commit `21cc1d194ab897f1084e36e9edac41080b4a4fab`, terminó correctamente:

- Compilación de los tres paquetes con colcon en el contenedor ROS Jazzy.
- Pruebas de algoritmos.
- Integración ROS real: recepción de telemetría, presencia del nodo C++, lidar, odometría, rechazo de modo desconocido, movimiento en PATROL y parada enclavada.
- Conservación del log de ejecución como artefacto del workflow.

## Pendiente de validar en Codespaces

Todavía no se ha arrancado la imagen completa de desarrollo, el escritorio noVNC, RViz ni Gazebo. El workflow usa la imagen base de ROS y ejecuta los nodos sin interfaz gráfica. Por tanto, su resultado no demuestra que el escritorio o el renderizado 3D funcionen correctamente ni mide su rendimiento.

La configuración está preparada para comprobar esos puntos al crear el Codespace. Los cambios posteriores limitados a documentación no requieren repetir la prueba de código ya completada.

## Primera validación en Codespaces

1. Espera a que termine `postCreateCommand` sin errores.
2. Abre una terminal nueva en la raíz y ejecuta `bash scripts/doctor.sh`.
3. Sin otras demos ejecutándose, lanza `ROS_DOMAIN_ID=73 python3 scripts/check_runtime.py`. Debe imprimir PASS y cerrar sus procesos.
4. Abre 6080 en modo Private y arranca `ros2 launch lab_py course.launch.py`. Comprueba RViz y los servicios de modo/parada.
5. Detén esa demo y arranca `ros2 launch lab_py gazebo.launch.py gui:=false`. Comprueba `/clock` y `/odom`, envía una orden breve y después un Twist cero.
6. Si funciona el servidor de Gazebo, prueba también el cliente gráfico y valora el rendimiento de ese Codespace.

Las dos comprobaciones siguientes son diferentes: la integración ROS verifica comunicación y comportamiento básico, mientras la prueba del escritorio y Gazebo verifica además dependencias gráficas y recursos. Si una falla, conserva el log y consulta `DIAGNOSTICO.md`.
