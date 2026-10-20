# 04 · Cuando el tipo coincide y aun así no llega nada

**Objetivo:** provocar y explicar una incompatibilidad de QoS y reconocer bloqueos de callbacks. **Tiempo:** 60 minutos.

## QoS forma parte de la interfaz

Una suscripción solicita unas garantías y el publicador ofrece otras. Para fiabilidad, un publicador best effort no puede satisfacer un suscriptor que exige reliable. Un publicador reliable sí puede atender a un suscriptor best effort. Esto explica por qué dos nodos pueden descubrirse, usar el mismo topic y tipo, y no intercambiar muestras.

`depth` limita la historia que se conserva en las colas asociadas a una política keep last. No equivale a un período ni a un timeout. `transient_local` permite conservar historia para suscriptores tardíos compatibles mientras el publicador está disponible; no debe confundirse con escribir un archivo persistente.

## Provoca el caso

Detén todas las instancias de sensor y monitor. Terminal A:

```bash
ros2 run lab_py sensor --ros-args -p best_effort:=true
```

Terminal B:

```bash
ros2 run lab_cpp monitor
```

El monitor de referencia exige reliable. Inspecciona:

```bash
ros2 topic info /telemetry -v
ros2 topic echo /telemetry --qos-reliability best_effort
```

La CLI con best effort puede recibir aunque el monitor no lo haga. Ahora detén el sensor y reinícialo sin el override: el monitor debería recibir. Apunta las cuatro combinaciones reliable/best effort y el resultado esperado antes de consultar la guía.

## Callbacks y planificación

Los nodos Python del curso usan el executor monohilo por defecto. Un callback largo retrasa otros callbacks de ese executor. Para observarlo, añade temporalmente `time.sleep(0.8)` al principio de `Sensor.tick` y ejecuta el sensor con `period:=0.1`. Mide la salida con `ros2 topic hz /telemetry` durante unos segundos. El período configurado no elimina el tiempo que consume el trabajo.

Restaura el archivo al terminar. Si usas `--symlink-install`, cambios en módulos Python instalados mediante enlaces suelen verse al reiniciar el proceso; recompila si has cambiado entry points, interfaces o archivos instalados.

Un executor multihilo no vuelve concurrente cualquier código por arte de magia: intervienen los callback groups y la seguridad de los datos compartidos. Como regla de diseño, evita esperar de forma bloqueante dentro de un callback a un resultado que necesita ese mismo executor. El cliente de acciones de otra práctica espera desde la función principal, que sí permite girar el executor.

## Comprueba

Has terminado cuando puedes explicar el caso sin atribuirlo a firewall o latencia, restaurar los archivos y obtener telemetría en C++. El simulador publica lidar con perfil de datos de sensor; sus consumidores usan un perfil compatible.

**Pregunta:** ¿reliable garantiza que tu callback procese la muestra antes de un plazo? No. Fiabilidad de transporte y cumplimiento de plazos son propiedades diferentes.
