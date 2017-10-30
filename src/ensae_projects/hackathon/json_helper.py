# -*- coding: utf-8 -*-
"""
@file
@brief Helpers for the hackathon 2017 (Label Emmaüs).
"""
import ijson
import os
from io import StringIO
from pyquickhelper.loghelper import noLOG


def enumerate_json_items(filename, encoding=None, fLOG=noLOG):
    """
    Enumerates items from a JSON files.

    @param      filename        filename or string or stream to parse
    @param      encoding        encoding
    @param      fLOG            logging function
    @return                     iterator on records at first level.

    We assume the syntax follows the format: ``[ {"id":1, ...}, {"id": 2, ...}, ...]``.
    """
    if isinstance(filename, str):
        if "{" not in filename and os.path.exists(filename):
            with open(filename, "r", encoding=encoding) as f:
                for el in enumerate_json_items(f, encoding=encoding, fLOG=fLOG):
                    yield el
        else:
            st = StringIO(filename)
            for el in enumerate_json_items(st, encoding=encoding, fLOG=fLOG):
                yield el
    else:
        parser = ijson.parse(filename)
        current = None
        curkey = None
        stack = []
        nbyield = 0
        for i, (prefix, event, value) in enumerate(parser):
            if i % 1000000 == 0:
                fLOG("[enumerate_json_items] i={0} yielded={1}".format(
                    i, nbyield))
            if event == "start_array":
                if curkey is None:
                    current = []
                else:
                    if not isinstance(current, dict):
                        raise RuntimeError(
                            "Type issue {0}".format(type(current)))
                    c = []
                    current[curkey] = c
                    current = c
                curkey = None
                stack.append(current)
            elif event == "end_array":
                stack.pop()
                if len(stack) == 0:
                    # We should be done.
                    current = None
                else:
                    current = stack[-1]
            elif event == "start_map":
                c = {}
                if curkey is None:
                    current.append(c)
                else:
                    current[curkey] = c
                stack.append(c)
                current = c
                curkey = None
            elif event == "end_map":
                stack.pop()
                current = stack[-1]
                if len(stack) == 1:
                    nbyield += 1
                    yield current[-1]
                    # We clear the memory.
                    current.clear()
            elif event == "map_key":
                curkey = value
            elif event in {"string", "number", "boolean"}:
                if curkey is None:
                    current.append(value)
                else:
                    current[curkey] = value
                    curkey = None
            elif event == "null":
                if curkey is None:
                    current.append(None)
                else:
                    current[curkey] = None
                    curkey = None
            else:
                raise ValueError("Unknown event '{0}'".format(event))


def extract_images_from_json_2017(filename, encoding=None, fLOG=noLOG):
    """
    Extracts images from *filename*.

    @param      filename    filename
    @param      encoding    encoding
    @param      fLOG        logging function
    @return                 iterator on images

    ..warning:: Copy between two iterations?

        If you plan to store the enumerated dictionaries, you should
        copy them because dictionary are reused.
    """
    for record in enumerate_json_items(filename, encoding=encoding, fLOG=fLOG):
        images = []
        if "best_offer" in record and record["best_offer"]:
            best = record["best_offer"]
            if "assigned_images" in best and best["assigned_images"]:
                images.extend(best["assigned_images"])
        else:
            continue
        product = best.get("product")
        if product is None:
            continue
        if "assigned_images" in record and record["assigned_images"]:
            images.extend(record["assigned_images"])
        res = {}
        res["pk"] = product.get("pk")
        res["id"] = product.get("id")
        res["id2"] = record.get("id2")
        res["sku"] = best.get("sku")
        res["description"] = record.get("description")
        if isinstance(res["description"], str):
            res["description"] = res["description"].replace(
                "\n", "\\n").replace("\t", "\\t").replace("\r", "")
        res["last_modified"] = best.get("last_modified")
        res["name"] = record.get("name")
        res["product_type"] = record.get("product_type")
        res["gender"] = record.get("gender")
        res["popularity"] = record.get("popularity")
        res["application_categories"] = record.get("application_categories")
        if isinstance(res["application_categories"], list):
            res["application_categories"] = ",".join(
                map(str, res["application_categories"]))
        res["language"] = record.get("language")
        paths = list(im.get("image_path") for im in images)
        done = set()
        for p in paths:
            if p and p not in done:
                res["image_path"] = p
                yield res
                done.add(p)
