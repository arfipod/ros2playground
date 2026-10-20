# 03 · C++17, mensajes generados y CMake

**Objetivo:** consumir en C++ los mensajes que produce Python y extender el nodo. **Tiempo:** 60 minutos.

## Un contrato compartido

Python y C++ no comparten objetos en memoria aquí. Ambos usan tipos generados a partir del mismo contrato de interfaz y se comunican mediante ROS. Esto permite cambiar la implementación de un componente conservando su interfaz, aunque los aspectos temporales y de QoS sigan siendo parte de su comportamiento.

Lee `lab_cpp/src/monitor.cpp` y `lab_cpp/CMakeLists.txt`. `find_package` resuelve dependencias; `ament_target_dependencies` añade lo necesario para usar rclcpp y el mensaje generado; `install` coloca el binario donde `ros2 run` puede encontrarlo. Se declara explícitamente C++17 y avisos de compilación.

El nodo conserva el `SharedPtr` de su suscripción. La lambda captura `this` para acceder al logger. ROS entrega un `ConstSharedPtr` a la muestra: tu callback no tiene que modificarla para observarla. Evita extraer conclusiones generales de latencia o ausencia de copias a partir de este ejemplo básico.

## Ejecuta

```bash
ros2 run lab_py sensor
# Otra terminal:
ros2 run lab_cpp monitor
```

Verás la misma secuencia que en `ros2 topic echo /telemetry`, con el formato del logger C++. Si no recibes nada, revisa el grafo y el topic antes de tocar CMake.

## Ejercicio

Modifica `Monitor` para declarar un parámetro double `low_voltage`, con valor inicial 11.9. En el callback, lee el parámetro y usa `RCLCPP_WARN` cuando la muestra baje del umbral; conserva el log informativo para el resto. Tienes una propuesta de código en `soluciones/GUIA.md`, práctica 03.

```bash
bash scripts/build.sh
source scripts/env.sh
ros2 run lab_cpp monitor --ros-args -p low_voltage:=12.1
```

Detén la instancia anterior antes de lanzar otra con el mismo nombre. En otra terminal, cambia el parámetro mientras corre:

```bash
ros2 param set /monitor low_voltage 11.8
ros2 param get /monitor low_voltage
```

El efecto dinámico viene de leer el valor dentro del callback, no solo de que exista un servicio de parámetros. La primera versión del ejercicio no valida el rango: documenta esa limitación y añade una validación como ampliación.

## Comprueba

Debes poder cambiar la proporción de avisos sin reiniciar el nodo. Una modificación de C++ requiere compilación y reinicio del proceso; una modificación de un parámetro consultado dinámicamente no requiere recompilar. No confundas actualizar el archivo fuente con sustituir el código de un proceso ya arrancado.

**Reto:** detecta saltos de `sequence` sin alertar por la primera muestra. Explica qué haría tu lógica cuando el contador de 32 bits vuelva a cero.

Antes de continuar, guarda los cambios con Git y detén los procesos. La prueba de integración espera los nombres originales de los nodos, así que consérvalos.
