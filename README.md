# News Hyperlocalizer

Welcome to the repository for News Hyperlocalizer! 

This README provides instructions on setting up the development server using Docker.

---
## Prerequisites

Before you begin, make sure you have the following installed:

- **Docker**: Docker is used to containerize the development environment. You can create a Docker account and download Docker Desktop from [the official Docker website](https://www.docker.com/products/docker-desktop).
- **GitHub Account**: You will need a GitHub account to access the GitHub Container Registry (GHCR). 
- **Personal Access Token (PAT)**: You will need a Personal Access Token (PAT) to access the GitHub Container Registry (GHCR). You can create a PAT by going to your GitHub account settings, selecting Developer settings, Personal access tokens, and then clicking Generate new token. Make sure to copy the token as you will not be able to see it again. The PAT should have the `read:packages` scope.
- *(Optional)* **OpenAI API Key**: You will need an OpenAI API key to use the story collection and evaluation functionality. You can create an account and get an API key from [the OpenAI website](https://platform.openai.com/).
- *(Optional)* **SmartOcto API Key**: You will need a SmartOcto API key to use the story userneeds evaluation functionality. You may not create one yourself, but can request one from your ContentInsights manager.

---
## Getting Started
 
1. From a console, login to the GitHub Container Registry (GHCR) using your GitHub username and a personal access token (PAT) with the `read:packages` scope. You can create a PAT by going to your GitHub account settings, selecting Developer settings, Personal access tokens, and then clicking Generate new token. Make sure to copy the token as you will not be able to see it again.

    ```bash
    docker login ghcr.io -u <username> -p <token>
    ```
    Replace `<username>` with your GitHub username and `<token>` with the PAT you generated. 
2. Pull the Docker image from the GitHub Container Registry (GHCR) using the following command:

    ```bash
    docker pull ghcr.io/rulfman/news_hyperlocalizer:latest    
    ```
3. Run the Docker container using the following command:

    ```bash
   docker run -e OPENAI_API_KEY=your_openai_api_key -e SMARTOCTO_API_KEY=your_smartocto_api_key --name news_hyperlocalizer_latest -d -p 8000:8000 ghcr.io/rulfman/news_hyperlocalizer:latest
    ```
    Replace `your_openai_api_key` with your OpenAI API key and `your_smartocto_api_key` with your SmartOcto API key. If you do not have a SmartOcto API key, you may leave the environment variable empty.
    If you do not set the API keys on first run, restarting the container will ask you to set them.
    Alternatively, you may manually edit the .env file inside the docker image to set the API keys.

4. Access the development environment by visiting ``http://localhost:8000/`` in your browser.
---
## Using the API

You can visit documentation for the API using swaggerUI at http://localhost:8000/api/swagger/ or using redoc at http://localhost:8000/api/redoc/.

API calls require basic authorization (for now). This means you need to provide a username and password in the authorization header. This needs to be a valid user, which you may create using ``python manage.py createsuperuser``.

Alternatively, in development you may also use the dummy user, with username `api` and password `aP1`.

---
## Questions or Issues?
If you have any questions or encounter any issues while setting up the development environment, please don't hesitate to open an issue in this repository or reach out to **Ruben**.

