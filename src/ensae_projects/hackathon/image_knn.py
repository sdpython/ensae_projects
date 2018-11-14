# -*- coding: utf-8 -*-
"""
@file
@brief Builds a knn classifier for image in order to find close images.
"""
import os
import numpy
from sklearn.neighbors import NearestNeighbors
from PIL.Image import Image
from .image_helper import img2gray, enumerate_image_class, read_image, image_zoom


class ImageNearestNeighbors(NearestNeighbors):
    """
    Builds a model on the top of :epkg:`NearestNeighbors`
    in order to find close images.
    """

    def __init__(self, transform='gray', size=(10, 10), **kwargs):
        """
        @param      folder_or_list      folder or list or of images
        @param      transform           function which transform every image
        @param      size                every image is zoomed to keep the same dimension
        @param      kwargs              see :epkg:`NearestNeighbors`
        """
        NearestNeighbors.__init__(self, **kwargs)
        self.image_size = size
        self.transform = transform
        self._get_transform()

    def _get_transform(self):
        """
        Returns the associated transform function with ``self.transform_``.
        """
        if self.transform == "gray":
            pre = img2gray
        elif self.transform is None:
            pre = None
        else:
            raise ValueError(
                "No transform assicated with value '{0}'.".format(self.transform))
        if pre is None:
            return lambda img: image_zoom(img, new_size=self.image_size)
        else:
            return lambda img: image_zoom(pre(img), new_size=self.image_size)

    def _folder2matrix(self, folder, fLOG):
        """
        Converts images stored in a folder into a matrix of features.
        """
        transform = self._get_transform()
        imgs = []
        subs = []
        stack = []
        for i, (name, sub) in enumerate(enumerate_image_class(folder, abspath=False)):
            if fLOG is not None and i % 1000 == 0:
                fLOG(
                    "[ImageNearestNeighbors] processing image {0}: '{1}' - class '{2}'".format(i, name, sub))
            imgs.append(name.replace("\\", "/"))
            subs.append(sub)
            img = read_image(os.path.join(folder, name))
            trimg = transform(img)
            stack.append(numpy.array(trimg).ravel())
        X = numpy.vstack(stack)
        return X, imgs, subs

    def _imglist2matrix(self, list_of_images, fLOG):
        """
        Converts a list of images into a matrix of features.
        """
        transform = self._get_transform()
        imgs = []
        subs = []
        stack = []
        for i, name in enumerate(list_of_images):
            if isinstance(name, tuple):
                name, sub = name
            else:
                sub = None
            if fLOG is not None and i % 1000 == 0:
                fLOG(
                    "[ImageNearestNeighbors] processing image {0}: '{1}' - class '{2}'".format(i, img, sub))
            if isinstance(name, Image):
                imgs.append(None)
                img = name
            else:
                imgs.append(name.replace("\\", "/"))
                img = read_image(name)
            subs.append(sub)
            trimg = transform(img)
            stack.append(numpy.array(trimg).ravel())
        X = numpy.vstack(stack)
        return X, imgs, subs

    def fit(self, X, y=None, fLOG=None):  # pylint: disable=W0221
        """
        Fits the model. *X* can be a folder.

        @param      X       matrix or str for a subfolder of images
        @param      y       unused
        @param      fLOG    logging function

        If *X* is a folder, the method relies on function
        @see fct enumerate_image_class. In that case, the method
        also creates attributes:

        * ``image_names_``: all image names
        * ``image_classes_``: subfolder the image belongs too
        """
        if isinstance(X, str):
            if not os.path.exists(X):
                raise FileNotFoundError("Folder '{0}' not found.".format(X))
            X, imgs, subs = self._folder2matrix(X, fLOG)
            self.image_names_ = imgs  # pylint: disable=W0201
            self.image_classes_ = subs  # pylint: disable=W0201

        elif isinstance(X, list):
            if isinstance(X[0], Image):
                transform = self._get_transform()
                X = numpy.array([numpy.array(transform(img)).ravel()
                                 for img in X])
            elif isinstance(X[0], str):
                # image names
                X, imgs, subs = self._imglist2matrix(X, fLOG)
                self.image_names_ = imgs  # pylint: disable=W0201
                self.image_classes_ = subs  # pylint: disable=W0201
            elif isinstance(X[0], tuple):
                self.image_classes_ = list(  # pylint: disable=W0201
                    map(lambda t: t[1], X))
                X, imgs, _ = self._imglist2matrix([_[0] for _ in X], fLOG)
                self.image_names_ = imgs  # pylint: disable=W0201
            else:
                raise TypeError(
                    "X should be a list of PIL.Image not {0}".format(type(X[0])))

        super(ImageNearestNeighbors, self).fit(X, y)

    def _private_kn(self, method, X, *args, fLOG=None, **kwargs):
        """
        Commun private function to handle the same kind of
        inputs in all transform functions.

        @param      method      method to run
        @param      X           inputs, matrix, folder or list of images
        @param      args        additional positinal arguments
        @param      fLOG        logging function
        @param      kwargs      additional named arguements
        @return                 depends on *method*
        """
        if isinstance(X, str):
            if not os.path.exists(X):
                raise FileNotFoundError("Folder '{0}' not found.".format(X))
            if os.path.isfile(X):
                X = [X]
                return self._private_kn(method, X, *args, **kwargs)
            X = self._folder2matrix(X, fLOG=fLOG)[0]

        elif isinstance(X, list):
            if isinstance(X[0], Image):
                transform = self._get_transform()
                X = numpy.array([numpy.array(transform(img)).ravel()
                                 for img in X])
            elif isinstance(X[0], str):
                # image names
                X = self._imglist2matrix(X, None)[0]
            elif isinstance(X[0], tuple):
                # image names
                X = self._imglist2matrix([_[0] for _ in X], fLOG=fLOG)[0]
            else:
                raise TypeError("X should be a list of Image")
        elif isinstance(X, Image):
            return self._private_kn(method, [X], *args, **kwargs)

        method = getattr(NearestNeighbors, method)
        return method(self, X, *args, **kwargs)

    def kneighbors(self, X=None, n_neighbors=None, return_distance=True, fLOG=None):  # pylint: disable=W0221
        """
        See :epkg:`NearestNeighbors`, method :epkg:`kneighbors`.
        Parameter *X* can be a file, the image is then loaded and converted
        with the same transform. *X* can also be a :epkg:`PIL.Image`.
        """
        return self._private_kn("kneighbors", X=X, n_neighbors=n_neighbors, return_distance=return_distance, fLOG=fLOG)

    def kneighbors_graph(self, X=None, n_neighbors=None, mode='connectivity', fLOG=None):  # pylint: disable=W0221
        """
        See :epkg:`NearestNeighbors`, method :epkg:`kneighbors_graph`.
        Parameter *X* can be a file, the image is then loaded and converted
        with the same transform. *X* can also be a :epkg:`PIL.Image`.
        """
        return self._private_kn("kneighbors_graph", X=X, n_neighbors=n_neighbors, mode=mode, fLOG=fLOG)

    def radius_neighbors(self, X=None, radius=None, return_distance=True, fLOG=None):  # pylint: disable=W0221
        """
        See :epkg:`NearestNeighbors`, method :epkg:`radius_neighbors`.
        Parameter *X* can be a file, the image is then loaded and converted
        with the same transform. *X* can also be a :epkg:`PIL.Image`.
        """
        return self._private_kn("radius_neighbors", X=X, radius=radius, return_distance=return_distance, fLOG=fLOG)

    def get_image_names(self, indices):
        """
        Returns images names for the given list of indices.

        @param      indices     indices can be a single array or a matrix.
        @return                 same shape
        """
        if not hasattr(self, "image_names_"):
            raise RuntimeError("No image names were stored during training.")
        new_indices = indices.ravel()
        res = numpy.array([self.image_names_[i] for i in new_indices])
        return res.reshape(indices.shape)

    def get_image_classes(self, indices):
        """
        Returns images classes for the given list of indices.

        @param      indices     indices can be a single array or a matrix.
        @return                 same shape
        """
        if not hasattr(self, "image_classes_"):
            raise RuntimeError("No image classes were stored during training.")
        new_indices = indices.ravel()
        res = numpy.array([self.image_classes_[i] for i in new_indices])
        return res.reshape(indices.shape)

    def plot_neighbors(self, neighbors, distances=None, obs=None, return_figure=False,
                       format_distance="%1.2f", folder_or_images=None):
        """
        Calls :epkg:`plot_gallery_images`
        with information on the neighbors.

        @param      neighbors           matrix of indices
        @param      distances           distances to display
        @param      obs                 original image, if not None, will be placed
                                        on the first row
        @param      format_distance     used to format distances
        @param      folder_or_images    image paths may be relative to some folder,
                                        in that case, they should be relative to
                                        this folder, it can also be a list of images
        @return                         *ax* or *fix, ax* if *return_figure* is True
        """
        from mlinsights.plotting import plot_gallery_images
        names = self.get_image_names(neighbors)
        if hasattr(self, "image_classes_"):
            subs = self.get_image_classes(neighbors)
        else:
            subs = numpy.array([["" for i in range(names.shape[1])]
                                for j in range(names.shape[0])])

        labels = []
        if distances is not None:
            for i in range(names.shape[0]):
                for j in range(names.shape[1]):
                    labels.append("{0} d={1}".format(
                        subs[i, j], format_distance % distances[i, j]))
        else:
            for i in range(names.shape[0]):
                for j in range(names.shape[1]):
                    labels.append(subs[i, j] + " i=%d" % neighbors[i, j])
        subs = numpy.array(labels).reshape(subs.shape)

        if obs is not None:
            if isinstance(obs, str):
                obs = read_image(obs)
            row = numpy.array([object() for i in range(names.shape[1])])
            row[0] = obs
            names = numpy.vstack([row, names])
            text = numpy.array(["" for i in range(names.shape[1])])
            text[0] = "-"
            subs = numpy.vstack([text, subs])

        fi = None if isinstance(folder_or_images, list) else folder_or_images
        return plot_gallery_images(names, subs, return_figure=return_figure,
                                   folder_image=fi)
