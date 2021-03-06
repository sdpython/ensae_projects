"""
@file
@brief Defines a search engine for images inspired from
# searchimagesrst>`_.
`Search images with deep learning <http://www.xavierdupre.fr/app/mlinsights/helpsphinx/notebooks/search_images.html
It relies on :epkg:`lightmlrestapi`.
"""
import os
import logging
import shutil
import numpy
import falcon
from pyensae.datasource import download_data


def search_images_dogcat(app=None, url_images=None, dest=None, module="torch"):
    """
    Defines a :epkg:`REST` application.
    It returns a list of neighbors among a small set of
    images representing dogs and cats. It relies
    on :epkg:`torch` or :epkg:`keras`.

    @param      app         application, if None, creates one
    @param      url_images  url or path to the images
    @param      dest        destination of the images (where to unzip)
    @param      module      :epkg:`keras` or :epkg:`torch`
    @return                 app

    You can start it by running:

    ::

        start_dogcatrestapi

    And then query it with:

    ::

        import requests
        import ujson
        from lightmlrestapi.args import image2base64
        img = "path_to_image"
        b64 = image2base64(img)[1]
        features = ujson.dumps({'X': b64})
        r = requests.post('http://127.0.0.1:8081', data=features)
        print(r)
        print(r.json())

    It should return:

    ::

        {'Y': [[[41, 4.8754486973, {'name': 'wiki.png', description='something'}]]]}
    """
    logger = logging.getLogger('search_images_dogcat')
    if module == "keras":
        return _search_images_dogcat_keras(
            app=app, url_images=url_images, dest=dest, fLOG=logger.info)
    elif module == "torch":
        return _search_images_dogcat_torch(
            app=app, url_images=url_images, dest=dest, fLOG=logger.info)
    else:
        raise ValueError("Unexpected module '{0}'.".format(module))


def _search_images_dogcat_keras(app=None, url_images=None, dest=None, fLOG=None):
    fLOG("[_search_images_dogcat_keras] Use keras")
    if url_images is None or len(url_images) == 0:
        url_images = "dog-cat-pixabay.zip"
    if dest is None or len(dest) == 0:
        dest = os.path.abspath("images")
        if not os.path.exists(dest):
            fLOG("Create folder '{0}'".format(dest))  # pylint: disable=W1202
            os.mkdir(dest)

    if not os.path.exists(dest):
        raise FileNotFoundError("Unable to find folder '{0}'".format(dest))

    # Downloads and unzips images.
    fLOG("Downloads images '{0}'".format(url_images))  # pylint: disable=W1202
    fLOG("Destination '{0}'".format(dest))  # pylint: disable=W1202
    if '/' in url_images:
        spl = url_images.split('/')
        zipname = spl[-1]
        website = '/'.join(spl[:-1])
        fLOG("zipname '{0}'".format(zipname))  # pylint: disable=W1202
        download_data(zipname, whereTo=dest, website=website + "/")
    else:
        download_data(url_images, whereTo=dest)

    classes = [_ for _ in os.listdir(
        dest) if os.path.isdir(os.path.join(dest, _))]
    if len(classes) == 0:
        # We move all images in a folder.
        imgs = os.listdir(dest)
        cl = os.path.join(dest, "oneclass")
        os.mkdir(cl)
        for img in imgs:
            shutil.move(os.path.join(dest, img), cl)
        fLOG("Moving all images to '{0}'".format(cl))  # pylint: disable=W1202
        classes = ['oneclass']

    fLOG("Discovering images in '{0}'".format(dest))  # pylint: disable=W1202

    # Iterator on images
    from keras.preprocessing.image import ImageDataGenerator
    augmenting_datagen = ImageDataGenerator(rescale=1. / 255)
    try:
        iterimf = augmenting_datagen.flow_from_directory(dest, batch_size=1, target_size=(224, 224),
                                                         classes=classes, shuffle=False)
    except Exception as e:
        fLOG("ERROR '{0}'".format(str(e)))  # pylint: disable=W1202
        raise e

    # Deep learning model.
    fLOG("Loading model '{0}'".format('MobileNet'))  # pylint: disable=W1202

    from keras.applications.mobilenet import MobileNet
    model = MobileNet(input_shape=None, alpha=1.0, depth_multiplier=1, dropout=1e-3,
                      include_top=True, weights='imagenet', input_tensor=None,
                      pooling=None, classes=1000)

    # Sets up the application.
    def predict_load():
        from mlinsights.search_rank import SearchEnginePredictionImages
        se = SearchEnginePredictionImages(model, fct_params=dict(layer=len(model.layers) - 2),
                                          n_neighbors=5)
        # fit
        fLOG("Creating the neighbors")
        se.fit(iterimf)
        return se

    # prediction function
    from lightmlrestapi.args import base642image, image2array

    def mypredict(se, X):
        if isinstance(X, str):
            img2 = base642image(X)
            return mypredict(se, img2)
        elif isinstance(X, list):
            return [mypredict(se, x) for x in X]
        else:
            gen = ImageDataGenerator(rescale=1. / 255)
            X = image2array(X.convert('RGB').resize((224, 224)))
            iterim = gen.flow(X[numpy.newaxis, :, :, :], batch_size=1)
            score, ind, meta = se.kneighbors(iterim)
            res = list(zip(map(float, score), map(
                int, ind), meta.to_dict('records')))
            return res

    # Creates the application.
    fLOG("[_search_images_dogcat_keras] Setting the application")
    from lightmlrestapi.mlapp import MachineLearningPost
    if app is None:
        app = falcon.API()
    app.add_route('/',
                  MachineLearningPost(predict_load, mypredict))
    return app


def _search_images_dogcat_torch(app=None, url_images=None, dest=None, fLOG=None):
    fLOG("[_search_images_dogcat_torch] Use torch")
    if url_images is None or len(url_images) == 0:
        url_images = "dog-cat-pixabay.zip"
    if dest is None or len(dest) == 0:
        dest = os.path.abspath("images")
        if not os.path.exists(dest):
            fLOG("Create folder '{0}'".format(dest))  # pylint: disable=W1202
            os.mkdir(dest)

    if not os.path.exists(dest):
        raise FileNotFoundError("Unable to find folder '{0}'".format(dest))

    # Downloads and unzips images.
    fLOG("Downloads images '{0}'".format(url_images))  # pylint: disable=W1202
    fLOG("Destination '{0}'".format(dest))  # pylint: disable=W1202
    if '/' in url_images:
        spl = url_images.split('/')
        zipname = spl[-1]
        website = '/'.join(spl[:-1])
        download_data(zipname, whereTo=dest, website=website + "/")
    else:
        download_data(url_images, whereTo=dest)

    classes = [_ for _ in os.listdir(
        dest) if os.path.isdir(os.path.join(dest, _))]
    if len(classes) == 0:
        # We move all images in a folder.
        imgs = os.listdir(dest)
        cl = os.path.join(dest, "oneclass")
        os.mkdir(cl)
        for img in imgs:
            shutil.move(os.path.join(dest, img), cl)
        fLOG("Moving all images to '{0}'".format(cl))  # pylint: disable=W1202
        classes = ['oneclass']

    fLOG("Discovering images in '{0}'".format(dest))  # pylint: disable=W1202

    # fit a model
    from torchvision import datasets, transforms  # pylint: disable=E0401
    trans = transforms.Compose([transforms.Resize((224, 224)),
                                transforms.CenterCrop(224),
                                transforms.ToTensor()])
    iterim = datasets.ImageFolder(dest, trans)

    from torchvision.models import squeezenet1_1  # pylint: disable=E0401
    model = squeezenet1_1(True)

    # Sets up the application.
    def predict_load():
        from mlinsights.search_rank import SearchEnginePredictionImages
        se = SearchEnginePredictionImages(
            model, fct_params=dict(), n_neighbors=5)
        # fit
        fLOG("Creating the neighbors")
        se.fit(iterim)
        fLOG("Creating the neighbors - end")
        return se

    # prediction function
    from lightmlrestapi.args import base642image, image2array

    def mypredict(se, X):
        if isinstance(X, str):
            img2 = base642image(X)
            return mypredict(se, img2)
        elif isinstance(X, list):
            return [mypredict(se, x) for x in X]
        else:
            try:
                X = image2array(X.convert('RGB').resize((224, 224)))
                if X.shape[1] != 3:
                    X = numpy.transpose(X, (2, 0, 1))
                if X.dtype.kind == 'u':
                    X = X / numpy.float32(255.0)
                score, ind, meta = se.kneighbors(X)
            except Exception as e:
                # import traceback
                # traceback.print_exc()
                raise e
            try:
                res = list(zip(map(float, score), map(
                    int, ind), meta.to_dict('records')))
            except Exception as e:
                fLOG("ERROR: {}".format(e))
                raise e
            return res

    # Creates the application.
    fLOG("[_search_images_dogcat_torch] Setting the application")
    from lightmlrestapi.mlapp import MachineLearningPost
    if app is None:
        app = falcon.API()
    app.add_route('/',
                  MachineLearningPost(predict_load, mypredict))
    return app
