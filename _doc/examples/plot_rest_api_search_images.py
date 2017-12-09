"""
Search engines for images through a REST API
============================================

This example starts a :epkg:`waitress` server, creates
a :epkg:`WSGI` application based on :epkg:`falcon`
and queries the REST API. This application takes an image and
searches for similar images based on features produced
by a deep learning model.
"""

####################
# Settings.
host = '127.0.0.1'
port = 8083

########################
# Creates the search engine and starts a server in a different process.
# See :func:`search_images_dogcat <ensae_projects.restapi.search_images_dogcat.search_images_dogcat>`.


def process_server(host, port):
    import logging
    logger = logging.getLogger('search_images_dogcat')
    logger.setLevel(logging.INFO)
    hdlr = logging.FileHandler('search_images_dogcat.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)

    # If not specified, the application looks for zip file:
    # http://www.xavierdupre.fr/enseignement/complements/dog-cat-pixabay.zip
    url = None
    from ensae_projects.restapi import search_images_dogcat
    app = search_images_dogcat(url_images=url)

    from waitress import serve
    serve(app, host=host, port=port)

##########################
# Saves this code into a file and we start it
# from a different process.


import os
import ensae_projects

header = """
import sys
sys.path.append(r'{0}')
""".format(os.path.join(os.path.dirname(ensae_projects.__file__), '..'))

import inspect
code = "".join(inspect.getsourcelines(process_server)[0])
code = header + code + "\nprocess_server('{0}', {1})\n".format(host, port)
dest = os.path.abspath('temp_scripts')
if not os.path.exists(dest):
    os.mkdir(dest)
code_file = os.path.join(dest, "_start_server.py")
print("Write file '{0}'.".format(code_file))
with open(code_file, "w") as f:
    f.write(code)

import sys
from subprocess import Popen
if sys.platform.startswith('win'):
    cmd = '{0} -u "{1}"'.format(sys.executable, code_file)
    print("Running '{0}'".format(cmd))
    proc = Popen(cmd)
else:
    cmd = [sys.executable, '-u', code_file]
    print("Running '{0}'".format(cmd))
    proc = Popen(cmd)
print('Start server, process id', proc.pid)

##########################
# Let's wait.
from time import sleep
sleep(15)

####################
# Let's load an image.

from lightmlrestapi.args import image2base64
import ensae_projects.datainc.search_images as si
imgfile = os.path.join(os.path.dirname(si.__file__), "cat-1192026__480.jpg")

from PIL import Image
img = Image.open(imgfile)

import numpy
from matplotlib.pyplot import imshow
imshow(numpy.asarray(img))

############################
# Let's query the server.

import requests
import ujson

b64 = image2base64(imgfile)[1]
features = ujson.dumps({'X': b64})
r = requests.post('http://127.0.0.1:%d' % port, data=features)
js = r.json()
if 'description' in js:
    # This is an error.
    print(js['description'])
    res = None
else:
    print(js)
    res = []
    for ans in js['Y']:
        print("Number of neighbors:", len(ans))
        for n in ans:
            print("score, id, name", n)
            res.append((n[0], n[2]['name']))

#######################
# Let's display the images.

txts = list(map(lambda x: str(x[0]), res))
imgs = list(map(lambda x: os.path.join('images', x[1]), res))

from mlinsights.plotting import plot_gallery_images
plot_gallery_images(imgs, txts)

import matplotlib.pyplot as plt
# plt.show()

####################
# Let's stop the server.
from pyquickhelper.loghelper import reap_children
reap_children(subset={proc.pid}, fLOG=print)
