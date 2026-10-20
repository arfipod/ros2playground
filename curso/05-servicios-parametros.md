# 05 · Órdenes discretas y configuración

**Objetivo:** usar y validar servicios y parámetros con efectos observables. **Tiempo:** 45 minutos.

## Elegir la interacción

Un topic encaja con un flujo continuo como velocidad o lidar. Un servicio encaja con una petición y respuesta breve, como seleccionar el modo de la patrulla. Un parámetro configura un nodo, por ejemplo su velocidad objetivo. Un servicio no es adecuado para retener una petición durante una misión de varios minutos: para seguimiento, feedback y cancelación veremos acciones.

El curso define `lab_interfaces/srv/SetMode.srv`. La línea `---` separa petición y respuesta. En este caso el contrato admite un texto; el servidor es quien valida los valores `OFF` y `PATROL`. No hay un enum que impida construir otras cadenas en el cliente.

## Hazlo

```bash
ros2 launch lab_py course.launch.py
# Otra terminal:
ros2 service list -t
ros2 interface show lab_interfaces/srv/SetMode
ros2 service call /set_mode lab_interfaces/srv/SetMode "{mode: PATROL}"
ros2 service call /set_mode lab_interfaces/srv/SetMode "{mode: TURBO}"
```

La segunda petición debe devolver `success: false` y conservar el modo anterior. Una llamada que devuelve respuesta no implica que la aplicación acepte la orden: comprueba el contenido de esa respuesta.

```bash
ros2 param list /patrol
ros2 param describe /patrol speed
ros2 param set /patrol speed 0.3
ros2 param set /patrol speed 2.0
ros2 param get /patrol speed
```

El valor 2.0 debe rechazarse. El callback de parámetros valida antes de aceptar; `Patrol.tick` consulta los valores aceptados en cada ciclo. Mira ambas partes del código: declarar el parámetro no basta para validar ni para cambiar el comportamiento.

## Ejercicio

Añade el parámetro double `obstacle_distance`, con valor por defecto 0.85 y rango permitido de 0.6 a 2.0. Sustituye el literal de `Patrol.tick`. Valida también el override inicial al construir el nodo. Esa última comprobación importa: registrar una validación después de declarar los parámetros no valida retrospectivamente los valores iniciales.

Prueba un valor correcto, uno fuera de rango y el arranque con un override inválido. Al reducir el umbral, recuerda que el gate bloquea el avance cuando la distancia frontal es menor que 0.55; el controlador de patrulla y el gate tienen responsabilidades distintas.

## Comprueba

Conserva la respuesta de rechazo y demuestra que el parámetro mantiene el último valor aceptado. Pon el modo OFF antes de llamar a `/reset_world`: el reset no cambia el modo del controlador. Si este continúa en PATROL, seguirá publicando órdenes después del reset.

**Pregunta:** ¿te conviene publicar una orden de cambio de modo en un topic sin confirmación? Depende del requisito, pero en este ejercicio queremos conocer si el servidor la aceptó y por eso usamos un servicio.
