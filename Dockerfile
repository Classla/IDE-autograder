# Use an official Python runtime as a parent image
FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config

CMD ["/usr/sbin/sshd", "-D"]

# Set the working directory in the container
WORKDIR /app

RUN mkdir src
RUN mkdir tests

ENV PYTHONPATH=/app/src:/app/tests

# Install default packages. Unfortunately, this includes pydraw.
RUN pip install --no-cache-dir pydraw 