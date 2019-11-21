"""
@file
@brief Functions to handle data coming from
:epkg:`Cancer Imaging Archive`.
"""
import os
import pydicom
import cv2
import pandas
from pyquickhelper.filehelper.synchelper import explore_folder_iterfile


def _recurse_fill(obs, dataset, parent=""):
    for data_element in dataset:
        if isinstance(data_element.value, bytes):
            continue
        if data_element.VR == "SQ":   # a sequence
            name = data_element.name
            for i, ds in enumerate(data_element.value):
                _recurse_fill(obs, ds,
                              parent="{parent}.{name}[{i}]".format(
                                  parent=parent, name=name, i=i))
        else:
            text = str(data_element.value)
            name = str(data_element.name)
            key = name if parent == '' else parent + "." + name
            obs[key] = text


def convert_dcm2png(folder, dest, fLOG=None):
    """
    Converts all medical images in a folder from format
    :epkg:`dcm` to :epkg:`png`.

    @param      folder      source folder
    @param      dest        destination folder
    @param      fLOG        logging function
    @return                 :epkg:`pandas:DataFrame` with many data

    The function uses module :epkg:`pydicom`.
    """
    if not os.path.exists(dest):
        raise FileNotFoundError("Unable to find folder '{}'.".format(dest))
    if fLOG is not None:
        fLOG("[convert_dcm2png] convert dcm files from '{}'.".format(folder))
        fLOG("[convert_dcm2png] into '{}'.".format(dest))
    done = {}
    rows = []
    for name in explore_folder_iterfile(folder, ".*[.]dcm$"):
        relname = os.path.relpath(name, folder)
        if fLOG is not None:
            fLOG("[convert_dcm2png] read {}: '{}'.".format(
                len(rows) + 1, relname))
        f1 = relname.replace("\\", "/").split("/")[0]
        name_ = "img_%06d.png" % len(done)
        if "_" in f1:
            sub = f1.split('_')[0]
            fsub = os.path.join(dest, sub)
            if not os.path.exists(fsub):
                if fLOG is not None:
                    fLOG("[convert_dcm2png] create folder '{}'.".format(sub))
                os.mkdir(fsub)
            new_name = os.path.join(sub, name_)
        else:
            new_name = name_

        # read
        ds = pydicom.dcmread(name)

        # data
        obs = dict(_src=relname, _dest=new_name, _size=len(ds.pixel_array))
        _recurse_fill(obs, ds)
        rows.append(obs)

        # image
        full_name = os.path.join(dest, new_name)
        if os.path.exists(full_name):
            done[name] = full_name
            continue

        pixel_array_numpy = ds.pixel_array
        cv2.imwrite(full_name, pixel_array_numpy)  # pylint: disable=E1101
        done[name] = full_name

    final = os.path.join(dest, "_summary.csv")
    if fLOG is not None:
        fLOG("[convert_dcm2png] converted {} images.".format(len(rows)))
        fLOG("[convert_dcm2png] write '{}'.".format(final))
    df = pandas.DataFrame(rows)
    df.to_csv(final, index=False, encoding="utf-8")
    return df
