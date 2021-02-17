#!/usr/bin/env python
'''
    File name: aod_launcher.py
    Author: Steven Macías
    Github: StevenMacias
    Date created: 12/02/2021
    Date last modified: 13/02/2021
    Python Version: 3.9.1
'''
# Imports
from sys import platform
import subprocess
import argparse
import logging
import time
import os

# Config
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
operating_system = None
args = None

# Global variables
container_name = "danstar_container"
image_name = "danstar"
version = "1.0"
cmd_stop_container = "docker stop "+ container_name
cmd_start_container = "docker start "+ container_name
cmd_remove_container = "docker rm "+ container_name
cmd_remove_image = "docker rmi "+ image_name+":"+version
cmd_docker_build = "docker build -t "+image_name+":"+version+" . "
args_device_docker_linux = "--device=%s --privileged -v /dev/serial:/dev/serial"
args_device_docker_windows = "--device=%s"
cmd_run_container = "docker run -itd %s --volume=%s:/workspace --name %s %s:%s"""
cmd_get_console = "docker exec -it %s /bin/zsh" % container_name

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    # from whichcraft import which
    from shutil import which
    return which(name) is not None

def detectOperatingSystem():
    global operating_system
    if platform == "linux" or platform == "linux2":
        # linux
        operating_system="linux"
        logging.info("Linux OS Detected")
    elif platform == "darwin":
        # OS X
        operating_system="mac"
        logging.info("Mac OS Detected")
    elif platform == "win32":
        # Windows...
        operating_system="windows"
        logging.info("Windows OS Detected")

def argsDefinition():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', required=False, help="Write your serial port. \
    For instance, COMX (Windows) or /dev/ttyACMX (Linux/Mac) where X is a number.")

    parser.add_argument('--project-full-path', required=False, help="Write the full path of \
    the project that you want to send to the docker container. It will be placed in the \
    worksace directory inside the container.")

    parser.add_argument('--stop-container', action='store_true',
        help="Stop the docker container")

    parser.add_argument('--start-container', action='store_true',
        help="Start the docker container")

    parser.add_argument('--remove-image', action='store_true',
        help="Remove the docker image")

    parser.add_argument('--remove-container', action='store_true',
        help="Remove the docker container")

    parser.add_argument('--build-image', action='store_true',
        help="Build the docker image using the Dockerfile")

    parser.add_argument('--run-container', action='store_true',
        help="Run the container sharing the --device and creating a volume for --project-ful-path")

    parser.add_argument('--get-console', action='store_true',
        help="Get container console")
    args = parser.parse_args()
    logging.debug(args)

def executeDockerCommands():
    logging.info("Docker found in PATH")
    if args.stop_container:
        logging.info("--- Stop Docker Container ---")
        cmd = cmd_stop_container
        logging.info(cmd)
        os.system(cmd)
    if args.start_container:
        logging.info("--- Start Docker Container ---")
        cmd = cmd_start_container
        logging.info(cmd)
        os.system(cmd)
    if args.remove_container:
        logging.info("--- Remove Docker Container ---")
        cmd = cmd_remove_container
        logging.info(cmd)
        os.system(cmd)
    if args.remove_image:
        logging.info("--- Remove Docker Image ---")
        cmd = cmd_remove_image
        logging.info(cmd)
        os.system(cmd)

    if args.build_image:
        logging.info("--- Build Docker Image ---")
        cmd = cmd_docker_build
        logging.info(cmd)
        os.system(cmd)

    if args.run_container:
        logging.info("--- Run Docker Image ---")

        # Linux / Mac
        if operating_system == "linux" or operating_system == "mac":
            if args.device:
                args_device_docker_linux_filled = args_device_docker_linux % args.device
            else:
                args_device_docker_linux_filled = ""
            cmd = cmd_run_container % (args_device_docker_linux_filled, args.project_full_path, container_name, image_name, version)
        # Windows
        else:
            args_device_docker_windows_filled = args_device_docker_windows % args.device
            cmd = cmd_run_container % (args_device_docker_windows_filled, args.project_full_path, container_name, image_name, version)
        logging.info(cmd)
        os.system(cmd)
    if args.get_console:
        logging.info("--- Get Container Console ---")
        cmd = cmd_get_console
        logging.info(cmd)
        os.system(cmd)

def main():
    detectOperatingSystem()
    argsDefinition()
    if is_tool("docker"):
        executeDockerCommands()
    else:
        logging.error("Docker NOT found in PATH")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
