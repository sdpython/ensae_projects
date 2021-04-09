"""
@brief      test log(time=8s)
"""

import sys
import os
import unittest
import json
import pandas
from ensae_projects.hackathon.random_answers import random_answers_2020_images


class TestRandomAnswers(unittest.TestCase):

    def test_random_answers_2020_images(self):
        df = random_answers_2020_images()
        self.assertEqual(df.shape, (505, 3))
        self.assertEqual(list(df.columns), ['file_name', 'label', 'score'])
        self.assertEqual(set(df['label']), {0, 1})


if __name__ == "__main__":
    unittest.main()
