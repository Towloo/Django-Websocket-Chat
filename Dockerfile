FROM python:3.8.11-slim-buster

# Env & Arg variables
ARG USERNAME=towloo
ARG USERPASS=passpass

# Set the working directory to /app
WORKDIR /app

# Apt update & apt install required packages
# whois: required for mkpasswd
RUN apt update && apt -y install whois g++ gcc libc-dev make

# Add a non-root user & set password
RUN useradd -ms /bin/bash $USERNAME

# Set password for non-root user
RUN usermod --password $(echo "$USERPASS" | mkpasswd -s) $USERNAME

# Remove no-needed packages
RUN apt purge -y whois && apt -y autoremove && apt -y autoclean && apt -y clean

# Change to non-root user
USER $USERNAME
WORKDIR /home/$USERNAME
ENV PATH="/home/$USERNAME/.local/bin:${PATH}"

# Install the dependencies
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY . /app

# Set volumes
WORKDIR /app
EXPOSE 8000

USER root
RUN chmod +x /app/bash.sh

USER $USERNAME

# Run entrypoint
CMD ["/app/bash.sh"]