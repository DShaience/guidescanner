FROM mcr.microsoft.com/devcontainers/python:1-3.12

RUN apt update -y
RUN apt upgrade -y

RUN pip install --upgrade pip

EXPOSE 8000

RUN  mkdir /guidescanner
WORKDIR /guidescanner

COPY src/requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

ADD src/app app
RUN mkdir output


# TODO: change according to the app's final configuration
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
