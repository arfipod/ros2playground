# 08 · Coordenadas, odometría y sensores

**Objetivo:** explicar dónde está expresado cada dato y visualizarlo correctamente. **Tiempo:** 60 minutos.

## Antes de mirar el dibujo

Una posición solo tiene sentido con una referencia. El simulador publica la pose del robot respecto a `odom` y una transformación `odom → base_link`. El lidar se expresa en `base_link`: ángulo cero hacia delante, positivo antihorario alrededor de z. La odometría contiene una estimación de pose y velocidad; en este simulador es la solución de un modelo ideal, sin ruido.

En un robot real puede haber `map`, `odom`, `base_link` y frames de sensores. No son sinónimos. Habitualmente `odom` busca continuidad local y `map` ofrece una referencia global que puede corregirse. Aquí no existe localización global, SLAM ni un frame `map`.

## Observa

```bash
ros2 launch lab_py course.launch.py
# Otra terminal:
ros2 topic echo /odom --once
ros2 topic echo /scan --once --qos-reliability best_effort
ros2 run tf2_ros tf2_echo odom base_link
```

En RViz usa `odom` como **Fixed Frame**. El robot aparece como un Marker, no como una malla URDF. En la configuración incluida, la rejilla mide un metro por celda y el lidar usa best effort para ser compatible con su publicador.

Cambia temporalmente el Fixed Frame a `map`: aparecerán errores porque el sistema no publica una transformación que conecte ese frame. Restáuralo a `odom`. Si desaparecen los puntos del lidar, comprueba el topic, la compatibilidad QoS y los mensajes de estado de RViz antes de cambiar el modelo.

## El modelo cinemático

`core.integrate` integra un robot planar con velocidad lineal v y angular w. Cuando w es cero, avanza en la dirección actual. Cuando w no es cero, sigue un arco de circunferencia. La orientación se representa internamente como yaw y se convierte en un cuaternión alrededor de z para publicar TF y odometría.

`ray_circle` calcula la intersección de cada rayo con obstáculos circulares. El sensor devuelve hasta seis metros y cubre una vuelta. Esto es geometría ideal: no hay ruido, oclusiones complejas, dinámica de motores, límites de adherencia ni colisiones resueltas por un motor físico. El dibujo puede atravesar obstáculos si ordenas movimientos inadecuados; no atribuyas al simulador una propiedad que no implementa.

## Ejercicio

Con el modo OFF, envía una orden por el canal previo al gate:

```bash
# Detén antes el launch y arranca solo rover y guard en terminales separadas:
ros2 run lab_py rover
# Terminal B:
ros2 run lab_py guard
# Terminal C:
timeout 3s ros2 topic pub /cmd_vel_raw geometry_msgs/msg/Twist \
  "{linear: {x: 0.1}, angular: {z: 0.4}}" --rate 10
```

No ejecutes `patrol` en esta prueba: incluso en modo OFF publicaría ceros en el mismo canal. Mide el cambio de posición con `/odom`. Si deseas visualizar esta ejecución aislada, lanza `rviz2 -d ros_ws/src/lab_py/config/course.rviz`.

## Comprueba

Puedes explicar por qué un giro positivo cambia la trayectoria hacia la izquierda y por qué el gate limita avanzar, pero permite girar ante un obstáculo frontal. Al cortar la publicación, el robot debe detenerse tras el watchdog. La práctica siguiente mide ese comportamiento con más cuidado.

**Reto:** dibuja un frame de lidar desplazado 10 cm hacia delante. Eso requiere publicar la transformación correcta y calcular los rayos desde esa nueva posición, no solo cambiar el texto de `frame_id`.
