# -*- coding: utf-8 -*-
"""
@file
@brief Generates random answers for challenges.
"""
import os
import numpy
import pandas


def random_answers_2020_images():
    """
    Generates random answers the deep learning challenge of
    hackathons :ref:`l-hackathon-2020`.
    """
    name = os.path.join(os.path.split(__file__)[0], "labels_2020_random.csv")
    df = pandas.read_csv(name)[['file_name']]
    df['label'] = numpy.random.randint(low=0, high=2, size=(df.shape[0], ))
    df['score'] = numpy.random.random((df.shape[0], ))
    return df
