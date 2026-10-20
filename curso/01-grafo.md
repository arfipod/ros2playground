# 01 · Entender un sistema mirando su grafo

**Objetivo:** distinguir nodo, topic, mensaje y servicio sin escribir código. **Tiempo:** 45 minutos. Empieza con los launch anteriores detenidos.

## El modelo

Un nodo es un participante lógico del sistema ROS. Un proceso puede contener uno o varios nodos. Un topic identifica un flujo de mensajes tipados: un publicador envía muestras y uno o varios suscriptores las reciben. El nombre y el tipo deben coincidir, pero también debe existir compatibilidad de QoS. El grafo describe estas relaciones; no es una lista de llamadas a funciones.

Si vienes de embebidos, piensa en componentes comunicados mediante interfaces, colas y callbacks. ROS añade descubrimiento y herramientas de inspección. Eso no convierte automáticamente la aplicación en determinista o de tiempo real: hay que analizar planificación, memoria, comunicaciones y plazos.

## Explora turtlesim

Terminal A:

```bash
ros2 run turtlesim turtlesim_node
```

Mira su ventana en noVNC. Terminal B:

```bash
ros2 node list
ros2 node info /turtlesim
ros2 topic list -t
ros2 topic info /turtle1/cmd_vel -v
ros2 interface show geometry_msgs/msg/Twist
```

`Twist` contiene velocidades lineales y angulares. Para un robot planar usamos normalmente `linear.x` en m/s y `angular.z` en rad/s. La tortuga es una demostración de coordenadas y no un robot con unidades físicas calibradas.

Publica durante tres segundos:

```bash
timeout 3s ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 1.0}, angular: {z: 0.7}}" --rate 10
ros2 topic echo /turtle1/pose --once
```

El código de salida 124 de `timeout` significa que terminó por el límite de tiempo; aquí es esperado. Prueba `ros2 run turtlesim turtle_teleop_key` y da el foco a su terminal para manejar las flechas. Sal con `Ctrl+C`.

## Ejercicio

Haz tres movimientos distintos cambiando solo los campos del mensaje: avanzar recto, girar sobre el sitio y describir una curva. Observa `ros2 topic hz /turtle1/pose` durante unos segundos. Esa frecuencia es una estimación del observador; no es una garantía del planificador.

Abre `ros2 run rqt_graph rqt_graph`. Activa la vista de topics si aparecen ocultos. Identifica el nodo de publicación temporal de la CLI, turtlesim y la dirección del flujo. La CLI también puede crear participantes ROS y alterar el grafo mientras inspeccionas.

## Terminado cuando

Puedes explicar por qué hay posición aunque hayas dejado de publicar velocidades, y puedes identificar el tipo de `/turtle1/pose` sin adivinarlo. Sabrás diagnosticar el error de publicar `std_msgs/msg/String` en un topic que espera `Twist`: no comparten la interfaz requerida.

**Pregunta:** ¿pueden varios nodos publicar en el mismo topic? Sí. Eso puede ser deliberado o una fuente de órdenes contradictorias; en el proyecto final habrá un único productor previsto de `/cmd_vel`.

Para finalizar, detén turtlesim y rqt_graph. Soluciones y respuestas: `soluciones/GUIA.md`, práctica 01.
