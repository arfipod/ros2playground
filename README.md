# ROS 2 desde el navegador

[![Abrir en GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/arfipod/ros2playground)

Repositorio: [arfipod/ros2playground](https://github.com/arfipod/ros2playground). [Comprobaciones automáticas](https://github.com/arfipod/ros2playground/actions).

Curso práctico en español para un desarrollador de sistemas embebidos con experiencia en C/C++. Entorno de **Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic**, preparado para GitHub Codespaces. Jazzy se elige como base estable del curso, sin afirmar que sea la distribución más reciente.

**12 prácticas, unas 12–16 horas** con ejercicios. Python para experimentar; C++17 para conectar con tu trabajo habitual. Todo el código de referencia está incluido: no hay que descargar modelos ni depender de una plataforma de cursos.

## Lo que aprenderás

Construir y observar un grafo ROS, crear nodos en Python y C++, definir interfaces, elegir QoS, usar servicios y acciones, validar parámetros, organizar launch files, interpretar TF, grabar bags, probar fallos e integrar Gazebo. Terminarás modificando y justificando un pequeño sistema de patrulla.

## Arrancar en Codespaces

### Si los archivos ya están en un repositorio

1. Abre el repositorio en GitHub. **Code → Codespaces → Create codespace**. Elige 4 núcleos si están disponibles.
2. Espera a que se construya el contenedor y termine `postCreateCommand`. La primera creación puede tardar varios minutos y descargar varios GB.
3. Abre una terminal nueva y ejecuta `bash scripts/doctor.sh` desde la raíz.
4. En **Ports**, abre el puerto **6080** en el navegador. Pulsa **Connect** y usa la contraseña de escritorio `codespaces`. Mantén el puerto con visibilidad **Private**: el acceso externo lo protege tu sesión de GitHub.
5. Lee [la práctica 00](curso/00-empezar.md). Para previsualizar Markdown en VS Code: abre el archivo y pulsa `Ctrl+Shift+V`.

### Si has recibido el ZIP y todavía no tienes repositorio

1. Crea un repositorio en tu cuenta de GitHub llamado, por ejemplo, `ros2-browser-course`, inicializado con un README.
2. Abre un Codespace de ese repositorio. Inicialmente usará el entorno por defecto.
3. Sube **este ZIP** a la raíz usando el explorador de VS Code web (arrastrar o **Upload**). El nombre del ZIP de entrega es `Curso_ROS2_Codespaces.zip`.
4. En la terminal, desde la raíz del repositorio:

   ```bash
   unzip -o Curso_ROS2_Codespaces.zip
   git add .devcontainer .github .vscode .gitignore README.md LICENSE curso ejemplos ejercicios soluciones scripts tests ros_ws docs
   git commit -m "Add ROS 2 browser course and development environment"
   git push
   ```

   El ZIP coloca los archivos directamente en la raíz e incluye las carpetas ocultas. Si el navegador cambia el nombre del ZIP, adapta el comando `unzip`.

5. Abre la paleta con `Ctrl+Shift+P` y ejecuta **Codespaces: Rebuild Container**. Después sigue los pasos de arriba.

## Primera demostración

En la terminal del contenedor reconstruido:

```bash
source scripts/env.sh
ros2 launch lab_py course.launch.py
```

Abre el escritorio del puerto 6080: verás RViz, el robot verde, obstáculos y puntos del lidar. En otra terminal:

```bash
ros2 service call /set_mode lab_interfaces/srv/SetMode "{mode: PATROL}"
ros2 service call /emergency_stop std_srvs/srv/SetBool "{data: true}"
```

La primera orden inicia la patrulla; la segunda enclava la parada del ejercicio. Para terminar, `Ctrl+C` en la terminal de launch. El primer simulador es cinemático: **no calcula dinámica ni contactos**, ni garantiza evitar todas las colisiones. Gazebo es una práctica aparte, con física y su propio modelo.

## Itinerario

| Práctica | Tema | Duración orientativa |
|---|---|---:|
| [00](curso/00-empezar.md) | Preparar el puesto y ejecutar el proyecto | 30 min |
| [01](curso/01-grafo.md) | Nodos, topics e inspección con turtlesim | 45 min |
| [02](curso/02-python-interfaces.md) | Workspace, Python e interfaces propias | 60 min |
| [03](curso/03-cpp.md) | Suscriptor C++17 y CMake | 60 min |
| [04](curso/04-qos-executors.md) | QoS, callbacks y executors | 60 min |
| [05](curso/05-servicios-parametros.md) | Servicios y parámetros validados | 45 min |
| [06](curso/06-acciones.md) | Acciones, feedback y cancelación | 45 min |
| [07](curso/07-launch-bags.md) | Launch, nombres y rosbag | 60 min |
| [08](curso/08-tf-rviz.md) | TF, odometría, lidar y RViz | 60 min |
| [09](curso/09-fallos-tests.md) | Watchdogs, fallos y pruebas | 60 min |
| [10](curso/10-gazebo.md) | Robot diferencial en Gazebo | 60 min |
| [11](curso/11-proyecto.md) | Proyecto final y revisión | 120 min |

Puedes repartirlo en sesiones de 30–45 minutos. Cada práctica contiene objetivos observables, una explicación, comandos, ejercicios y criterios para saber si has terminado. Las soluciones están separadas en `soluciones/`.

## Comprobaciones y límites

```bash
python3 -m unittest discover -s tests -v       # Sin ROS: algoritmos y casos de fallo
bash scripts/doctor.sh                      # Dentro del contenedor
# Con todas las demos detenidas, en una terminal NUEVA:
ROS_DOMAIN_ID=73 python3 scripts/check_runtime.py
```

El último comando arranca y apaga sus propios nodos y escribe `/tmp/ros2-course-runtime.log`. El workflow `.github/workflows/ci.yml` compila los tres paquetes y ejecuta pruebas de algoritmos y comunicación ROS. No comprueba el escritorio ni el rendimiento de Gazebo.

Codespaces no ofrece actualmente sus antiguas máquinas GPU. La simulación ligera reduce esa dependencia; RViz también requiere que funcione OpenGL por software. Gazebo y su GUI pueden ir más lentos. Si falla la GUI, su servidor se puede ejecutar con `gui:=false` y observar la odometría. El acceso desde una red corporativa depende de que permita GitHub Codespaces, sus dominios de puertos y WebSockets.

La cuota gratuita depende de tu plan y consumo: comprueba **Settings → Billing**. Parar el Codespace detiene el cómputo, pero no elimina el almacenamiento. Guarda tus cambios en GitHub antes de borrar un Codespace. Este proyecto contiene material didáctico propio; la lógica de parada no es un sistema de seguridad para hardware real.

## Estructura

- `curso/`: lecciones y ejercicios guiados.
- `ros_ws/src/lab_interfaces`: mensaje `Telemetry` y servicio `SetMode`.
- `ros_ws/src/lab_py`: sensor, simulador, patrulla, gate, launch, RViz y mundo SDF.
- `ros_ws/src/lab_cpp`: monitor C++17.
- `ejemplos/`: cliente de acciones; `ejercicios/` y `soluciones/`: código para completar y referencias.
- `docs/`: diagnóstico, fuentes y estado de validación.

El código está disponible bajo MIT. Las versiones de distribución están fijadas; las etiquetas de contenedor, paquetes apt y feature de escritorio reciben actualizaciones. No se promete reproducibilidad binaria byte a byte.
