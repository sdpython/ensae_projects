# -*- coding: utf-8 -*-
"""
@file
@brief Helpers for the hackathon 2017 (Label Emmaüs).
"""
import os
from io import BytesIO
from PIL import Image


def resize_image(filename_or_bytes, maxdim=512, dest=None, format=None):
    """
    Resizes an image until one of its dimension becomes smaller
    than *maxdim* after dividing the dimensions by two many times.

    @param      filename        filename or bytes
    @param      maxdim          maximum dimension
    @param      dest            if filename is a str
    @param      format          saved image format (if *filename_or_bytes* is bytes)
    @return                     same type
    """
    if isinstance(filename_or_bytes, str):
        ext = os.path.splitext(filename_or_bytes)[-1][1:]
        with open(filename_or_bytes, "rb") as f:
            r = resize_image(f.read(), maxdim=maxdim, format=ext)
        if dest is None:
            dest = filename_or_bytes
        with open(dest, "wb") as f:
            f.write(r)
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
