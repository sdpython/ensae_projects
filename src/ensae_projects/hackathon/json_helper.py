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
    Enumerates items from a JSON file or string.

    @param      filename        filename or string or stream to parse
    @param      encoding        encoding
    @param      fLOG            logging function
    @return                     iterator on records at first level.

    It assumes the syntax follows the format: ``[ {"id":1, ...}, {"id": 2, ...}, ...]``.

    .. exref::
        :title: Processes a json file by streaming.

        The module :epkg:`ijson` can read a JSON file by streaming.
        This module is needed because a record can be written on multiple lines.
        This function leverages it produces the following results.

        .. runpython::
            :showcode:

            from ensae_projects.hackathon import enumerate_json_items

            text_json = '''
                [
                {
                    "glossary": {
                        "title": "example glossary",
                        "GlossDiv": {
                            "title": "S",
                            "GlossList": [{
                                "GlossEntry": {
                                    "ID": "SGML",
                                    "SortAs": "SGML",
                                    "GlossTerm": "Standard Generalized Markup Language",
                                    "Acronym": "SGML",
                                    "Abbrev": "ISO 8879:1986",
                                    "GlossDef": {
                                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
                                        "GlossSeeAlso": ["GML", "XML"]
                                    },
                                    "GlossSee": "markup"
                                }
                            }]
                        }
                    }
                },
                {
                    "glossary": {
                        "title": "example glossary",
                        "GlossDiv": {
                            "title": "S",
                            "GlossList": {
                                "GlossEntry": [{
                                    "ID": "SGML",
                                    "SortAs": "SGML",
                                    "GlossTerm": "Standard Generalized Markup Language",
                                    "Acronym": "SGML",
                                    "Abbrev": "ISO 8879:1986",
                                    "GlossDef": {
                                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
                                        "GlossSeeAlso": ["GML", "XML"]
                                    },
                                    "GlossSee": "markup"
                                }]
                            }
                        }
                    }
                }
                ]
            '''

            for item in enumerate_json_items(text_json):
                print('------------')
                print(item)
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
    Extracts fields from a JSON files such as images.

    @param      filename    filename
    @param      encoding    encoding
    @param      fLOG        logging function
    @return                 iterator on images

    ..warning:: Copy between two iterations?

        If you plan to store the enumerated dictionaries, you should
        copy them because dictionary are reused.

    One example on dummy data implementing a subset of the fields
    the JSON contains. This can be easily converted into a dataframe.

    .. runpython::
        :showcode:

        from ensae_projects.hackathon import extract_images_from_json_2017

        text_json = '''
            [
               {"assigned_images": [],
                "best_offer": {"created_on": "2016-11-04T23:20:53+01:00", "images": [], "offer_longitude": null, "availability": "in_stock",
                               "start_selling_date": null, "delay_before_shipping": 0.00, "free_return": null, "free_shipping": null,
                               "assigned_images": [{"image_path": "https://coucou.JPEG"}], "id": 1306501, "eco_tax": 0.000000, "keywords": ["boutique", "test"],
                "sku": "AAAA27160018",
                "product": {"pk": 2550, "external_id": null, "id": 2580},
                "description": "livre l", "last_modified": "2016-11-04T23:27:01+01:00",
                "name": "les names", "language": "fr"}, "id": 25540,
                "description": "livre 2", "slug": "les-l",
                "application_categories": [280, 283], "product_type": "physical",
                "name": "les l n", "language": "fr", "popularity": 99, "gender": null
                }
            ]
            '''

        items = []
        for item in extract_images_from_json_2017(text_json):
            print(item)
            items.append(item)

        from pandas import DataFrame
        df = DataFrame(items)
        print(df)
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
        res["product_pk"] = product.get("pk")
        res["product_id"] = product.get("id")
        res["id2"] = record.get("id2")
        res["sku"] = best.get("sku")
        res["created_on"] = record.get("created_on")
        res["keywords"] = record.get("keywords")
        if isinstance(res["keywords"], list):
            res['keywords'] = ";".join(res['keywords'])
        res["availability"] = best.get("availability")
        res["eco_tax"] = best.get("eco_tax")
        res["restock_date"] = best.get("restock_date")
        res["status"] = best.get("status")
        res["number_of_items"] = best.get("number_of_items")
        res["price_with_vat"] = best.get("price_with_vat")
        res["price_without_vat"] = best.get("price_without_vat")
        res["previous_price_without_vat"] = best.get(
            "previous_price_without_vat")
        res["max_order_quantity"] = best.get("max_order_quantity")
        res["stock"] = best.get("stock")
        res["start_selling_date"] = best.get("start_selling_date")
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
