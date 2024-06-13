# News Hyperlocalizer backend

Welcome to the **backend** repository for the News Hyperlocalizer challenge!

The **front-end** repository can be found at :link:[News Hyperlocalizer Front-End](https://github.com/roydebiejs/news-hyperlocalizer).

---
## :pushpin:Prerequisites

For using the repository, make sure you have the following...

- **Docker**: Docker is used to containerize the (development) environment. You can create a Docker account and download Docker Desktop from :link:[the official Docker website](https://www.docker.com/products/docker-desktop).
- *(Optional)* **OpenAI API Key**: You will need an OpenAI API key and sufficient credit to use the story collection and evaluation functionality. You can create an account and get an API key from :link:[the OpenAI website](https://platform.openai.com/).
- *(Optional)* **SmartOcto API Key**: You will need a SmartOcto API key to use the story userneeds evaluation functionality. You may not create one yourself, but can request one from your ContentInsights manager.

For development, you will also need...

- **GitHub Account**: You will need a GitHub account to make changes to the codebase and access the GitHub Container Registry (GHCR). 
- **Personal Access Token (PAT)**: You will need a PAT to push changes in the docker image to the GitHub Container Registry (GHCR). You can create a PAT by going to your GitHub account settings, selecting Developer settings, Personal access tokens, and then clicking Generate new token. Make sure to copy the token as you will not be able to see it again. The PAT should have the `delete:packages, read:org, read:repo, write:packages` scopes.

---
## :gear:Getting Started
You can either use the repository entirely through docker by pulling and running the image, or by cloning the repository and building the image locally. Below instructions explain both options.

### Getting started using Docker
 
1. Pull the Docker image from the GitHub Container Registry (GHCR) using the following command:

    ```bash
    docker pull ghcr.io/rulfman/news_hyperlocalizer:latest    
    ```
   
2. Run the Docker container using the following command:

    ```bash
   docker run -e OPENAI_API_KEY=your_openai_api_key -e SMARTOCTO_API_KEY=your_smartocto_api_key --name news_hyperlocalizer_backend -d -p 8000:8000 ghcr.io/rulfman/news_hyperlocalizer:latest
    ```
    Replace `your_openai_api_key` with your OpenAI API key and `your_smartocto_api_key` with your SmartOcto API key. If you do not have either keys, you may leave the environment variable empty, but do note that functionality will not work properly.
    Alternatively, you may manually edit the .env file inside the docker image to set the API keys.

### Getting started using a clone of the repository

1. Clone the repository.
   ```bash
   git clone https://github.com/RUlfman/news_hyperlocalizer.git
   cd news_hyperlocalizer
   ```

2. Edit or create the :file_folder:`.env` file in the root directory of the repository to set your OpenAI API and SmartOcto API keys. If you do not have a SmartOcto API key, you may leave the environment variable empty. If no :file_folder:`.env` file exists, you may create one from the template provided in :file_folder:`.env.example`.

3. Start the development server.
   ```bash
   docker-compose up --build
   ```

---
## :hammer_and_wrench:Usage
After getting started, while the docker container is running, you can visit the development server at :link:[``http://localhost:8000/``](http://localhost:8000/) in your browser. The (development) server will automatically detect and reload if you make changes to the codebase. 

### Using the API

You can visit documentation for the API using swaggerUI at :link:[``http://localhost:8000/api/swagger/``](http://localhost:8000/api/swagger/) or using redoc at :link:[``http://localhost:8000/api/redoc/``](http://localhost:8000/api/redoc/).

API calls require :lock:_basic authorization_ for simple GET requests and :lock:_token authentication_ for more advanced (POST, UPDATE, DELETE, etc) requests. For both basic and token authentication a valid user is required. For development purposes you may use the dummy API-user which is automatically created, with username :key:`api` and password :key:`aP1`. You can create additional (more secure) user credentials through the admin tools at :link:[``http://localhost:8000/admin/``](http://localhost:8000/admin/). Note that the admin tools require a superuser login, which you may create using the terminal command ``python manage.py createsuperuser``.

### Developing

The codebase is written in Python, using the Django framework. It is highly recommended you use a virtual environment whenever you're working with Python, even when using Docker to isolate the project files. You may initiate the virtual environment using ``.\venv\Scripts\activate``. However, do not set the docker container itself to run or use a virtual environment, as this _may_ cause issues with building the image.

If during development you change the dependencies of the project, remember to update the :file_folder:`requirements.txt` file (which you may automate using ``pip freeze > requirements.txt`` from the terminal). Without updating the requirements file, while they may be installed locally, they will not be included in the docker container when rebuilding it. Note that these type of changes to the codebase require a rebuild of the docker image, and will not be automatically applied during a reload of the server.

---
## :construction:Troubleshooting
- If you experience problems with installation, please make sure Docker is running on your machine
- If you experience any problems with the backend, please make sure Docker and the backend container are running on your machine.
- By default, the app runs on port 8000. Ensure that no other services are running on port 8000 to avoid port conflicts.
- If the collection service fails, it may mean the chromium browser and chromedriver failed to install inside the container. You may manually install these inside the container to resolve the issue.
