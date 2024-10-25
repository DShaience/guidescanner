FROM mcr.microsoft.com/devcontainers/python:1-3.12

RUN apt update -y
RUN apt upgrade -y

EXPOSE 8000

RUN  mkdir /gutguardian
WORKDIR /gutguardian

# TODO: change according to the app's final configuration
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
