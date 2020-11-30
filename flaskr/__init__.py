# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# NLP components
from spacy_summarization import text_summarizer
import time
import spacy
nlp = spacy.load('en_core_web_sm')


# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

# from scripts import tabledef
# from scripts import forms
# from scripts import helpers

from flask import Flask, redirect, url_for, render_template, request, session, jsonify
import json
import sys
import os
import pandas as pd
from werkzeug.utils import secure_filename

from flask import make_response, Response



# https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/



# Reading Time
def readingTime(mytext):
    total_words = len([ token.text for token in nlp(mytext)])
    estimatedTime = total_words/200.0
    return estimatedTime

# Fetch Text From Url
def get_text(url):
    page = urlopen(url)
    soup = BeautifulSoup(page)
    # fetch all the p tags in the document
    fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def home():
        return render_template('home.html')


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

#-------------------------------------------------------------------------
# Summary routes

    @app.route('/analyze',methods=['GET','POST'])
    def analyze():
            start = time.time()
            if request.method == 'POST':
                rawtext = request.form['rawtext']
                final_reading_time = readingTime(rawtext)
                final_summary = text_summarizer(rawtext)
                summary_reading_time = readingTime(final_summary)
                end = time.time()
                final_time = end-start
                time_saved = final_reading_time - summary_reading_time
                # user = helpers.get_user()
                # user.active = True
                # user.key = stripe_keys['publishable_key']
            return render_template('home.html',
                ctext=rawtext,final_summary=final_summary,
                final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,time_saved=time_saved)


    @app.route('/analyze_url',methods=['GET','POST'])
    def analyze_url():
            start = time.time()
            if request.method == 'POST':
                raw_url = request.form['raw_url']
                rawtext = get_text(raw_url)
                final_reading_time = readingTime(rawtext)
                final_summary = text_summarizer(rawtext)
                summary_reading_time = readingTime(final_summary)
                end = time.time()
                final_time = end-start
                time_saved = final_reading_time - summary_reading_time
                # user = helpers.get_user()
                # user.active = True
                # user.key = stripe_keys['publishable_key']
            return render_template('home.html',
                ctext=rawtext,final_summary=final_summary,
                final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,time_saved=time_saved)




    return app
