"""
@brief      test log(time=8s)
"""

import sys
import os
import unittest
import json
import io
import pandas
from pyquickhelper.pycode import get_temp_folder, ExtTestCase
from ensae_projects.hackathon.random_answers import (
    random_answers_2020_images, random_answers_2020_ml)


class TestRandomAnswers(ExtTestCase):

    def test_random_answers_2020_images(self):
        df = random_answers_2020_images()
        self.assertEqual(df.shape, (505, 3))
        self.assertEqual(list(df.columns), ['file_name', 'label', 'score'])
        self.assertEqual(set(df['label']), {0, 1})

    def test_random_answers_2020_ml(self):
        df = random_answers_2020_ml()
        self.assertEqual(df.shape, (473333, 3))
        self.assertEqual(list(df.columns), ['index', 'label', 'score'])
        self.assertEqual(set(df['label']), {0, 1})

    def test_export_as_json(self):
        temp = get_temp_folder(__file__, "temp_export")

        st = io.StringIO()
        df = random_answers_2020_ml()
        df.to_csv(st, encoding="utf-8", index=False, line_terminator="\n")
        data = dict(name="xavier", project="tgtg", version="1", team="test",
                    password="AAA", content=st.getvalue())
        t1 = json.dumps(data, indent=4)
        with open(os.path.join(temp, "random_ml.json"), "w", encoding="utf-8") as f:
            f.write(t1)

        st = io.StringIO()
        df = random_answers_2020_images()
        df.to_csv(st, encoding="utf-8", index=False, line_terminator="\n")
        data = dict(name="xavier", project="sea", version="1", team="test",
                    password="AAA", content=st.getvalue())
        t1 = json.dumps(data, indent=4)
        with open(os.path.join(temp, "random_dl.json"), "w", encoding="utf-8") as f:
            f.write(t1)


if __name__ == "__main__":
    unittest.main()
