"""
@brief      test log(time=8s)
"""

import sys
import os
import unittest
import json
import pandas
from ensae_projects.hackathon.random_answers import random_answers_2020_images
from ensae_projects.hackathon.hack2020 import score_images


class TestEvaluation(unittest.TestCase):

    def test_evaluation(self):
        df1 = random_answers_2020_images().iloc[:, :2]
        df2 = random_answers_2020_images()
        score = score_images(df1, df2)
        self.assertIsInstance(score, dict)
        score = score_images(df2.iloc[:, :2], df2)
        self.assertIsInstance(score, dict)
        self.assertEqual(score['accuracy'], 1)


if __name__ == "__main__":
    unittest.main()
