#!/usr/bin/env bash
set -eo pipefail
cd "$(dirname "$0")/.."
if [ ! -f /opt/ros/jazzy/setup.bash ]; then
  echo 'Falta ROS Jazzy. Ejecuta Codespaces: Rebuild Container.'; exit 1
fi
source scripts/env.sh
printf 'ROS: %s | DISPLAY: %s | DOMAIN: %s\n' "$ROS_DISTRO" "${DISPLAY:-sin-escritorio}" "$ROS_DOMAIN_ID"
ros2 pkg prefix lab_py
ros2 pkg prefix lab_cpp
ros2 pkg prefix ros_gz_sim
ros2 interface show lab_interfaces/msg/Telemetry
python3 -m unittest discover -s tests -v
echo 'Diagnóstico básico correcto. Para comprobar ROS en ejecución: python3 scripts/check_runtime.py'
