# -*- coding: utf-8 -*-
"""
@file
@brief Helpers for the hackathon 2017 (Label Emmaüs).
"""
import os
from io import BytesIO
from collections import Counter
import hashlib
import pickle
import warnings
import shutil
import numpy
from numpy.random import RandomState
import pandas
from sklearn.model_selection import train_test_split
from PIL import Image


def resize_image(filename_or_bytes, maxdim=512, dest=None, format=None):  # pylint: disable=W0622
    """
    Resizes an image until one of its dimension becomes smaller
    than *maxdim* after dividing the dimensions by two many times.

    @param      filename_or_bytes   filename or bytes
    @param      maxdim              maximum dimension
    @param      dest                if filename is a str
    @param      format              saved image format (if *filename_or_bytes* is bytes)
    @return                         same type
    """
    if isinstance(filename_or_bytes, str):
        ext = os.path.splitext(filename_or_bytes)[-1][1:]
        with open(filename_or_bytes, "rb") as f:
            r = resize_image(f.read(), maxdim=maxdim, format=ext)
        if dest is None:
            dest = filename_or_bytes
        with open(dest, "wb") as f:
            f.write(r)
        return None
    elif isinstance(filename_or_bytes, bytes):
        st = BytesIO(filename_or_bytes)
        img = Image.open(st)
        new_size = img.size
        mn = min(new_size)
        while mn > maxdim:
            new_size = (new_size[0] // 2, new_size[1] // 2)
            mn = min(new_size)
        if new_size == img.size:
            return filename_or_bytes
        else:
            mapping = {'jpg': 'jpeg'}
            img = img.resize(new_size)
            st = BytesIO()
            img.save(st, format=mapping.get(format.lower(), format))
            return st.getvalue()
    else:
        raise TypeError("Unexpected type '{0}'".format(
            type(filename_or_bytes)))


def read_image(filename_or_bytes):
    """
    Reads an image.

    @param      filename_or_bytes   filename or bytes
    @return                         :epkg:`PIL.Image`
    """
    if isinstance(filename_or_bytes, str):
        with open(filename_or_bytes, "rb") as f:
            return read_image(f.read())
    elif isinstance(filename_or_bytes, bytes):
        st = BytesIO(filename_or_bytes)
        return Image.open(st)
    else:
        raise TypeError("Unexpected type '{0}'".format(
            type(filename_or_bytes)))


def enumerate_image_class(folder, abspath=True, ext={'.jpg', '.png'}):  # pylint: disable=W0102
    """
    Lists all images in one folder assuming subfolders
    indicates the class of each image belongs to.

    @param      folder      folder
    @param      abspath     use absolute paths
    @param      ext         allowed extensions
    @return                 list of (filename, class)
    """
    if not os.path.exists(folder):
        raise FileNotFoundError("Unable to find '{0}'".format(folder))
    for root, _, files in os.walk(folder, topdown=False):
        for name in files:
            e = os.path.splitext(name)[-1]
            if e not in ext:
                continue
            if abspath:
                name = os.path.join(root, name)
            else:
                name = os.path.join(os.path.relpath(root, folder), name)
            fold = os.path.split(name)[0]
            sub = os.path.split(fold)[-1]
            yield name, sub


def histogram_image_size(folder, ext={'.jpg', '.png'}):  # pylint: disable=W0102
    """
    Computes the distribution of images size.

    @param      folder      folder
    @param      ext         allowed extensions
    @return                 histogram
    """
    def get_size(name):
        r = read_image(name)
        return r.size

    return Counter(map(lambda r: get_size(r[0]), enumerate_image_class(folder, ext=ext)))


def img2gray(img, mode='L'):
    """
    Converts an image (:epkg:`PIL`) to gray scale.

    @param      img     see :epkg:`PIL.Image`
    @param      mode    ``'L'`` or ``'LA'``
    @return             see :epkg:`PIL.Image`
    """
    return img.convert(mode)


def stream_apply_image_transform(src_folder, dest_folder, transform,  # pylint: disable=W0102
                                 ext={'.png', '.jpg'}, fLOG=None):
    """
    Applies a transform on every image in a folder,
    saves it in another one. It keeps the same subfolders.

    @param      src_folder      source folder
    @param      dest_folder     destination folder
    @param      transform       function, ``trans(img) -> img``
    @param      ext             image extension to consider
    @param      logging         function
    @return                     number of processed image

    The function yields every created filename and returns
    an iterator.

    Example::

        list(stream_apply_image_transform(src, fest, lambda im: img2gray(im)))
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    for ii, (img, sub) in enumerate(enumerate_image_class(src_folder, ext=ext, abspath=False)):
        if fLOG is not None and ii % 1000 == 0:
            fLOG(
                "[apply_image_transform] processing image {0}: '{1}' - class '{2}'".format(ii, img, sub))
        i = read_image(os.path.join(src_folder, img))
        fold, name = os.path.split(img)
        n = transform(i)
        dfold = os.path.join(dest_folder, fold)
        if not os.path.exists(dfold):
            os.makedirs(dfold)
        fd = os.path.join(dfold, name)
        n.save(fd)
        yield fd


def image_zoom(img, new_size, **kwargs):
    """
    Applies :epkg:`PIL:Image:resize`.


    @param  img         :epkg:`PIL.Image`
    @param  new_size    size after zoom
    @param  kwargs      additional arguments
    @return             new image
    """
    return img.resize(new_size, **kwargs)


def stream_image2features(src_folder, dest_folder, transform, batch_size=1000,  # pylint: disable=W0102
                          prefix="batch", ext={'.png', '.jpg'}, fLOG=None):
    """
    Considers all images in a folder, transform them into
    features (function *transform*) and saves them
    with :epkg:`pickle` into :epkg:`numpy` arrays by batch.

    @param      src_folder  folder which contains images
    @param      dest_folder destination of the batches
    @param      transform   from image to features,
                            function, ``trans(img) -> numpy.array``
    @param      batch_size  number of images to save together
    @param      prefix      prefix name for the batch files
    @param      ext         list of extensions to process
    @param      fLOG        logging function
    @return                 list of written files (iterator)

    The function yields a batch file when one is ready. It does
    not wait the end before returning all of them. The saved files
    contains two arrays, first one for the features, second one
    for the classes.

    Example::

        list(stream_image2features(this, temp,
                lambda im: numpy.array(image_zoom(img2gray(im), (10, 12)))))
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    def save_batch(nb, features, subs):
        conc = numpy.vstack(features)

        name = "%s%d.pkl" % (os.path.join(dest_folder, prefix), nb)
        fold = os.path.dirname(name)
        if not os.path.exists(fold):
            os.makedirs(fold)

        with open(name, "wb") as f:
            pickle.dump([conc, numpy.array(subs)], f)
        return name

    features = []
    subs = []
    nbatch = 0
    for ii, (img, sub) in enumerate(enumerate_image_class(src_folder, ext=ext, abspath=False)):
        i = read_image(os.path.join(src_folder, img))
        feat = transform(i)
        features.append(feat)
        subs.append(sub)

        if len(features) >= batch_size:
            filename = save_batch(nbatch, features, subs)
            yield os.path.relpath(filename, dest_folder)
            if fLOG:
                fLOG(
                    "[stream_image2features] save file '{0}' - {1} seen images.".format(filename, ii))
            nbatch += 1
            features.clear()
            subs.clear()

    if len(features) > 0:
        filename = save_batch(nbatch, features, subs)
        yield os.path.relpath(filename, dest_folder)
        if fLOG:
            fLOG("[stream_image2features] save file '{0}'.".format(filename))


def load_batch_features(batch_file):
    """
    Loads a batch file saved by @see fn stream_image2features.

    @param      batch_file      batch file
    @return                     features, classes
    """
    with open(batch_file, "rb") as f:
        return pickle.load(f)


def enumerate_batch_features(folder, batch_or_image=False):
    """
    Enumerates all batches saved in a folder.

    @param      folder          folder where to find the batches.
    @param      batch_or_image  False to enumerate filenames,
                                True for couple (features, class)
    @return                     enumerator
    """
    batches = os.listdir(folder)
    for b in batches:
        ext = os.path.splitext(b)[-1]
        if ext == '.pkl':
            if batch_or_image:
                feat, cl = load_batch_features(os.path.join(folder, b))
                for i in range(cl):
                    yield feat[i], cl[i]
            else:
                yield b


def stream_download_images(urls, dest_folder, fLOG=None, use_request=None,
                           skipif_done=True, dummys=None, skip=0):
    """
    Downloads images based on their urls.

    @param  urls            filename or list of urls
    @param  dest_folder     destination folder
    @param  fLOG            logging function
    @param  use_request     None to let the function choose,
                            True to use :epkg:`urllib3`,
                            False to use :epkg:`*py:urllib:request`.
    @param  skipif_done     skip if the image was already downloaded
    @param  dummys          some website returns a dummy image to tell there is no
                            image at this specific address, if an image is part
                            of this set of images, it is ignored,
                            if the value is None, it is replaced by a default set
                            of images
    @param  skip            skip the first images
    @return                 enumerator on created files

    The function continue if an error occurs.
    Use ``fLOG=print`` to see which url failed.
    Parameter *dummys* can be set to avoid images like
    the following:

    .. image:: empty.jpg
        :width: 100

    The function does not download an image already downloaded
    but still yields it.
    """
    if isinstance(urls, str):
        with open(urls, "r", encoding='utf-8') as f:
            urls = [_.strip("\n\r\t ") for _ in f.readlines()]
            urls = [_ for _ in urls if _]

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    if use_request is None:
        use_request = False

    leave = None

    try:
        if use_request:
            raise ImportError("Cannot use urllib3")
        import urllib3
        from urllib3.exceptions import HTTPError

        timeout = urllib3.Timeout(connect=2.0, read=8.0)
        http = urllib3.PoolManager(timeout=timeout)

        def download(url, fLOG):
            with warnings.catch_warnings(record=True) as ws:
                warnings.simplefilter("ignore")
                try:
                    r = http.request('GET', url)
                    if r.status == 200:
                        return r.data
                    else:
                        if fLOG:
                            fLOG("[stream_download_images] error {0} for url '{1}'.".format(
                                r.status, url))
                        return None
                    for w in ws:
                        if fLOG:
                            fLOG(
                                "[stream_download_images] warning {0} for url '{1}'.".format(w, url))
                except HTTPError as e:
                    if fLOG:
                        fLOG(
                            "[stream_download_images] fails for url '{0}' due to {1}.".format(url, e))
                    return None

        leave = http

    except ImportError:
        if not use_request:
            raise
        from urllib.request import Request, urlopen
        from urllib.error import URLError

        def download(url, fLOG):
            with warnings.catch_warnings(record=True) as ws:
                warnings.simplefilter("ignore")
                try:
                    req = Request(url)
                    with urlopen(req, timeout=10) as f:
                        try:
                            return f.read()
                        except Exception as e:  # pylint: disable=W0703
                            if fLOG:
                                fLOG(
                                    "[stream_download_images] error {0} for url '{1}'.".format(e, url))
                            return None
                    for w in ws:
                        if fLOG:
                            fLOG(
                                "[stream_download_images] warning {0} for url '{1}'.".format(w, url))
                except URLError as e:
                    if fLOG:
                        fLOG(
                            "[stream_download_images] fails for url '{0}' due to {1}.".format(url, e))
                    return None

    this = os.path.dirname(__file__)
    if dummys is None:
        dummys = [
            numpy.array(read_image(os.path.join(this, "empty.jpg"))).ravel(),
        ]

    for i, url in enumerate(urls):
        if i < skip:
            continue
        if fLOG and i % 100 == 0:
            fLOG(
                "[stream_download_images] ... {0}/{1}: '{2}'".format(i + 1, len(urls), url))
        name = url.split('/')[-1].replace("..", ".")
        for c in "?:%":
            name = name.replace(c, "")
        ext = os.path.splitext(name)[-1]
        if len(ext) not in (4, 5) or ext[0] != '.':
            if fLOG:
                fLOG(
                    "[stream_download_images] wrong filename for url '{0}'.".format(url))
            continue

        dest = os.path.join(dest_folder, name)
        if skipif_done and os.path.exists(dest):
            yield name
            continue
        try:
            data = download(url, fLOG)
        except UnicodeEncodeError as e:
            if fLOG:
                fLOG(
                    "[stream_download_images] fails for url '{0}' due to {1}.".format(url, e))
            continue

        if data is not None:

            try:
                img = read_image(data)
            except Exception as e:  # pylint: disable=W0703
                if fLOG:
                    fLOG("[stream_download_images] cannot load image for url '{0}' due to {1}".format(
                        url, e))
                    continue

            imgr = numpy.array(img).ravel()
            ok = True
            for idu, dummy in enumerate(dummys):
                if imgr.shape != dummy.shape:
                    continue
                if numpy.max(numpy.abs(dummy - imgr)) == 0:
                    ok = False
                    if fLOG:
                        fLOG("[stream_download_images] empty image '{0}' equal to dummy {1}".format(
                            url, idu))
                    break

            if ok:
                with open(dest, "wb") as f:
                    f.write(data)
                yield name

    if leave:
        leave.clear()


def stream_copy_images(src_folder, dest_folder, valid, ext={'.jpg', '.png'}, fLOG=None):  # pylint: disable=W0102
    """
    Copies all images from *src_folder* to *dest_folder*
    if *valid(name)* is True.

    @param      src_folder      source folder
    @param      dest_folder     destination folder
    @param      valid           function ``valid(name) -> bool``
    @param      ext             allowed extensions
    @param      fLOG            loggung function
    @return                     iterator on copied files
    """
    for i, (img, sub) in enumerate(enumerate_image_class(src_folder, ext=ext, abspath=False)):
        if fLOG is not None and i % 1000 == 0:
            fLOG(
                "[stream_copy_images] copy image {0}: '{1}' - class '{2}'".format(i, img, sub))
        if not valid(img):
            continue
        dst = os.path.join(dest_folder, img)
        fold = os.path.dirname(dst)
        if not os.path.exists(fold):
            os.makedirs(fold)
        shutil.copy(os.path.join(src_folder, img), dst)
        yield dst


def stream_random_sample(folder, n=1000, seed=None, abspath=True,  # pylint: disable=W0102
                         ext={'.jpg', '.png'}):
    """
    Extracts a random sample from a folder which contains many images.
    Relies on fonction @see fn enumerate_image_class.

    @param      folder      folder
    @param      n           number of requested images
    @param      seed        seed
    @param      abspath     use absolute paths
    @param      ext         allowed extensions
    @return                 list of (filename, class)

    The function is a streaming function, it yields the current
    state of a sample drawn with the :epkg:`reservoir sampling`
    algorithm. It also works with

    .. runpython::
        :showcode:

        import os
        from ensae_projects.hackathon.image_helper import stream_random_sample, last_element

        this = os.path.join(os.path.dirname(__file__), '..')
        res = last_element(stream_random_sample(this, abspath=False, ext={'.py', '.rst', '.pyc'}))
        print(res)
    """
    sample = []
    state = RandomState(seed=seed)
    for i, (img, sub) in enumerate(enumerate_image_class(folder, abspath=abspath, ext=ext)):
        if len(sample) < n:
            sample.append((img, sub))
        else:
            j = state.randint(0, i)
            if j < n:
                sample[j] = (img, sub)
        yield sample


def last_element(iter):  # pylint: disable=W0622
    """
    Returns the last element of sequence assuming they
    were generated by an iterator or a generator.

    @param      iter        iterator or generator
    @return                 element

    .. runpython::
        :showcode:

        from ensae_projects.hackathon.image_helper import last_element

        def gen():
            for i in range(10):
                yield "A%d" % i

        print(last_element(gen()))
    """
    el = None
    for el in iter:
        pass
    return el


def plot_gallery_random_images(folder, n=12, seed=None,  # pylint: disable=W0102
                               ext={'.jpg', '.png'}, **kwargs):
    """
    Plots a gallery of images using :epkg:`matplotlib`.
    Extracts a random sample from a folder which contains many images.
    Relies on fonction @see fn enumerate_image_class.
    Calls :epkg:`plot_gallery_images` to build the gallery.

    @param      folder      folder
    @param      n           number of requested images
    @param      seed        seed
    @param      ext         allowed extensions
    @param      kwargs      argument to send to :epkg:`matplotlib`
    @return                 tuple (ax, random sample)

    The function is a streaming function, it yields the current
    state of a sample drawn with the :epkg:`reservoir sampling`
    algorithm. It also works with
    """
    def hash_md5(name):
        m = hashlib.md5()
        m.update(name.encode('utf-8'))
        res = m.hexdigest()
        if len(res) > 4:
            res = res[:4]
        return res

    from mlinsights.plotting import plot_gallery_images
    rnd = last_element(stream_random_sample(
        folder, n=n, seed=seed, abspath=False, ext=ext))
    imgs = [os.path.join(folder, _[0]) for _ in rnd]
    if isinstance(imgs[0], str):
        texts = [hash_md5(nm) for nm in imgs]
    else:
        texts = list(str(_) for _ in range(len(imgs)))
    ax = plot_gallery_images(imgs, texts, **kwargs)
    rnd = [(t,) + cu for t, cu in zip(texts, rnd)]
    return ax, rnd


def folder_split_train_test(src_folder, dest_train, dest_test, seed=None,  # pylint: disable=W0102
                            ext={'.jpg', '.png'}, test_size=0.25):
    """
    Splits images from a folder into train and test.
    The function saves images into two separate folders.

    @param      src_folder          source folder
    @param      dest_train          destination folder for the train set
    @param      dest_test           destination folder for the test set
    @param      ext                 desired extensions
    @param      seed                random seed
    @param      test_size           test ratio
    @return                         list of copied files in a 2-uple

    The function relies on @see fn enumerate_image_class
    to extract the image from folder *src_folder*.
    The subfolder is used to perform a stratitied split.
    """
    images = list(enumerate_image_class(src_folder, abspath=False, ext=ext))
    df = pandas.DataFrame(data=images, columns=["name", "sub"])
    df_train, df_test = train_test_split(df, test_size=test_size, random_state=seed,
                                         shuffle=True, stratify=df['sub'])

    def dump_images(imgs, fold):
        copied = []
        for img in imgs:
            src = os.path.join(src_folder, img)
            dst = os.path.join(fold, img)
            d = os.path.dirname(dst)
            if not os.path.exists(d):
                os.makedirs(d)
            shutil.copy(src, dst)
            copied.append(dst)
        return copied

    img_train = df_train["name"]
    img_test = df_test["name"]
    tr = dump_images(img_train, dest_train)
    te = dump_images(img_test, dest_test)
    return tr, te
