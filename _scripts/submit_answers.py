"""
Measures the performances of the models.
"""
import os
from io import StringIO
import json
import pprint
import requests
from ensae_projects.hackathon.random_answers import random_answers_2020_images


def submit_random(url, password, version):
    df = random_answers_2020_images()
    st = StringIO()
    df.to_csv(st, index=False, line_terminator="\n")

    data = {
        "name": "xavier",
        "format": "df",
        "team": "prof",
        "project": "test",
        "version": version,
        "content": st.getvalue(),
        "password": password
    }

    response = requests.post(url, json=data, verify=False)
    return response


def query(url, password, name):
    data = {
        "name": name,
        "password": password
    }

    response = requests.post(url, json=data, verify=False)
    return response


url = os.environ['DASHBOARDURL']
password = os.environ['DASHBOARDPWD']


if False:
    response = submit_random(url + "submit/", password, "11")
    pprint.pprint(response.json())


if True:
    response = query(url + "query/", password, "xavier")
    pprint.pprint(response.json())
