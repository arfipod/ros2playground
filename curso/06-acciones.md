# 06 · Objetivos que tardan: acciones

**Objetivo:** enviar un objetivo, leer feedback y cancelar una acción. **Tiempo:** 45 minutos. Para la demostración del curso y arranca solo turtlesim.

## El contrato

Una acción tiene goal, feedback y result. El servidor puede aceptar o rechazar el objetivo. Después de aceptarlo publica feedback y finalmente termina con un estado, por ejemplo succeeded, canceled o aborted. La cancelación es una petición: no debes asumir que todo servidor la acepta ni que es instantánea.

Usaremos la acción existente `turtlesim/action/RotateAbsolute`. Así puedes centrarte en el cliente y el protocolo antes de escribir un servidor propio. No implementamos un servidor de misiones completo en este curso de fundamentos.

## Desde la CLI

```bash
ros2 run turtlesim turtlesim_node
# Otra terminal:
ros2 action list -t
ros2 action info /turtle1/rotate_absolute
ros2 interface show turtlesim/action/RotateAbsolute
ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute \
  "{theta: 3.0}" --feedback
```

Observa el goal aceptado, los valores de ángulo restante y el resultado final. Si repites exactamente el mismo objetivo cuando la tortuga ya está orientada así, la acción puede acabar muy deprisa. No es un error de feedback.

## Cliente Python

Lee `ejemplos/rotate_action.py`. El cliente espera al servidor con límite de tiempo, envía el goal de forma asíncrona y permite procesar callbacks mientras espera los futuros. El ejemplo usa `spin_until_future_complete` desde la función principal, no dentro de un callback de un nodo ya en spin.

```bash
ros2 service call /reset std_srvs/srv/Empty "{}"
python3 ejemplos/rotate_action.py
ros2 service call /reset std_srvs/srv/Empty "{}"
python3 ejemplos/rotate_action.py --cancel
```

En el segundo caso el timer solicita la cancelación después de 0.5 segundos. Mira el estado del resultado: las constantes oficiales de `action_msgs/msg/GoalStatus` permiten interpretarlo sin depender de números memorizados.

## Ejercicio

Modifica una copia del cliente para que el ángulo objetivo y el tiempo hasta cancelar se reciban como argumentos. Prueba un objetivo cercano y otro lejano. Registra por separado: servidor no disponible, objetivo rechazado, resultado completado y cancelación solicitada. No inventes una respuesta de rechazo si el servidor de turtlesim no rechaza tu caso: explica qué rama del cliente lo gestionaría.

## Comprueba

La versión normal debe terminar con éxito y la versión cancelada debe observar una cancelación cuando el objetivo aún está en curso. Si no ocurre, reinicia o resetea turtlesim y repite con un recorrido angular largo. Detén todos los procesos al terminar.

**Pregunta:** ¿por qué un servicio que gira el robot y no responde hasta terminar complica el diseño? Porque mezcla una operación larga con una interacción breve y no ofrece por sí mismo el protocolo de feedback y cancelación de una acción.
