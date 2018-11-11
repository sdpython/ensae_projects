"""
@brief      test log(time=9s)
"""

import sys
import os
import unittest
import numpy
from PIL import Image
from pyquickhelper.pycode import get_temp_folder, ExtTestCase


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

from src.ensae_projects.hackathon.image_helper import resize_image, read_image, enumerate_image_class, histogram_image_size, img2gray
from src.ensae_projects.hackathon.image_helper import stream_apply_image_transform, image_zoom, stream_image2features
from src.ensae_projects.hackathon.image_helper import load_batch_features, stream_download_images, stream_copy_images, stream_random_sample
from src.ensae_projects.hackathon.image_helper import last_element, plot_gallery_random_images
from src.ensae_projects.hackathon.image_helper import folder_split_train_test
from src.ensae_projects.hackathon.image_knn import ImageNearestNeighbors


class TestImage(ExtTestCase):

    def test_image_resize(self):
        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "data", "white.png")
        temp = get_temp_folder(__file__, "temp_resize_mage")

        dest = os.path.join(temp, "mini.png")
        resize_image(data, dest=dest, maxdim=200)
        self.assertExists(dest)
        im = Image.open(dest)
        self.assertGreater(200, min(im.size))

        dest = os.path.join(temp, "mini2.png")
        resize_image(data, dest=dest, maxdim=100)
        self.assertExists(dest)
        im = Image.open(dest)
        self.assertGreater(100, min(im.size))

    def test_image_read(self):
        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "data", "white.png")
        im = read_image(data)
        size = im.size
        self.assertEqual(size, (694, 407))

    def test_enumerate_image(self):
        this = os.path.abspath(os.path.dirname(__file__))
        imgs = list(enumerate_image_class(this, abspath=False))
        da = [_ for _ in imgs if _[1] == 'data']
        self.assertGreater(len(da), 1)
        da = [(_.replace('\\', '/'), __) for _, __ in da]
        self.assertEqual(da[:1], [('data/white.png', 'data')])

    def test_histogram_size(self):
        this = os.path.abspath(os.path.dirname(__file__))
        hist = histogram_image_size(this)
        self.assertIn((694, 407), hist)

    def test_image2gray(self):
        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "data", "white.png")
        im = read_image(data)
        gray = img2gray(im)
        self.assertEqual(gray.size, im.size)
        np = numpy.array(gray)
        self.assertEqual(np.shape, (407, 694))

    def test_image2gray_folder(self):
        this = os.path.abspath(os.path.dirname(__file__))
        temp = get_temp_folder(__file__, "temp_image2gray_folder")
        list(stream_apply_image_transform(this, temp, lambda im: img2gray(im)))
        do = os.path.join(temp, "data", "white.png")
        self.assertExists(do)
        im = read_image(do)
        ar = numpy.array(im)
        self.assertEqual(len(ar.shape), 2)

    def test_zoom(self):
        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "data", "white.png")
        im = read_image(data)
        zo = image_zoom(im, (10, 10))
        self.assertEqual(zo.size, (10, 10))

    def test_stream_image2features(self):
        this = os.path.abspath(os.path.dirname(__file__))
        temp = get_temp_folder(__file__, "temp_stream_image2features")
        res = list(stream_image2features(
            this, temp, lambda im: numpy.array(image_zoom(img2gray(im), (10, 12)))))
        self.assertEqual(res, ['batch0.pkl'])
        name = os.path.join(temp, res[0])
        obj = load_batch_features(name)
        self.assertEqual(len(obj), 2)
        img, cl = obj
        self.assertIsInstance(img, numpy.ndarray)
        self.assertGreater(len(img.shape), 2)
        self.assertIsInstance(cl, numpy.ndarray)
        self.assertIsInstance(cl[0], str)

    def test_stream_download_images(self):
        temp = get_temp_folder(__file__, "temp_stream_download_images")

        urls = ['http://www.xavierdupre.fr/blog/documents/feed-icon-16x16.png']
        res = list(stream_download_images(urls, temp, use_request=True))
        self.assertEqual(len(res), 1)
        self.assertEndsWith(res[0], 'feed-icon-16x16.png')
        img = read_image(os.path.join(temp, res[0]))
        self.assertNotEmpty(img)

        urls = ['http://www.xavierdupre.fr/blog/documents/linkedin.png']
        res = list(stream_download_images(urls, temp, use_request=False))
        self.assertEqual(len(res), 1)
        self.assertEndsWith(res[0], 'linkedin.png')
        img = read_image(os.path.join(temp, res[0]))
        self.assertNotEmpty(img)

    def test_imagenearestneighbors_folder(self):
        this = os.path.abspath(os.path.dirname(__file__))
        folder = os.path.join(this, "data", "many")
        knn = ImageNearestNeighbors()
        knn.fit(folder)
        self.assertEqual(knn.image_classes_, [
                         'cl1', 'cl1', 'cl1', 'cl2', 'cl2', 'cl2'])
        self.assertEqual(knn.image_names_, ['cl1/739728353121427456_CkQLA7WVEAAZxFI.jpg',
                                            'cl1/950995136640700416_DTKdA4lWAAAOuqj.jpg',
                                            'cl1/img23.jpg',
                                            'cl2/768263167319371776_CqlrRw3WAAAb3ni.jpg',
                                            'cl2/768263432214814720_CqlrfCqXEAAANKG.jpg',
                                            'cl2/img22.jpg'])

        dist, kn = knn.kneighbors(folder, n_neighbors=2)
        self.assertEqual(kn.shape, dist.shape)
        names = knn.get_image_names(kn)
        exp = [[0, 2], [1, 2], [2, 1], [3, 2], [4, 5], [5, 4]]
        self.assertEqual(kn, numpy.array(exp))
        self.assertEqual(kn.shape, names.shape)
        self.assertEqual(
            names[0, 0], 'cl1/739728353121427456_CkQLA7WVEAAZxFI.jpg')
        names = knn.get_image_classes(kn)
        self.assertEqual(kn.shape, names.shape)
        exp = [['cl1', 'cl1'], ['cl1', 'cl1'], ['cl1', 'cl1'],
               ['cl2', 'cl1'], ['cl2', 'cl2'], ['cl2', 'cl2']]
        self.assertEqual(names.ravel().tolist(),
                         numpy.array(exp).ravel().tolist())

    def test_imagenearestneighbors_names(self):
        this = os.path.abspath(os.path.dirname(__file__))
        folder = os.path.join(this, "data", "many")
        knn = ImageNearestNeighbors()
        images = list(enumerate_image_class(folder))
        knn.fit(images)
        self.assertEqual(knn.image_classes_, [
                         'cl1', 'cl1', 'cl1', 'cl2', 'cl2', 'cl2'])
        dist, kn = knn.kneighbors(images, n_neighbors=2)
        self.assertEqual(kn.shape, dist.shape)
        names = knn.get_image_names(kn)
        exp = [[0, 2], [1, 2], [2, 1], [3, 2], [4, 5], [5, 4]]
        self.assertEqual(kn, numpy.array(exp))
        self.assertEqual(kn.shape, names.shape)
        self.assertEndsWith(
            'cl1/739728353121427456_CkQLA7WVEAAZxFI.jpg', names[0, 0])
        names = knn.get_image_classes(kn)
        self.assertEqual(kn.shape, names.shape)
        exp = [['cl1', 'cl1'], ['cl1', 'cl1'], ['cl1', 'cl1'],
               ['cl2', 'cl1'], ['cl2', 'cl2'], ['cl2', 'cl2']]
        self.assertEqual(names.ravel().tolist(),
                         numpy.array(exp).ravel().tolist())

    def test_imagenearestneighbors_images(self):
        this = os.path.abspath(os.path.dirname(__file__))
        folder = os.path.join(this, "data", "many")
        knn = ImageNearestNeighbors()
        images = list(enumerate_image_class(folder))
        images = [read_image(_[0]) for _ in images]
        knn.fit(images)
        self.assertFalse(hasattr(knn, 'image_classes_'))
        dist, kn = knn.kneighbors(images, n_neighbors=2)
        self.assertEqual(kn.shape, dist.shape)
        self.assertRaise(lambda: knn.get_image_names(kn))
        self.assertRaise(lambda: knn.get_image_classes(kn))

    def test_imagenearestneighbors_tuple_image(self):
        this = os.path.abspath(os.path.dirname(__file__))
        folder = os.path.join(this, "data", "many")
        knn = ImageNearestNeighbors()
        images = list(enumerate_image_class(folder))
        images = [(read_image(_[0]), _[1]) for _ in images]
        knn.fit(images)
        self.assertEqual(knn.image_classes_, [
                         'cl1', 'cl1', 'cl1', 'cl2', 'cl2', 'cl2'])
        dist, kn = knn.kneighbors(images, n_neighbors=2)
        self.assertEqual(kn.shape, dist.shape)
        names = knn.get_image_names(kn)
        exp = [[0, 2], [1, 2], [2, 1], [3, 2], [4, 5], [5, 4]]
        self.assertEqual(kn, numpy.array(exp))
        self.assertEqual(kn.shape, names.shape)
        self.assertEqual(None, names[0, 0])
        names = knn.get_image_classes(kn)
        self.assertEqual(kn.shape, names.shape)
        exp = [['cl1', 'cl1'], ['cl1', 'cl1'], ['cl1', 'cl1'],
               ['cl2', 'cl1'], ['cl2', 'cl2'], ['cl2', 'cl2']]
        self.assertEqual(names.ravel().tolist(),
                         numpy.array(exp).ravel().tolist())

    def test_imagenearestneighbors_gallery(self):
        this = os.path.abspath(os.path.dirname(__file__))
        folder = os.path.join(this, "data", "many")
        knn = ImageNearestNeighbors()
        knn.fit(folder)

        temp = get_temp_folder(__file__, "temp_imagenearestneighbors_gallery")

        from matplotlib import pyplot as plt

        img = os.path.join(
            folder, "cl1", "739728353121427456_CkQLA7WVEAAZxFI.jpg")
        dist, kn = knn.kneighbors(img, n_neighbors=2)
        fig, _ = knn.plot_neighbors(
            kn, dist, obs=img, folder_or_images=folder, return_figure=True)
        img = os.path.join(temp, "gallery.png")
        fig.savefig(img)
        plt.close('all')

    def test_imagenearestneighbors_tuple_image_gallery(self):
        this = os.path.abspath(os.path.dirname(__file__))
        folder = os.path.join(this, "data", "many")
        knn = ImageNearestNeighbors()
        images = list(enumerate_image_class(folder))
        images = [(read_image(_[0]), _[1]) for _ in images]
        knn.fit(images)
        temp = get_temp_folder(
            __file__, "temp_imagenearestneighbors_tuple_gallery")

        from matplotlib import pyplot as plt

        img = read_image(os.path.join(
            folder, "cl1", "739728353121427456_CkQLA7WVEAAZxFI.jpg"))
        dist, kn = knn.kneighbors(img, n_neighbors=2)
        fig, _ = knn.plot_neighbors(
            kn, dist, obs=img, folder_or_images=images, return_figure=True)
        img = os.path.join(temp, "gallery.png")
        fig.savefig(img)
        plt.close('all')

    def test_imagenearestneighbors_gallery5(self):
        this = os.path.abspath(os.path.dirname(__file__))
        folder = os.path.join(this, "data", "many")
        knn = ImageNearestNeighbors()
        knn.fit(folder)

        temp = get_temp_folder(__file__, "temp_imagenearestneighbors_gallery5")

        from matplotlib import pyplot as plt

        img = os.path.join(
            folder, "cl1", "739728353121427456_CkQLA7WVEAAZxFI.jpg")
        dist, kn = knn.kneighbors(img, n_neighbors=5)
        fig, _ = knn.plot_neighbors(
            kn, dist, obs=img, folder_or_images=folder, return_figure=True)
        img = os.path.join(temp, "gallery.png")
        fig.savefig(img)
        plt.close('all')

    def test_stream_copy_images(self):
        temp = get_temp_folder(__file__, "temp_stream_copy_images")
        folder = os.path.join(temp, "..", "data", "many")
        files = list(stream_copy_images(folder, temp, valid=lambda img: True))
        self.assertEqual(len(files), 6)

    def test_random_sample(self):
        this = os.path.abspath(os.path.dirname(__file__))
        folder = os.path.join(this, "data", "many")
        images = last_element(stream_random_sample(folder, n=2, abspath=False))
        self.assertEqual(len(images), 2)

    def test_plot_gallery_random_images(self):
        this = os.path.abspath(os.path.dirname(__file__))
        folder = os.path.join(this, "data", "many")
        temp = get_temp_folder(__file__, "temp_plot_gallery_random_images")

        from matplotlib import pyplot as plt
        (fig, _), rnd = plot_gallery_random_images(
            folder, n=2, return_figure=True)
        img = os.path.join(temp, "gallery.png")
        fig.savefig(img)
        plt.close('all')
        self.assertNotEmpty(rnd)
        self.assertIsInstance(rnd[0], tuple)
        self.assertEqual(len(rnd[0]), 3)

    def test_folder_train_test_split(self):
        temp = get_temp_folder(__file__, "temp_folder_train_test_split")
        data = os.path.join(temp, '..', 'data', 'many')
        train = os.path.join(temp, "train")
        test = os.path.join(temp, "test")
        itrain, itest = folder_split_train_test(
            data, train, test, test_size=0.5)
        self.assertEqual(len(itrain), 3)
        self.assertEqual(len(itest), 3)


if __name__ == "__main__":
    unittest.main()
