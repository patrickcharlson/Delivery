# Delivery
A website for Delivering Pizza

**At a glance, once the application is setup, a basic land page should appear

## Setting up

##### Clone the repo

```
$ git clone https://github.com/patrickcharlson/Delivery.git
$ cd Delivery
```

##### Initialize a virtualenv

```
$ pip install virtualenv
$ python3 -m venv venv
$ source venv/bin/activate
```

For mac users it will most likely be
```
$ pip install virtualenv
$ virtualenv -p python3 env
$ source venv/bin/activate
```

Note: if you are using a python2.x version, point the -p value towards your python2.x path

##### (If you're on a mac) Make sure xcode tools are installed

```
$ xcode-select --install
```

##### Install the dependencies

```
$ pip install -r requirements.txt
```

## Running the app

```
$ source venv/bin/activate
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run



```
