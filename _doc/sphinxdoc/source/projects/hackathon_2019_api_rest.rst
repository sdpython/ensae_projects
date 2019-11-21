
.. _l-hackathon-2019-api-rest:

Uploader vos résultats
======================

Les outils développés s'appuie sur le module
:epkg:`lightmlrestapi` et reprennent une partie
des éléments décrits dans ce tutoriel :
`API REST <http://www.xavierdupre.fr/app/lightmlrestapi/
helpsphinx/tutorial/store_rest_api.html>`_
ou ce notebook :ref:`restapisearchimagesrst`.
Il vous sera distribué un login et un mot de passe au début
de l'événement.

.. contents::
    :local:

Préparer son modèle
-------------------

Une fois le modèle appris
et stocké dans un ou plusieurs fichiers, il faut pouvoir créer un 
programme python qui permet au jury d'appeler votre modèle.

:: 

    import pickle
    import os


    def restapi_version():
        "Declare an id for the REST API."
        return "0.1.1234"


    def restapi_load(files={"model": "model_iris.pkl"}):
        """Loads the model.
        The model name is relative to this file.
        When call by a REST API, the default value is always used.
        """
        model = files["model"]
        here = os.path.dirname(__file__)
        model = os.path.join(here, model)
        if not os.path.exists(model):
            raise FileNotFoundError("Cannot find model '{0}' (full path is '{1}')".format(
                model, os.path.abspath(model)))
        with open(model, "rb") as f:
            loaded_model = pickle.load(f)
        return loaded_model


    def restapi_predict(model, X):
        """
        Computes the prediction for model *clf*.
        """
        return model.predict_proba(X)

Voir `Iris
<http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/tutorial/
store_rest_api.html#train-a-model-on-iris>`_. 

Uploader son modèle
-------------------

Il faut installer les modules :epkg:`lightmlrestapi` et 
:epkg:`pyquickhelper` puis lancer la ligne de commande suivante :

::

    python -m lightmlrestapi upload_model --name=equipe/iteration --url=http://<addresse_ip>:<port>/ --pyfile=model_iris.py --data "fichier1,fichier2" --login=hk2019 --pwd=<password>

Les informations entre ``<>`` seront précisées au début du hackathon.
Voir aussi :
`Upload a machine learned model
<http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/tutorial/
store_rest_api.html#upload-a-machine-learned-model>`_.

Vérifier le modèle uploadé
--------------------------

::

    from lightmlrestapi.netrest import json_predict_model, submit_rest_request
    from sklearn import datasets

    iris = datasets.load_iris()
    X = iris.data[:, :2]

    req = json_predict_model("equipe/iteration", X)
    res = submit_rest_request(req, login="<login>", pwd="<password>",
                              url="http://<adresse_ip>:<port>/", fLOG=print)
    print(res)

Voir aussi
`Compute prediction through the REST API
<http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/tutorial/
store_rest_api.html#compute-prediction-through-the-rest-api>`_.

Version des modules utilisées pour tester votre modèle
------------------------------------------------------

::

    bayespy==0.5.18
    bokeh==1.4.0
    cairocffi==1.1.0
    Cartopy==0.17.0
    catboost==0.18.1
    category-encoders==2.1.0
    cffi==1.13.2
    chainer==6.4.0
    chainercv==0.13.1
    cvxopt==1.2.3
    Cython==0.29.14
    falcon==2.0.0
    folium==0.10.0
    gensim==3.8.1
    geopandas==0.6.2
    imbalanced-learn==0.5.0
    jyquickhelper==0.3.128
    Keras==2.3.1
    Keras-Applications==1.0.8
    Keras-Preprocessing==1.1.0
    lightgbm==2.3.0
    lightmlrestapi==0.2.151
    matplotlib==3.1.1
    moviepy==1.0.1
    networkx==2.4
    nltk==3.4.5
    numba==0.46.0
    numpy==1.17.4
    opencv-python==4.0.0.21
    pandas==0.25.3
    Pillow==6.2.1
    protobuf==3.10.0
    pyproj==2.4.1
    pyquickhelper==1.9.3248
    scikit-image==0.16.2
    scikit-learn==0.21.3
    scipy==1.3.2
    Shapely==1.6.4.post2
    spacy==2.2.2
    statsmodels==0.10.1
    tensorflow==2.0.0
    tensorflow-estimator==2.0.1
    tf-estimator-nightly==1.12.0.dev20181217
    tf-nightly==1.13.0.dev20190111
    thinc==7.3.1
    torchvision==0.4.2+cpu
    ujson==1.35
    virtualenv==16.7.7
    x86cpu==0.4
    xarray==0.14.0
    xgboost==0.90
