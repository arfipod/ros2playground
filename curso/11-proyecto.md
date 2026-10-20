# 11 · Proyecto final: patrulla supervisada

**Objetivo:** modificar, verificar y explicar una aplicación ROS pequeña. **Tiempo:** unas dos horas; más si haces las ampliaciones. Usa la simulación ligera, no el mundo Gazebo, y para todas las instancias anteriores.

## Punto de partida

El proyecto ya funciona como referencia. No se trata solo de arrancarlo: tendrás que cambiarlo y aportar evidencia de las decisiones. El flujo previsto es `patrol → /cmd_vel_raw → guard → /cmd_vel → rover`; el lidar vuelve desde rover a patrol y guard. Sensor y monitor forman una rama de telemetría independiente.

Patrol elige avanzar o girar según el obstáculo frontal. No calcula rutas ni garantiza cobertura del mapa. Guard aplica límites, caducidad de recepción y un enclavamiento. Rover integra una pose ideal y calcula escaneos geométricos. Cada componente hace una parte explícita del trabajo; ninguna etiqueta de arquitectura sustituye comprobar el comportamiento.

## Requisitos de tu versión

1. Conserva OFF y PATROL y rechaza modos desconocidos sin cambiar el estado anterior.
2. Añade `obstacle_distance` con validación inicial y dinámica como en la práctica 05.
3. Añade un estado observable: publica un `std_msgs/msg/String` en `/patrol_state` con `OFF`, `ADVANCE`, `TURN` o `NO_SCAN`. Documenta si emites por ciclo o solo al cambiar.
4. Añade al monitor C++ el umbral de voltaje de la práctica 03.
5. Mantén el gate como único publicador previsto de `/cmd_vel` en la aplicación ligera. No conectes patrol directamente al simulador.
6. Añade al menos tres pruebas nuevas: frontera del timeout, umbral frontal y un dato no finito.
7. Documenta cómo parar, resetear y reanudar sin dejar una orden no deseada activa.

## Plan de trabajo

Dedica primero 15 minutos a escribir qué archivo cambiarás y cómo observarás cada requisito. Implementa en pasos pequeños y comprueba los algoritmos antes de arrancar la GUI. Después ejecuta la prueba de integración y haz una prueba manual de patrulla, parada enclavada y pérdida de sensor.

Graba unos 20–30 segundos de topics si te ayuda a comparar. Anota los parámetros y el commit que usaste. Sin esas condiciones, dos gráficas de odometría no permiten saber si estabas comparando el mismo sistema.

Para cerrar el ciclo:

```bash
bash scripts/build.sh
source scripts/env.sh
python3 -m unittest discover -s tests -v
ROS_DOMAIN_ID=73 python3 scripts/check_runtime.py
git diff
git add ros_ws tests
git commit -m "Complete supervised patrol exercises"
git push
```

No subas evidencias o datos que no quieras publicar. Un repositorio personal puede configurarse privado; el curso no necesita material de tu empresa.

## Criterios de revisión

| Aspecto | Evidencia para aprobar |
|---|---|
| Construcción | Los tres paquetes compilan y los nodos se resuelven desde una terminal nueva. |
| Interfaces | Explicas el mensaje propio, el servicio y por qué usas topics para órdenes continuas. |
| QoS | Reproduces y diagnosticas la incompatibilidad de la práctica 04. |
| Configuración | Los valores inválidos se rechazan y los aceptados afectan al controlador. |
| Fallos | Muestras la parada por pérdida de órdenes, pérdida de sensor y enclavamiento. |
| Visualización | Interpretas odom, base_link y lidar sin inventar un frame map. |
| Pruebas | Pasan las pruebas existentes y las nuevas aportan casos distintos. |
| Comunicación | Describes al menos tres limitaciones reales de tu aplicación. |

## Si quieres orientarlo a autonomía UAS

Como ampliación conceptual, sustituye la patrulla planar por un gestor de misión con estados de espera, ejecución y aborto; escribe antes el contrato de comandos, telemetría y tiempos. No hace falta añadir PX4 o un simulador de vuelo para aprender el diseño de interfaces. El salto a un autopiloto real exige otras herramientas y validaciones que no cubre este curso.

Otros siguientes pasos razonables: un servidor de acciones propio, nodos lifecycle, pruebas `launch_testing`, URDF y `robot_state_publisher`, Nav2 con localización y mapas, y análisis de ejecutores y tiempo real. Son temas posteriores, no capacidades que ya tenga esta referencia.
