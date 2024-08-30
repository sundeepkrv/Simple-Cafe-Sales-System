# Cafe42
A simple cafe sales management system for office cafe where an admin can login, create/edit/delete sales entry for listed employees and items as well as summary dashboard for selected employee (developed in flask)

## Demo

You can go to https://cafe42.onrender.com for live working website.

![App Walkthrough](https://raw.githubusercontent.com/sundepkrv/cafe42/main/screenshots/AppWalkthrough.gif)

## Screenshots

You can find the app screenshots in `screenshots` folder

## Development

This app has been developed in flask using python.

## Deployment

### For Unix/MacOS

Clone the project

```bash
  git clone https://github.com/sundepkrv/cafe42.git
```

Go to the project directory

```bash
  cd cafe42
```

Create a virtual environment and install requirements

```bash
  python3 -m venv venv
  source ./venv/bin/activate
  pip install -r requirements.txt
```

Start the server for local deployment

```bash
  python3 cafe42app.py
```

Using gunicorn for production deployment

```bash
  gunicorn --workers:2 cafe42app:app
```

### For Windows

Clone the project

```bash
  git clone https://github.com/sundepkrv/cafe42.git
```

Go to the project directory

```bash
  cd cafe42
```

Create a virtual environment and install requirements

```bash
  python -m venv venv
  .\venv\Scripts\activate
  pip install -r requirements.txt
```

Start the server for local deployment

```bash
  python3 cafe42app.py
```

Using gunicorn for production deployment

```bash
  gunicorn --workers:2 cafe42app:app
```

### Running behind a proxy network
If you are trying to install the dependencies behind a proxy network, run the following - 

```bash
  pip --proxy=http://xxx.xxx.xxx.xxx:yyyy install -r requirements.txt
```
## Tech Stack

**Client:** HTML, Bootstrap, Datatables, Javascript, jQuery, Chartjs

**Server:** Flask, SQLite3

## Errors

The app may run into errors and you can debug the same using references from error traceback calls.

## Feedback and contact

[@sundeepkrv](https://github.com/sundeepkrv)
