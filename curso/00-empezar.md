# 00 · Tu laboratorio remoto

**Objetivo:** arrancar el entorno, ver un robot y comprobar que una llamada cambia su comportamiento. **Tiempo:** 30 minutos. **Requisitos:** un Codespace reconstruido con la configuración del repositorio.

## Qué se ejecuta dónde

En tu portátil solo se ejecuta el navegador. El compilador, ROS y el simulador son procesos Linux del contenedor remoto. VS Code web envía tus cambios a ese sistema de archivos; la terminal es una shell de ese Linux. El escritorio noVNC transmite la imagen de las ventanas y devuelve teclado y ratón. No necesitas instalar Docker, ROS, VS Code ni un cliente VNC en el portátil.

La configuración del contenedor está en `.devcontainer/`. El Dockerfile instala las dependencias; `desktop-lite` añade el escritorio; `scripts/setup.sh` compila los tres paquetes y prepara las terminales nuevas. Si cambias las dependencias del Dockerfile, reconstruyes el contenedor. Si cambias código del curso, normalmente basta con recompilar.

## Hazlo

Desde la raíz del proyecto:

```bash
bash scripts/doctor.sh
source scripts/env.sh
ros2 launch lab_py course.launch.py
```

Abre **Ports → 6080 → Open in Browser**, conecta y usa `codespaces` como contraseña. RViz debe mostrar un robot verde y tres obstáculos. Este dibujo es una visualización de mensajes ROS; RViz no está simulando la física.

En una segunda terminal:

```bash
ros2 node list
ros2 topic list -t
ros2 service call /set_mode lab_interfaces/srv/SetMode "{mode: PATROL}"
```

El robot avanza y gira cuando encuentra un obstáculo frontal. Prueba:

```bash
ros2 service call /emergency_stop std_srvs/srv/SetBool "{data: true}"
ros2 service call /set_mode lab_interfaces/srv/SetMode "{mode: OFF}"
ros2 service call /emergency_stop std_srvs/srv/SetBool "{data: false}"
```

La parada queda enclavada hasta que la liberas. Liberarla con el modo en OFF evita que la patrulla reanude la marcha. Si el modo sigue en PATROL, una orden nueva podría reanudarla al liberar el enclavamiento: es parte del comportamiento que analizarás después.

## Ejercicio y comprobación

Anota los nombres de los cinco nodos de la aplicación y qué papel crees que tiene cada uno. Ejecuta `ros2 topic echo /odom --once` y localiza posición y orientación. Guarda una breve nota en `evidencias/00.md`; esta carpeta no se sube automáticamente porque está ignorada. Si quieres conservar evidencias en Git, cambia esa decisión en `.gitignore`.

Has terminado cuando puedes arrancar, iniciar la patrulla, detenerla y cerrar todos los procesos con `Ctrl+C` en la terminal de launch. En el README tienes el itinerario; la siguiente práctica empieza con las demos detenidas.

**Pregunta:** ¿cerrar la pestaña del navegador equivale a apagar la máquina remota? No: controla el Codespace desde GitHub y usa **Stop codespace** al terminar.
