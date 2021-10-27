# Flask-API
Basic RESTFUL API 

# My Steps

The step I took to create this project on Windows WSL Linux Docker  .

## Step One

Create and test front and backend frameworks

### Create Frontend Framework

* Command: `npx create-react-app react-flask-app` **Create app using npm**
* *Modified `App.js` to use React's __useState & useEffect__ && React-Router-Dom*

### Create Backend Framework

* Command: `cd react-flask-app` **Move into the directory**
* Command: `mkdir api` **Create Directory for api**
* Command: `cd api` **Move into the directory**
* Command: `python3 -m venv venv` **Create virtual environment**
* Command: `source venv/bin/activate` **Activate virtual enviornment - (Linux)**
* Command: `venv\Scripts\activate` **Activate virtual environment - (Windows)**
* Command: `python -m pip install --upgrade pip` **Upgrade pip**
* Command: `pip install flask flask-restful flask-jwt pandas python-dotenv gunicorn` **Install needed packages**
* Command: `pip freeze > requirements.txt` **Write install packages to txt**

* Add the following to bring [app] to the top level of the package.
    _File Name: *`__init.py`*_
    ----------------------------
        from flask import Flask

        app = Flask(__name__, static_folder='../build', static_url_path='/')
    
        from api import api

* Add the following to add the api app to the environemnt varibles on run.
    _File Name: *`.flaskenv`*_
    -----------------------------
        FLASK_APP=api.py
        FLASK_ENV=development

* *Append "proxy": "http:///localhost:5000" to end of package.json*
* *Append*
    - *"start-api": "cd api && venv/bin/flask run --no-debugger", to package.json[scripts] - (Linux)*
    - *"start-api": "cd api && venv/Scripts/flask run --no-debugger", to package.json[scripts] - (Windows)*

### Test Frontend

* Command: `npm install --global yarn` **Install Yarn** 
* Command: `cd react-flask-app` **Move into the directory**
* Command: `yarn start` **Start app to test use Ctrl-C to terminate**

### Test Backend
* Command: `cd react-flask-app` **Move into the directory**
* Command: `yarn start-api` **Start app to test use Ctrl-C to terminate**

### Create Build
* Command: `yarn build`

### Serve Build
* Command: `yarn global add services`
* Command: `serve -s build`

## Step Two

Prepare and deploy

### Prepare nginx and backend service
* Command: `cd react-flask-app` **Move into the directory**
* Command: `mkdir deployment`
* Command:  `cd deployment`

### Create Nginx and Service files

_File Name: *`nginx.default.conf`*_
------------------------------------
    server {
        listen       80;
        server_name  localhost;

        root   /usr/share/nginx/html;
        index index.html;
        error_page   500 502 503 504  /50x.html;

        location / {
            try_files $uri $uri/ =404;
            add_header Cache-Control "no-cache";
        }

        location /static {
            expires 1y;
            add_header Cache-Control "public";
        }

        location /api {
            proxy_pass http://api:5000;
        }
    }

_File Name: *`react-flask-app.nginx`*_
--------------------------------------
    server {
        listen 80;
        root /home/ubuntu/react-flask-app/build;
        server_name _;
        index index.html;

        location / {
            try_files $uri $uri/ /index.html;
            add_header Cache-Control "no-cache";
        }

        location /static {
            expires 1y;
            add_header Cache-Control "public";
        }

        location /api {
            include proxy_params;
            proxy_pass http://localhost:5000;
        }
    }

_File Name: *`react-flask-app.service`*_
----------------------------------------
    [Unit]
    Description=A simple Flask API
    After=network.target

    [Service]
    User=ubuntu
    WorkingDirectory=/home/ubuntu/react-flask-app/api
    ExecStart=/home/ubuntu/react-flask-app/api/venv/bin/gunicorn -b 127.0.0.1:5000 api:app
    Restart=always

    [Install]
    WantedBy=multi-user.target

### Create Backend Dockerfile

**Build python container**
--------------------------------
_File Name: *`Dockerfile.api`*_
--------------------------------
    FROM python:3.9
    WORKDIR /app

    COPY api/requirements.txt api/api.py api/.flaskenv ./
    RUN python -m pip install --upgrade pip
    RUN pip install -r ./requirements.txt
    ENV FLASK_ENV production

    EXPOSE 5000
    ENTRYPOINT ["gunicorn", "-b", ":5000", "api:app"]

### Create Frontend Dockerfile

_File Name: *`Dockerfile.client`*_
------------------------------------
**Build the React front end**
---------------------------------------------
    FROM node:16-alpine as build-step
    WORKDIR /app
    ENV PATH /app/node_modules/.bin:$PATH
    COPY package.json yarn.lock ./
    COPY ./src ./src
    COPY ./public ./public
    RUN yarn install
    RUN yarn build
----------------------------------------------
**Build an nginx container**
----------------------------------------------
    FROM nginx:stable-alpine
    COPY --from=build-step /app/build /usr/share/nginx/html
    COPY deployment/nginx.default.conf /etc/nginx/conf.d/default.conf

### Create docker-compose.yml

_File Name: *`docker-compose.yml`*_
------------------------------------
    services:
    api:
        build:
        context: .
        dockerfile: Dockerfile.api
        image: react-flask-app-api
    client:
        build:
        context: .
        dockerfile: Dockerfile.client
        image: react-flask-app-client
        ports:
        - "3000:80"

### Build Dockers
* Command: `docker-compose up`