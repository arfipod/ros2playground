# Guía de soluciones y criterios

Consulta cada apartado después de intentar la práctica. Los archivos de `ros_ws/src` constituyen la referencia inicial funcional; las ampliaciones de aquí se aplican sobre ella. Conserva un commit antes de copiar soluciones.

## 00 · Primer arranque

Nodos de aplicación: `/sensor` genera telemetría, `/monitor` la registra desde C++, `/rover` simula y publica odometría/lidar/TF, `/patrol` decide la orden propuesta y `/guard` filtra esa orden. RViz añade su propio nodo cuando está activo. La CLI también puede añadir nodos temporales.

La parada está enclavada en guard. Poner el modo OFF no libera ese enclavamiento y liberar el enclavamiento no cambia el modo. Son estados independientes. Cerrar la pestaña no equivale a terminar los procesos.

## 01 · Grafo

Avance: `linear.x` positivo y `angular.z` cero. Giro en el sitio: `linear.x` cero y `angular.z` distinto de cero. Curva: ambos distintos de cero. `/turtle1/pose` es `turtlesim/msg/Pose` y turtlesim sigue publicándolo aunque esté parado.

La inspección debe mostrar un publicador de comandos durante la publicación CLI, y turtlesim como suscriptor. Si no ves un endpoint fugaz después de terminar el comando es normal: ya no existe.

## 02 · Python

`soluciones/battery_alarm.py` es una implementación ejecutable. Umbral 12.3: las muestras oscilan entre 11.8 y 12.2 aproximadamente, así que todas cumplen la condición de alarma. Umbral 11.9: solo parte del ciclo la cumple.

Histéresis: guarda un bool `low`. Cuando `not low and voltage < 11.9`, activa; cuando `low and voltage > 12.1`, desactiva. Si publicas solo en transiciones, un consumidor que llegue tarde no sabrá el estado actual a partir de un topic volatile sin nuevas transiciones. Puedes publicar el estado periódicamente o estudiar una QoS apropiada; la elección depende del contrato.

## 03 · C++

La versión ampliada completa está en `soluciones/monitor.cpp`. Para probarla después de intentar el ejercicio:

```bash
cp soluciones/monitor.cpp ros_ws/src/lab_cpp/src/monitor.cpp
bash scripts/build.sh
```

Declara el parámetro en el constructor y consulta su valor en el callback. Un contador puede detectar `expected = last + 1` con aritmética unsigned, que define el wrap de 32 bits. No uses una primera muestra inexistente como referencia ni confundas un reinicio del sensor con pérdida de transporte sin otras evidencias.

## 04 · QoS y callbacks

| Publicador | Suscriptor | Compatibilidad de fiabilidad |
|---|---|---|
| reliable | reliable | Sí |
| reliable | best effort | Sí |
| best effort | reliable | No |
| best effort | best effort | Sí |

Esto solo evalúa fiabilidad: otras políticas también importan. Un sleep de 0.8 s dentro del callback limita la tasa observada aunque el período solicitado sea 0.1 s. Vuelve a la versión sin sleep después del experimento.

## 05 · Parámetros

`soluciones/patrol_extended.py` incluye validación inicial y dinámica de `obstacle_distance`, además del estado observable del proyecto final. Es un módulo de paquete, no un script standalone. Para probar esa solución:

```bash
cp soluciones/patrol_extended.py ros_ws/src/lab_py/lab_py/patrol.py
bash scripts/build.sh
```

Prueba `ros2 param set /patrol obstacle_distance 0.9` y después `0.1`. El segundo valor debe ser rechazado. Un override inicial inválido debe impedir el arranque con un error claro. El getter debe conservar 0.9 después de rechazar 0.1.

## 06 · Acciones

En la API estándar los estados terminales relevantes son `STATUS_SUCCEEDED`, `STATUS_CANCELED` y `STATUS_ABORTED`, definidos en `action_msgs/msg/GoalStatus`. Una respuesta a `cancel_goal_async` indica qué objetivos acepta cancelar el servidor; el resultado final confirma en qué estado terminó.

Para parametrizar el ejemplo, usa `argparse` antes de inicializar ROS, sin pasar tus argumentos propios a `rclpy.init`. Comprueba que el ángulo es finito y que el tiempo de cancelación es positivo. El ejemplo de referencia tiene un timeout para que una ausencia de servidor no parezca un bloqueo ilimitado.

## 07 · Launch y bags

Añade `DeclareLaunchArgument('monitor', default_value='true')` y, en el `Node` C++, `condition=IfCondition(LaunchConfiguration('monitor'))`. Para parametrizar el YAML declara un argumento con la ruta por defecto y úsalo en `parameters=[LaunchConfiguration('params_file')]`.

Para el remapeo, el resultado esperado es `/bench/power`. Un bag reproducido mientras están activos los publicadores originales puede crear mezclas de datos. Graba o reproduce con un plan explícito de quién publica cada canal.

## 08 · TF

El lidar original está en `base_link`. Si desplazas el sensor, calcula los rayos desde `x + 0.1*cos(yaw), y + 0.1*sin(yaw)`, usa `frame_id='laser'` y publica `base_link → laser` con traslación x de 0.1. No debe haber dos padres distintos del mismo frame ni varios productores contradictorios de la misma transformación.

Para el movimiento v=0.1, w=0.4 durante 3 s, el modelo ideal sin gate recorrería un arco de radio 0.25 m y ángulo 1.2 rad. El tiempo real de recepción y los límites del gate hacen que la observación no sea una comparación exacta con ese valor ideal.

## 09 · Pruebas

`soluciones/limiter.py` satisface el contrato. Para probarla sin sobrescribir tu ejercicio:

```bash
PYTHONPATH=soluciones:ejercicios python3 -m unittest check_limiter -v
```

El orden de PYTHONPATH selecciona primero la solución del limitador. Como comprobación corta adicional:

```bash
python3 -c 'import sys; sys.path.insert(0,"soluciones"); from limiter import limit; import math; assert limit(math.nan,0)==(0,0); assert limit(2,-5)==(0.35,-1)'
```

La frontera de edad 0.5 se acepta; 0.500001 produce cero. Obstáculo a 0.55 no activa el bloqueo por distancia; por debajo sí. Escribe la expectativa con estos operadores concretos. `distance=inf` representa ausencia de retorno en el sector y se permite; NaN no.

## 10 · Gazebo

El bridge convierte tipos, no solo nombres. El comando requiere ROS_TO_GZ porque el publicador está en ROS y el plugin DiffDrive escucha en Gazebo. La odometría, TF y el reloj recorren el camino contrario. Cambiar el radio del plugin altera la relación entre velocidades de ruedas, velocidad ordenada y odometría; con una geometría inconsistente no debes asumir que la distancia física y la estimada seguirán coincidiendo.

El mundo de esta práctica no tiene sensor de obstáculos ni gate, y no debe presentarse como la misma aplicación de patrulla con física añadida. Su propósito es aislar la integración Gazebo–ROS y hacer visibles esas diferencias.

## 11 · Proyecto

La referencia ampliada publica `/patrol_state` en cada ciclo. La fuente del estado es patrol, no guard: si guard enclava una parada, patrol puede seguir diciendo ADVANCE porque esa sigue siendo su intención. Esta diferencia entre intención y orden efectiva debe constar en el informe. Una ampliación útil sería publicar también el motivo de bloqueo del gate.

Las tres limitaciones mínimas pueden ser: no hay planificación global; el lidar y la dinámica ligeros son ideales; la recepción reciente no garantiza edad de origen; la parada no es un sistema certificado; no se analiza un plazo duro de reacción. Explica las que realmente afectan a tus experimentos, sin rellenar una lista genérica.

No hay una solución única para decisiones de diseño. Para aprobar, el comportamiento debe ser observable, sus límites conocidos y las pruebas reproducibles.
