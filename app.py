#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 09:40:31 2020

@author: fakrul
"""

#pip install Flask-APScheduler
#pip install Flask
#https://github.com/r3ap3rpy/python/blob/master/flasksched/scheduled.py

from flask import Flask, url_for
from markupsafe import escape
from flask_apscheduler import APScheduler
from flask import request
import pickle
import requests



app = Flask(__name__)

scheduler = APScheduler()


def shutdown_server():    
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET','POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@app.route("/", methods=['GET','POST'])
def index():        
    return "Welcome to the scheduler!"

def scheduledTask():
    print("This task is running every 60 seconds")
    ITEM_URL = 'http://127.0.0.1:8000/process_finish_all/'
    STATUS = requests.get(ITEM_URL)
    print('Cleaning Status: ', STATUS)    


if __name__ == '__main__':
    scheduler.add_job(id ='Scheduled task', func = scheduledTask, trigger = 'interval', seconds = 60)
    scheduler.start()
    app.run(host = '0.0.0.0', port = 9001)