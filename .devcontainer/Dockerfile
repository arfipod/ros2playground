FROM ros:jazzy-ros-base
SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo git ripgrep unzip less nano curl mesa-utils \
    build-essential cmake python3-colcon-common-extensions python3-pytest \
    ros-jazzy-rviz2 ros-jazzy-turtlesim ros-jazzy-rqt-graph \
    ros-jazzy-ros-gz ros-jazzy-tf2-tools ros-jazzy-teleop-twist-keyboard \
    && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home --shell /bin/bash vscode \
    && echo 'vscode ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode
ENV DEBIAN_FRONTEND=dialog
