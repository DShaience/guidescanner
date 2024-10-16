FROM mcr.microsoft.com/devcontainers/python:1-3.12

RUN apt update -y
RUN apt upgrade -y

# This entire section is for installing azure cli inside the container
# Leaving it as an example
# RUN apt install ca-certificates curl apt-transport-https lsb-release gnupg -y
# RUN curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/microsoft.gpg > /dev/null
# RUN AZ_REPO=$(lsb_release -cs) && \
#     echo "AZ_REPO=$AZ_REPO" >> /etc/environment && \
#     echo "deb [arch=`dpkg --print-architecture` signed-by=/etc/apt/trusted.gpg.d/microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" | tee /etc/apt/sources.list.d/azure-cli.list
# # Source the /etc/environment to make the variable available in the shell sessions
# RUN . /etc/environment
# # Explicitly declare the environment variable for subsequent layers (optional)
# ENV AZ_REPO=${AZ_REPO}
# RUN apt update
# RUN apt install azure-cli -y
# End azure-ali installation here


RUN  mkdir /gutguardian
WORKDIR /gutguardian

