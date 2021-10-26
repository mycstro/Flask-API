# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

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

* *Create `__init__.py` and add the following to bring [app] to the top level of the package*
    from flask import Flask

    app = Flask(__name__, static_folder='../build', static_url_path='/')
    
    from api import api

* *Create `.flaskenv` and add the following to add the api to the environemnt varibles on run*
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
Command: `yarn build`

### Serve Build
* Command: `yarn global add services`
* Command: `serve -s build`

## Step Two

Prepare and deploy

### Prepare nginx and backend service
* Command: `cd react-flask-app` **Move into the directory**
* Command: `mkdir deployment

### Create Backend Dockerfile

__File Name: *`Dockerfile.api`*__
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

__File Name: *`Dockerfile.client`*__
------------------------------------
# Build step #1: build the React front end
FROM node:16-alpine as build-step
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json yarn.lock ./
COPY ./src ./src
COPY ./public ./public
RUN yarn install
RUN yarn build

# Build step #2: build an nginx container
FROM nginx:stable-alpine
COPY --from=build-step /app/build /usr/share/nginx/html
COPY deployment/nginx.default.conf /etc/nginx/conf.d/default.conf