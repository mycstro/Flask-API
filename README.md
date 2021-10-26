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

* *Add the following to bring [app] to the top level of the package*
    _File Name: *`__init.py`*_
    ----------------------------
        from flask import Flask

        app = Flask(__name__, static_folder='../build', static_url_path='/')
    
        from api import api

* *Add the following to add the api app to the environemnt varibles on run*
    _File Name: *`.flaskenv`*_
    -----------------------------
        FLASK_APP=api.py
        FLASK_ENV=development

* *Append "proxy": "http:///localhost:5000" to end of package.json*
* *Append "start-api": "cd api && venv/bin/flask run --no-debugger", to package.json[scripts] - (Linux)*
  *Append "start-api": "cd api && venv/Scripts/flask run --no-debugger", to package.json[scripts] - (Windows)*

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
* Command: `mkdir deployment

### Create Backend Dockerfile

_File Name: *`Dockerfile.api`*_
----------------------------------
    FROM python:3.9
    WORKDIR /app
    COPY --from=build-step /app/build ./build

    RUN mkdir ./api
    COPY api/requirements.txt api/api.py api/.flaskenv ./
    RUN python -m pip install --upgrade pip
    RUN pip install -r ./requirements.txt
    ENV FLASK_ENV production

    EXPOSE 3000
    WORKDIR /app/api
    CMD ["gunicorn", "-b", ":3000", "app:api"]

_File Name: *`Dockerfile.client`*_
------------------------------------
### Build step #1: build the React front end
    FROM node:16-alpine as build-step
    WORKDIR /app
    ENV PATH /app/node_modules/.bin:$PATH
    COPY package.json yarn.lock ./
    COPY ./src ./src
    COPY ./public ./public
    RUN yarn install
    RUN yarn build

### Build step #2: build an nginx container
    FROM nginx:stable-alpine
    COPY --from=build-step /app/build /usr/share/nginx/html
    COPY deployment/nginx.default.conf /etc/nginx/conf.d/default.conf

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