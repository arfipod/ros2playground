# Fuentes técnicas y decisiones

Consultadas el 20 de octubre de 2026. El material y los ejemplos de este proyecto son redacción y código propios; las fuentes se usan como documentación técnica de referencia.

- [GitHub Codespaces: qué es](https://docs.github.com/en/codespaces/about-codespaces/what-are-codespaces): contenedor Linux remoto y acceso web.
- [Dev Containers desktop-lite](https://github.com/devcontainers/features/blob/main/src/desktop-lite/README.md): escritorio Fluxbox y noVNC, puerto 6080, shared memory y soporte Debian/Ubuntu.
- [Facturación de Codespaces](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces): horas de núcleo y almacenamiento. La cuota no se interpreta como horas de reloj para cualquier máquina.
- [Retirada de máquinas GPU de Codespaces](https://github.blog/changelog/2025-08-01-upcoming-deprecation-of-gpu-machine-type-in-codespaces/): motivo para ofrecer simulación ligera y no prometer rendimiento 3D.
- [Tutoriales ROS 2 Jazzy](https://docs.ros.org/en/jazzy/Tutorials.html): itinerario de referencia para CLI, bibliotecas cliente, parámetros y launch. El sitio puede mostrar protección anti-bot en algunos entornos.
- [Documentación ROS en su repositorio](https://github.com/ros2/ros2_documentation/tree/jazzy/source/Tutorials): alternativa de consulta del material fuente.
- [Ejemplos oficiales rclpy](https://github.com/ros2/examples/tree/jazzy/rclpy) y [rclcpp](https://github.com/ros2/examples/tree/jazzy/rclcpp): organización de nodos de ejemplo.
- [Imágenes ROS mantenidas por OSRF](https://github.com/osrf/docker_images): relación entre imágenes base y metapaquetes de escritorio.
- [Compatibilidad ROS–Gazebo](https://gazebosim.org/docs/latest/ros_installation/): pareja Jazzy–Harmonic y uso de paquetes ros_gz.
- [Gazebo Harmonic: mover un robot](https://gazebosim.org/docs/harmonic/moving_robot/): plugin DiffDrive y su interfaz de comandos.
- [DiffDrive API de Gazebo Sim 8](https://gazebosim.org/api/sim/8/classgz_1_1sim_1_1systems_1_1DiffDrive.html): parámetros de ruedas, topics y frames.
- [ros_gz_bridge](https://github.com/gazebosim/ros_gz/tree/jazzy/ros_gz_bridge): conversiones de mensajes y configuración YAML.

## Alcance

Fundamentos de ROS 2 y un proyecto de integración pequeño. No incluye certificación, integración de hardware Airbus, determinismo de tiempo real, Nav2 completo, SLAM, PX4 ni un servidor de acciones propio. Se trabaja exclusivamente con datos sintéticos del curso.
