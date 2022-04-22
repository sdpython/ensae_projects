
.. _l-hackathon-2022:

Hackathon ENSAE / Statup / DataForGood / Eleven Stategy - 2022
==============================================================

.. index:: Eleven Strategy, ENSAE, Hackathon, 2022

Premier hackathon en présentiel après la pandémie.
Le hackathon est proposé et organisé par :epkg:`Eleven Strategy`
(sponsor), :epkg:`ENSAE`, *Statup*.
Les données seront fournies au début de l'événement.
Le sujet a été élaboré dans le cadre d'une initiative
de :epkg:`DataForGood`.

.. contents::
    :local:

Deux défis
----------

Le cinquième hackathon de l':epkg:`ENSAE` a lieu à l'ENSAE
du vendredi 22 au samedi 21 avril 2022.
Toujours centré sur le machine Learning.

Challenge machine learning
^^^^^^^^^^^^^^^^^^^^^^^^^^



Challenge Deep Learning
^^^^^^^^^^^^^^^^^^^^^^^

L'utilisation de :epkg:`pytorch` est recommandée. Autres modules :

* `moviepy <https://zulko.github.io/moviepy/>`_: manipuler les vidéos
* `ffmpeg <https://ffmpeg.org/>`_:
  l'outil en ligne de commande pour manipuler les vidés

::

    pip install --upgrade torch torchvision torchaudio

*Articles*

* `Who spoke when! How to Build your own Speaker Diarization Module <https://medium.com/saarthi-ai/who-spoke-when-build-your-own-speaker-diarization-module-from-scratch-e7d725ee279>`_
  (code `Resemblyzer <https://github.com/resemble-ai/Resemblyzer>`_)
* `Voice, speech and gender: male-female acoustic differences and cross-language variation in English and French speakers
  <https://halshs.archives-ouvertes.fr/halshs-00764811/document>`_
* `GENERALIZED END-TO-END LOSS FOR SPEAKER VERIFICATION <https://arxiv.org/pdf/1710.10467.pdf>`_
  (`code <https://github.com/Aurora11111/speaker-recognition-pytorch>`_)
* `Text to Speech <https://pytorch.org/tutorials/intermediate/text_to_speech_with_torchaudio.html>`_

*Outils*

* `diart <https://github.com/juanmc2005/StreamingSpeakerDiarization>`_
* `Awesome Speaker Diarization <https://wq2012.github.io/awesome-diarization/>`_
* `pyannote-audio <https://github.com/pyannote/pyannote-audio>`_
* `WAV2VEC2 <https://pytorch.org/tutorials/intermediate/speech_recognition_pipeline_tutorial.html>`_
* `torchaudio <https://pytorch.org/audio/stable/index.html>`_

Avec *ONNX*:

* `Speech & Audio Processing <https://github.com/onnx/models#speech--audio-processing->`_

**Windows**

La librairie `librosa <https://librosa.org/doc/latest/index.html>`_
crée des fichiers temporaires à l'endroit
où elle est installée. Il faut donner à python les mêmes droits que
ce répertoire.

**Examples**

::

    pip install git+https://github.com/pyannote/pyannote-audio.git@develop#egg=pyannote-audio
    pip install speechbrain
    pip install diart
    
L'exemple suivant fonctionne :

::

    from pyannote.audio import Pipeline
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")

    # apply pretrained pipeline
    diarization = pipeline("2022/maybe-next-time.wav")

    # print the result
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        
Avec `diart <https://github.com/juanmc2005/StreamingSpeakerDiarization>`_:

::

    python -m diart.demo microphone

Voir aussi :ref:`traitementdusonrst`.

Après la compétition
--------------------

*Quelques photos...*

Agenda
^^^^^^
