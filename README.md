# News Hyperlocalizer

Welcome to the repository for News Hyperlocalizer! 

This README provides instructions on setting up the development environment using Docker.

---
## Prerequisites

Before you begin, make sure you have the following installed:

- **Docker**: Docker is used to containerize the development environment. You can create a Docker account and download Docker Desktop from [the official Docker website](https://www.docker.com/products/docker-desktop).

---
## Getting Started

Follow these steps to set up the development environment:

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/RUlfman/news_hyperlocalizer.git
cd news_hyperlocalizer
````

### Step 2: Build the Docker Image

Build the Docker image using the provided Dockerfile. Run the following command in the root directory of the project:

```bash
docker build -t news_hyperlocalizer .
````

### Step 3: Run the Docker Container

Once the Docker image is built, you can run a Docker container and mount the project directory based on that image. Use the following command:

```bash
docker run -p 8000:8000 -v "[/path/to/your/django/project]:/app" news_hyperlocalizer
````

Note: replace `[/path/to/your/django/project]` with the root directory of the repository (the same folder where the `Dockerfile` file is located). Do **not** replace the `:/app part`, or it will not work.

This command will mount your project directory, and start the Django development server inside the Docker container, and your app will be accessible at http://localhost:8000 in your web browser.

### Step 4: Configure your IDE

The last step is configuring your IDE. I'm going to assume you're using PyCharm. Other IDE's should have similar workflows.

1. Open PyCharm, Go to "File" > "Settings" > "Project: YourProjectName" > "Python Interpreter".
2. Click "Add Interpreter" and choose Docker.
3. PyCharm should have automatically selected everything you need, except the server. This is `unix:///var/run/docker.sock` for Unix/Linux or `tcp://localhost:2375` for Windows with Docker Desktop.
4. Click OK. PyCharm will call the build command. Make sure your docker container is running (step 3). Be patient, the build may take a few minutes to complete!
5. After PyCharm has run its build, you should now be able to set the interpreter, this should be automatically set to something like `/usr/local/bin/python`.

**That's it!** You have now mounted your docker image, and configured your IDE. Any changes made to the codebase will now automatically be applied to the docker image, and will be viewable at http://localhost:8000 in your web browser. 

### Additional Commands
- To stop the Docker container, press `Ctrl + C` in the terminal where it's running.
- To restart the Docker container, use the ```docker run``` command again.
- To remove the Docker container, use the ```docker rm``` command followed by the container ID or name.
- To remove the Docker image, use the ```docker rmi``` command followed by the image ID or name.

### Development Workflow
1. Pull changes from the Git remote repository.
2. (Re)Build the docker image. **Note**: this is *only* necessary if there were changes to dependencies!
3. Run the docker image. After you run it the first time with commands, it should be visible in the Docker Desktop app (Windows) where you can run it by clicking the play button.
4. Develop your Django app locally on your machine.
5. If you made changes to the dependencies (e.g. you installed a new package), rebuild `requirements.txt` (see *note* below)
6. Commit your changes to Git and push them to the remote repository.

### Note
- Make sure to update the `requirements.txt` file with any new Python dependencies you install. You can automate this by running 
```pip freeze > requirements.txt```
- Modify the `Dockerfile` file as needed to accommodate changes in your project's dependencies or configuration.

---

## Developing in Django

### The Admin panel
You may have noticed when running the docker and visiting http://localhost:8000 that there is an admin page.
This page is using the built-in Django admin interface.

You can create an admin account from your IDE's terminal, using the following command:
```shell
python manage.py createsuperuser
```
Follow the instructions in the terminal to enter a username, email and password. Please note the password is entered using 'blind typing'. This means you cannot see what you type!

From the admin interface, you can add, delete or modify records in the database.
If your model is not available in the panel, make sure to edit the `admin.py` file in your app to register the model! See the `admin.py` file in the `stories` app for an example.

### Virtual environment

1. Run the below from Powershell (windows) or Shell (mac OS / Linux) to setup a python virtual environment.
```shell
python -m venv venv
```
2. To activate the virtual environment, run the below from the terminal in your IDE (for example PyCharm)
```shell
.\venv\Scripts\activate
```

### Modifying data models
After modifying a models.py file, you need to migrate these changes through the ORM to the SQLite database.
To do this, simply run these commands:
```shell
python manage.py makemigrations [your_app]
python manage.py migrate [your_app]
```
Replace `[your_app]` with the app you're changing, for example `stories` or `sources`.
The first command will generate a migration file with operations to execute on the database.
The second command will execute the migration for the app.
If you're editing the model for multiple apps, you may also build each migration seperately, and then migrate them all by leaving out the `[your_app]` part.

### Creating new apps
In Django, separate groups of functionality are split into apps.
To create a new app, simply use this command from the terminal in your IDE:
```shell
python manage.py startapp [your_app]
```

---
## Questions or Issues?
If you have any questions or encounter any issues while setting up the development environment, please don't hesitate to open an issue in this repository or reach out to **Ruben**!.

#### Happy coding!