# 02 · Tu primer componente en Python

**Objetivo:** entender cómo se construye el workspace y añadir un consumidor de telemetría. **Tiempo:** 60 minutos.

## Del archivo al ejecutable

`ros_ws/src/` contiene paquetes. `package.xml` declara identidad y dependencias; `setup.py` registra recursos y ejecutables Python. `colcon build` genera `build`, `install` y `log`. Al hacer `source` del setup de ROS cargas la distribución; al cargar el setup de `install` añades el overlay del curso. Una terminal que no conoce el overlay no puede resolver `lab_py` aunque el archivo exista.

El mensaje propio está en `lab_interfaces/msg/Telemetry.msg`. Su interfaz se convierte en clases Python y C++ durante la compilación. El header aporta marca temporal y frame, mientras `sequence` permite observar saltos. Una secuencia discontinua no prueba por sí sola un fallo: puedes haber empezado a escuchar después de la primera muestra.

## Ejecuta e inspecciona

```bash
bash scripts/build.sh
source scripts/env.sh
ros2 interface show lab_interfaces/msg/Telemetry
ros2 run lab_py sensor
```

En otra terminal:

```bash
ros2 topic echo /telemetry
ros2 topic hz /telemetry
```

Lee `ros_ws/src/lab_py/lab_py/sensor.py`. El constructor crea un publicador y un timer; `tick` fabrica una muestra y la publica. `rclpy.spin` atiende los callbacks del executor. La referencia del timer se conserva en el objeto; evita callbacks largos que bloqueen el procesamiento de otros eventos.

`period` se lee al construir el nodo y se usa para crear el timer. Este ejemplo no recrea el timer cuando cambia ese parámetro: para cambiar realmente su frecuencia, reinicia con un override. Más adelante usarás parámetros que sí tienen efecto dinámico.

## Escribe la alarma

Abre `ejercicios/battery_alarm.py`. Completa el callback para publicar un `std_msgs/msg/String` en `/battery_alarm` cuando el voltaje sea inferior a 11.9 V. Incluye la secuencia y el voltaje en el texto. No cambies el sensor para provocar el caso: la señal de ejemplo ya oscila alrededor de 12 V.

```bash
python3 ejercicios/battery_alarm.py
# En otra terminal:
ros2 topic echo /battery_alarm
```

El script se ejecuta desde el repositorio; no está registrado como ejecutable de un paquete. Ese es un atajo didáctico. Para un componente distribuible deberías añadirlo al paquete, registrar un entry point y recompilar.

## Comprueba

La alarma debe emitir mensajes solo cuando la muestra baja del umbral. Sube el umbral a 12.3 y razona por qué dispara con todas las muestras. Después restaura 11.9. Si ves `ModuleNotFoundError: lab_interfaces`, carga `scripts/env.sh` en esa misma terminal; no lo arregles instalando una librería de PyPI con el mismo nombre.

**Reto:** añade una histéresis: activa por debajo de 11.9 V y desactiva por encima de 12.1 V. Explica la diferencia entre publicar el estado en cada muestra y publicar solo las transiciones.

Referencia ejecutable: `python3 soluciones/battery_alarm.py`. Antes de seguir, para los procesos de esta práctica.
