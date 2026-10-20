# Diagnóstico rápido

| Síntoma | Comprobación y siguiente paso |
|---|---|
| `ros2: command not found` | Comprueba `/opt/ros/jazzy`. Si no existe, reconstruye el contenedor desde la configuración del repo. Si existe, `source scripts/env.sh`. |
| `Package lab_py not found` | Desde la raíz, `bash scripts/build.sh`; después `source scripts/env.sh` en esa misma terminal o abre una nueva. |
| `postCreateCommand` falló | Abre su log; distingue un fallo de descarga apt de un error de compilación. Repite `bash scripts/setup.sh` tras corregir el problema. |
| No aparece puerto 6080 | Revisa que se haya instalado desktop-lite. Consulta los logs de construcción del contenedor. Prueba reenviarlo desde Ports. |
| Error al conectar noVNC | Mantén sesión GitHub iniciada, abre la URL de Ports en otra pestaña y comprueba si la red permite el dominio y WebSockets. No publiques el puerto para evitar la autenticación. |
| Ventana no aparece | Comprueba `echo "$DISPLAY"` y si el escritorio está conectado. Las GUI están en noVNC, no en el panel central de VS Code. |
| RViz falla por OpenGL | `glxinfo -B` desde la terminal con DISPLAY configurado. Se usa Mesa por software. Prueba la aplicación con `rviz:=false` para separar comunicación ROS de renderizado. |
| No llega telemetría | `ros2 topic info /telemetry -v`: nombre, tipo, QoS, publicadores y suscriptores. Revisa `ROS_DOMAIN_ID` en ambas terminales. |
| Nombres duplicados | Para launch y procesos aislados antes de empezar una práctica nueva. Usa `ros2 node list`. |
| Rover no avanza | Modo PATROL, parada liberada, scan reciente y un único productor previsto de comandos. Inspecciona `/cmd_vel_raw` y `/cmd_vel`. |
| El reset no deja quieto al rover | Pon el modo OFF antes de resetear. El servicio del simulador no cambia el estado del controlador. |
| Gazebo no muestra GUI | Detén la ejecución anterior y usa `gui:=false`. Comprueba `/clock` y `/odom`. El simulador ligero permite continuar la parte principal del curso. |
| Gazebo no se detiene al cerrar el publicador | Envía un Twist cero. Ese mundo no incluye el watchdog de la simulación ligera. |
| Bag no se crea | La carpeta de salida ya puede existir. Usa un nombre nuevo y comprueba espacio libre. |
| Cambié un YAML y no cambia el resultado | Recompila para instalar recursos si no están enlazados y reinicia el launch. Comprueba la ruta que carga. |
| Un test ROS falla | Ejecuta sin demos, con `ROS_DOMAIN_ID=73`, y lee `/tmp/ros2-course-runtime.log`. |

Parar un proceso: `Ctrl+C` en su terminal. Parar el entorno: **Stop codespace** desde GitHub. Antes de borrar un entorno, haz commit y push de lo que quieras conservar. Los directorios build/install/log pueden regenerarse y están ignorados.
