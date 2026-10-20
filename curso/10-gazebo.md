# 10 · Pasar de cinemática ideal a Gazebo

**Objetivo:** ejecutar un mundo SDF y conectar el transporte de Gazebo con ROS 2. **Tiempo:** 60 minutos. Empieza con todos los nodos de la simulación ligera detenidos.

## Dos sistemas de comunicaciones

Gazebo tiene su propio transporte. Tener un topic de Gazebo llamado `/cmd_vel` no lo convierte en un topic ROS del mismo nombre. `ros_gz_bridge` convierte mensajes entre ambos. El archivo `config/bridge.yaml` declara tipos y dirección para comandos, odometría, TF y reloj.

La pareja elegida es ROS 2 Jazzy con Gazebo Harmonic. El mundo `worlds/rover.sdf` es local y usa primitivas: suelo, cuerpo, dos ruedas y un apoyo. El plugin DiffDrive transforma el mensaje de velocidad en movimiento de las articulaciones. No necesita descargar modelos de Fuel y no incluye lidar ni controlador de patrulla: es un laboratorio distinto para estudiar física e integración.

## Arranca

```bash
ros2 launch lab_py gazebo.launch.py
```

Abre el escritorio noVNC. Si la ventana gráfica no funciona o va demasiado lenta:

```bash
# Para la ejecución anterior con Ctrl+C antes de arrancar otra.
ros2 launch lab_py gazebo.launch.py gui:=false
```

En ambos casos el servidor debe avanzar en tiempo. Observa:

```bash
ros2 topic echo /clock --once
ros2 topic echo /odom --once
gz topic -l
```

El servidor se lanza con `-r` para iniciar la simulación sin tener que pulsar Play. El cliente gráfico es un proceso separado. Ejecutar sin cliente reduce necesidades de renderizado, pero no elimina el coste del motor físico.

## Mueve y detén

```bash
timeout 3s ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.15}, angular: {z: 0.2}}" --rate 10
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{}" --once
```

**Envía siempre el cero final:** este mundo no instala el gate ni el watchdog de la simulación ligera y DiffDrive puede conservar la última orden. El `timeout` solo termina el publicador; no es una orden de parada del robot. Aquí estás aprendiendo precisamente a distinguir ambos contratos.

## Ejercicio

Compara la odometría antes y después del movimiento. Identifica en el SDF el radio de rueda y su separación. Cambia solo el valor de radio usado por el plugin, sin cambiar la geometría física, recompila si hace falta para reinstalar el recurso y reinicia. Predice y observa qué ocurre con el movimiento y la odometría. Un plugin mal parametrizado puede producir resultados coherentes internamente pero distintos de la geometría real.

Restaura el SDF. Cambia la dirección del bridge de comandos a `GZ_TO_ROS` en una copia y explica por qué el comando ROS ya no mueve el modelo. No necesitas cambiar el código del controlador para provocar ese fallo.

## Tiempo de simulación

Gazebo publica `/clock`. Los nodos que deban interpretar su tiempo tienen que usar `use_sim_time:=true`; publicar `/clock` no modifica automáticamente todos los relojes ROS. Nuestro simulador ligero usa su propio tiempo y no debes ejecutarlo a la vez que este mundo, porque colisionarían nombres y productores.

## Comprueba

Debes poder observar odometría con o sin GUI, explicar para qué sirve cada dirección del bridge y detener el modelo con un mensaje. Si el entorno gráfico falla, documenta ese resultado y completa la parte de transporte en modo headless. No confundas una limitación de OpenGL con una incompatibilidad de mensajes ROS.
