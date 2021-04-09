# -*- coding: utf-8 -*-
"""
@file
@brief Code for :ref:`l-hackathon-2020`.
"""
import os  # pylint: disable=W0611
import numpy  # pylint: disable=W0611
import pandas  # pylint: disable=W0611
from sklearn.metrics import accuracy_score, log_loss


def score_images(df_expected, df_prediction):
    """
    Scores the predictions for images.
    """
    if df_expected.shape[1] != 2:
        raise ValueError("Expected 2 columns for the expected dataframe.")
    if df_prediction.shape[1] != 3:
        raise ValueError(
            "Expected 3 columns for the expected dataframe not %s." % list(
                df_prediction.columns))
    if df_expected.columns[1] != df_prediction.columns[1]:
        raise ValueError(
            "Predictions must have the following columns %r but "
            "has %r." % (list(df_expected.columns) + ['score'],
                         list(df_prediction.columns)))
    name_left = df_expected.columns[0]
    name_right = df_prediction.columns[0]
    label = df_prediction.columns[1]
    score = 'score'
    if len(set(df_expected[name_left])) != df_expected.shape[0]:
        raise ValueError("Names in expected values are not unique.")
    if len(set(df_prediction[name_right])) != df_prediction.shape[0]:
        raise ValueError("Names in expected values are not unique.")
    merged = df_expected.merge(df_prediction, left_on=name_left,
                               right_on=name_right, how='left')
    messages = []
    if merged.shape[0] != df_prediction.shape[0]:
        messages.append(
            "Some image names do not belong to the evaluation set.")
    lx = label + "_x"
    ly = label + "_y"
    merged[ly] = merged[ly].fillna(0)
    mini = merged['score'][~numpy.isnan(merged['score'])].min()
    if mini > 0:
        mini = 0
    merged['score'] = merged['score'].fillna(mini)
    acc = accuracy_score(merged[lx], merged[ly])
    ll = log_loss(merged[lx], merged[score])
    return dict(accuracy=acc, logloss=ll)
