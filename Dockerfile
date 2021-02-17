# File name: AOD Dockerfile
# Author: Steven Macías
# Github: StevenMacias
# Date created: 12/02/2021
# Date last modified: 13/02/2021

FROM ubuntu:latest

# Environment variables for binaries
ENV PATH="/opt/gcc-arm-none-eabi-10-2020-q4-major/bin:$PATH"
ENV PATH="/opt/openocd/bin:$PATH"

# Avoid being asked during installation of packages about timezone
ENV TZ=Europe/Copenhagen
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
  echo $TZ > /etc/timezone

# Install official packages
RUN apt-get update && apt-get install -y \
  cmake \
  curl \
  nano \
  git \
  make \
  libtool \
  pkg-config \
  autoconf \
  automake \
  texinfo \
  libusb-1.0-0 \
  libusb-1.0.0-dev \
  libftdi-dev \
  libhidapi-dev \
  pkg-config \
  npm \
  zsh \
  locales

# Set the locale to en_US
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install ARM toolchain
#   Download the toolchain using curl
RUN curl https://armkeil.blob.core.windows.net/developer/Files/downloads/gnu-rm/10-2020q4/gcc-arm-none-eabi-10-2020-q4-major-x86_64-linux.tar.bz2 \
  -o gcc-arm-none-eabi-10-2020-q4-major-x86_64-linux.tar.bz2
#   Extract the toolchain and move it to /opt
RUN tar -xjvf gcc-arm-none-eabi-10-2020-q4-major-x86_64-linux.tar.bz2 && \
  mv gcc-arm-none-eabi-10-2020-q4-major /opt/ && \
  rm -rf /gcc-arm-none-eabi-10-2020-q4-major-x86_64-linux.tar.bz2

# Install OpenOCD using xpack
RUN npm install --global xpm@latest && xpm install --global @xpack-dev-tools/openocd@0.10.0-15.1 --verbose \
  && mkdir -p /opt/openocd \
  && mv /root/.local/xPacks/@xpack-dev-tools/openocd/0.10.0-15.1/.content/* /opt/openocd/
# Define shared volume
VOLUME /workspace

# Fancy terminal and theme config (It insstalls OhMyZsh and types yes to make zsh as default terminal)
# Also modifies the .zshrc to change the default theme
RUN sh -c '/bin/echo -e “yes\n” | sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"' && \
sed -i 's/^\(ZSH_THEME\s*=\s*\).*$/\1\"linuxonly\"/' /root/.zshrc
