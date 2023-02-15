# karamoozesh_backend
## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Nima-Nilchian/karamoozesh_backend.git
$ cd karamoozesh_backend
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv venv -p python3
```

activating virtual environment on Windows:
```sh
$ venv\Scripts\acticvate
```
activating virtual environment on Linux:
```sh
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.


Once `pip` has finished downloading the dependencies, *Now You have to create a local_settings.py file in config folder and set secret_key, debug, database and smtp configurations.*

Then you can create a development database:
```sh
(venv)$ python manage.py migrate
```

Finally, run the project:
```sh
(venv)$ python manage.py runserver
```
