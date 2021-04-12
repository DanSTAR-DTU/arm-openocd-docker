# ARM OpenOCD Docker
This repo is used to create an Ubuntu container with all the dependencies needed for compiling your project with the *gcc-arm-none-eabi* toolchain and flashing the built project into your microcontroller using *OpenOCD*.

## Prerequisites
In order to build the Dockerfile you will need to install **docker** and **python3+**. Also, I am assuming that your project uses OpenOCD to flash the code into your microcontroller.

## Content
In this repository you can find the *Dockerfile* containing all the instruction to build the docker image with all its dependencies. On the other hand, you have the *aod_launcher.py* that will help you to delete and create images but also stop and run containers without remembering the specific docker commands.

## First time
The firs time you build the image you need to execute the following chain of commands:
```sh
# This command is expected to fail since you should not have a container
# running or an image already created, but you never know.
python3 aod_launcher.py --stop-container --remove-container --remove-image

# Now you need to build the image and run the container
# with your specific USB device and project folder. This step can take several minutes.
# In my case looks like this (Modify your path and serial device accordingly):
python3 aod_launcher.py --device /dev/ttyACM0 \
--project-full-path /home/steven/workspace/danstar/software-dolken \
--build-image --run-container

# Finally get the container console
python3 aod_launcher.py --get-console
```

## Stop container
When you are done working with the container you can call:
```sh
python3 aod_launcher.py --stop-container
```

## Start container and get the console
When you want to start the container again and retrieve its console, use:
```sh
python3 aod_launcher.py --start-container --get-console
```

## Change container configuration
If you changed your project directory or want to change your USB device:
```sh
# First stop and remove the container
python3 aod_launcher.py --stop-container --remove-container
# Re-run the container with the new parameters
# Note that device is ACM1 now and you do not
# have to build the image (--build-image) again
python3 aod_launcher.py --device /dev/ttyACM1 \
--project-full-path /home/steven/workspace/danstar/software-dolken \
--run-container
# Finally, obtain the container console back again:
python3 aod_launcher.py --get-console
```
