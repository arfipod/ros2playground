# 09 · Probar que el comportamiento falla de forma conocida

**Objetivo:** separar algoritmos de adaptadores ROS, probar límites e inyectar fallos. **Tiempo:** 60 minutos.

## Qué comprueba cada nivel

Las pruebas de `tests/test_core.py` importan funciones sin arrancar ROS. Comprueban movimiento recto y circular, intersecciones del lidar, selección del sector frontal y decisiones del gate. Son rápidas y permiten cubrir NaN, infinitos, ausencia de datos y edades fuera de rango.

La prueba `scripts/check_runtime.py` usa procesos ROS reales: lanza los componentes sin RViz, observa topics y llama servicios. Eso detecta errores de instalación, nombres e interfaces que una prueba matemática no puede detectar. El workflow de GitHub ejecuta ambos niveles. Que estén escritos no significa que ya se hayan ejecutado en tu cuenta: consulta el resultado del workflow.

```bash
python3 -m unittest discover -s tests -v
# Para todas las demos y usa otra terminal:
ROS_DOMAIN_ID=73 python3 scripts/check_runtime.py
```

El dominio separado evita mezclar la prueba con otras instancias del mismo entorno. No es una frontera de seguridad.

## El watchdog del ejercicio

El gate recibe `/cmd_vel_raw`, observa `/scan` y publica `/cmd_vel`. Usa tiempo monotónico local para medir cuánto hace que llegaron órdenes y escaneos. Si cualquiera lleva más de 0.5 segundos sin llegar, publica cero. Si el dato frontal no es válido o la parada está enclavada, también publica cero. El simulador añade su propio timeout de recepción de órdenes.

Esta medida local no detecta todos los tipos de mensaje antiguo: una cola podría entregar una muestra vieja ahora mismo. En un sistema real tendrías que definir el contrato temporal, validar timestamps y secuencias, analizar relojes, comunicaciones y la reacción física. El gate del curso sirve para aprender esa discusión, no para certificar seguridad.

## Inyecta un fallo

Arranca solo rover y guard en terminales separadas; no arranques patrol. Publica una orden a 10 Hz como en la práctica 08 y observa `/cmd_vel`. Interrumpe la publicación. Debe volver a cero tras unos 0.5 segundos más el período de evaluación, scheduling y transporte; no afirmamos un límite duro de tiempo real.

Luego vuelve a publicar y termina el proceso rover. Eso corta `/scan`. Observa desde otro `ros2 topic echo /cmd_vel` que el gate pasa a cero por falta de sensor aunque sigan llegando órdenes.

## Ejercicio

Completa `ejercicios/limiter.py` y ejecuta:

```bash
python3 ejercicios/check_limiter.py
```

El contrato permite solo avance entre 0 y 0.35 m/s, giro entre -1 y 1 rad/s, y devuelve cero si cualquiera de los valores no es finito. Escribe al menos un caso que fallaría si la implementación usara solo `min` y `max` sin tratar NaN.

Después añade una prueba de frontera para el watchdog: ¿qué ocurre exactamente con edad 0.5 y con 0.500001? Mira los operadores del contrato y escribe la expectativa antes de ejecutar.

## Comprueba

Entrega resultados de los tests y una explicación de por qué el timeout de comandos no sustituye al de sensores. Verifica que has restaurado el estado del entorno y que ninguna instancia duplicada sigue publicando. Puedes verlas con `ros2 node list` y `ros2 topic info /cmd_vel -v`.
