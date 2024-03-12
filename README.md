# FastAPI Reverse File Server - Learn, Build, Dockerize

## 🚀 Introduction

**Welcome to a journey of learning and exploration with FastAPI and Docker!** <br>
This project isn't just about building a backend server; it's a hands-on adventure into the world of file handling and API development. This is the playground for you to learn FastAPI and Docker!

### Why This Project?

- **Learn FastAPI**: FastAPI is a modern, fast web framework for building APIs with Python. It's gaining traction for its speed and ease of use. What better way to learn it than by hands-on experience?
- **Master File Handling**: Handling different types of files (images, audio, text) can be tricky. This project offers a practical way to learn these skills.
- **Dockerize Your Application**: Ever wondered how to containerize your Python applications? This project will show you how to use Docker to build, run, and deploy your FastAPI app.

## 🌟 Features

- **Versatile File Handling**: Learn to process images, audio, and text.
- **Security with Authentication**: Implement token bearer authentication for secure API access.
- **Docker Integration**: Step-by-step guidance on containerizing your FastAPI application.

## 🐳 DockerHub

You can run this project direct from [DockerHub](https://hub.docker.com/repository/docker/studeni/simple-backend/general), to fast check how everything works and afterwards try it by yourself and maybe upgrade ☄️

## 🛠 Getting Started

### Prerequisites

Before you embark on this journey, make sure you have the following:
- Docker installed on your machine.
- Basic understanding of Python.
- Curiosity and enthusiasm for learning new things!



### Installation and Usage

1. **Clone the Magical Repository**:
   ```bash
   git clone https://github.com/milistu/simple-backend.git
   ```
   ```bash
   cd simple-backend
   ```
3. **Build Docker image**:
    ```bash
    docker build -t simple-backend .
    ```

4. **Check if port 1000 is in use**:

    On **Linux** and **macOS**:
    ```bash
    sudo lsof -i :1000
    ```
    On **Windows**:
    ```
    netstat -ano | findstr :1000
    ```
    If you get output from these commands, it means something is running on port 1000. The output will typically include the process ID (PID) of the process using the port.

    In my case my `1000` port is **free**.

    _**Note**: If your port 1000 is not available you can change the `Dockerfile` and replace 1000 with your available port OR simply set `PORT` variable when running Docker Container!_

4. **Run container**:

    _**Note**: set different PORT if needed._

    ```bash
    docker run --rm -it -e PORT=1000 -p 127.0.0.1:1000:1000 simple-backend
    ```

5. **Test our server**:

    You can test the server through `backend-test.ipynb` notebook or with Swagger.

    **Swagger**:

    Open the link in the browser
    ```
    http://0.0.0.0:1000/docs
    ```

    Go to `Authorize` and input your **username** and **password** to get the required token. <br>
    In our example username:
    ```
    username=johndoe
    password=BestPassword!
    ```

    Now you can test one of the end-points (eg. image, audio, text).