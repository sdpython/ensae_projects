#-*- coding: utf-8 -*-
"""
@file
@brief Data related to a challenge, streets in Seattle
"""
import os
from pyensae.datasource import download_data
from pyensae.notebook_helper import folium_html_map


def get_seattle_streets(filename=None, folder="."):
    """
    Retrieve processed data from
    `Seattle Streets <https://data.seattle.gov/dataset/Street-Network-Database/afip-2mzr/data)>`_.

    @param      filename        local filename
    @param      folder          temporary folder where to download files
    @return                     shapes, records

    The function returns
    """
    if filename is None:
        download_data("WGS84_seattle_street.zip", whereTo=folder)
        filename = os.path.join(folder, "Street_Network_Database.shp")
    elif not os.path.exists(filename):
        raise FileNotFoundError(filename)
    return filename


def shapely_records(filename):
    """
    Use `pyshp <https://pypi.python.org/pypi/pyshp/>`_ to return
    shapes and records from shapefiles.

    @param      filename        filename
    @return                     shapes, records, fields

    .. faqref::
        :title: Fields in shapefiles

        The following codes is usually used to retrieve
        shapefiles:

        ::

            rshp = shapefile.Reader(filename)
            shapes = rshp.shapes()
            records = rshp.records()

        *records* contains metadata about each shape.
        Fields and values are not stored in a dictionary.
        Here is a snippet of code to do so:

        ::

            {k[0]: v for k, v in zip(rshp.fields[1:], records[0])}

        Here is an example of the results:

        ::

            {'ORD_PRE_DI': 'SW',
            'ORD_STNAME': 'SW 149TH ST',
            'ORD_STREET': '149TH',
            'ORD_STRE_1': 'ST',
            'ORD_SUF_DI': b'  ',
            'R_ADRS_FRO': 976,
            ...

    """
    import shapefile
    rshp = shapefile.Reader(filename)
    shapes = rshp.shapes()
    records = rshp.records()
    try:
        rshp.shp.close()
    except IOError:
        pass
    try:
        rshp.shx.close()
    except IOError:
        pass
    try:
        rshp.dbf.close()
    except IOError:
        pass
    return shapes, records, rshp.fields


def folium_html_street_map(subset, shapes, html_width=None, html_height=None, **kwargs):
    """
    Returns a folium map which represents the streets.

    @param      subset      list of streets index
    @param      shapes      list of shapes
    @param      kwargs      extra parameters for `Map <https://github.com/python-visualization/folium/blob/master/folium/folium.py#L19>`_
    @param      html_width  sent to function
                            `folium_html_map <http://www.xavierdupre.fr/app/pyensae/helpsphinx/pyensae/notebook_helper/folium_helper.html#pyensae.notebook_helper.folium_helper.folium_html_map>`_
    @param      html_height sent to function
                            `folium_html_map <http://www.xavierdupre.fr/app/pyensae/helpsphinx/pyensae/notebook_helper/folium_helper.html#pyensae.notebook_helper.folium_helper.folium_html_map>`_
    @return                 see function
                            `folium_html_map <http://www.xavierdupre.fr/app/pyensae/helpsphinx/pyensae/notebook_helper/folium_helper.html#pyensae.notebook_helper.folium_helper.folium_html_map>`_
    """
    import folium
    map_osm = None
    for i, index in enumerate(subset):
        shape = shapes[index]
        if map_osm is None:
            if "location" not in kwargs:
                x, y = shape.points[0]
                map_osm = folium.Map(location=[y, x], **kwargs)
            else:
                map_osm = folium.Map(kwargs["location"], **kwargs)
        map_osm.add_child(folium.PolyLine(
            locations=shape.points, latlon=False, weight=10))
        map_osm.add_child(folium.CircleMarker(
            [shape.points[0][1], shape.points[0][0]], popup=str((i, index)), radius=1))
        map_osm.add_child(folium.CircleMarker(
            [shape.points[-1][1], shape.points[-1][0]], popup=str((i, index)), radius=3))
    return folium_html_map(map_osm, width=html_width, height=html_height)


def build_streets_vertices(edges, shapes):
    """
    Returns vertices and edges based on the subset of edges.

    @param      edges       indexes
    @param      shapes      streets
    @return                 vertices, edges

    *vertices* is a list of points.
    *edges* is a list of `tuple(a, b)` where `a`, `b` are
    indices refering to the array of vertices
    """
    points = []
    for i in edges:
        p = shapes[i].points
        a, b = (p[0][0], p[0][1]), (p[-1][0], p[-1][1])
        points.append(a)
        points.append(b)
    vertices = list(sorted(set(points)))
    positions = {p: i for i, p in enumerate(vertices)}
    new_edges = []
    for i in edges:
        points = shapes[i].points
        a, b = (points[0][0], points[0][1]), (points[-1][0], points[-1][1])
        new_edges.append((positions[a], positions[b]))
    return vertices, new_edges


def plot_streets_network(edges_index, edges, vertices, shapes, ax=None, **kwargs):
    """
    Plot the network based on `basemap <http://matplotlib.org/basemap/>`_.

    @param      edges_index     index of the edges in shapes
    @param      edges           list of tuple(v1, v2) in array of vertices
    @param      vertices        list of vertices coordinates
    @param      shapes          streets
    @param      ax              axis or None
    @param      kwargs          parameter used to create the plot is ax is None
    @return                     ax

    *kwargs* may contain parameters:
    *color_v*, *color_e*, *size_v*, *size_e*, *size_c*
    """
    from mpl_toolkits.basemap import Basemap
    import numpy
    from matplotlib.collections import LineCollection
    import matplotlib.pyplot as plt
    params = ["color_v", "color_e", "size_v", "size_e"]
    if ax is None:
        options = {k: v for k, v in kwargs.items() if k not in params}
        fig, ax = plt.subplots(**options)
    x1, x2 = min(_[0] for _ in vertices), max(_[0] for _ in vertices)
    y1, y2 = min(_[1] for _ in vertices), max(_[1] for _ in vertices)
    dx, dy = (x2 - x1) * 0.2, (y2 - y1) * 0.2
    x1 -= dx
    x2 += dx
    y1 -= dy
    y2 += dy
    m = Basemap(resolution='i', projection='merc', llcrnrlat=y1, urcrnrlat=y2,
                llcrnrlon=x1, urcrnrlon=x2, lat_ts=(y1 + y2) / 2, ax=ax)
    m.drawcountries(linewidth=0.5)
    m.drawcoastlines(linewidth=0.5)
    for n in edges_index:
        sh = shapes[n]
        geo_points = sh.points
        lons = [_[0] for _ in geo_points]
        lats = [_[1] for _ in geo_points]
        data = numpy.array(m(lons, lats)).T
        segs = [data, ]
        lines = LineCollection(segs, antialiaseds=(1,))
        lines.set_edgecolors("black")
        lines.set_linewidth(kwargs.get('size_e', 2))
        ax.add_collection(lines)
        mx, my = (lons[0] + lons[-1]) / 2, (lats[0] + lats[-1]) / 2
        gx, gy = m(mx, my)
        ax.text(gx, gy, "e%d" % n, color=kwargs.get('color_e', "blue"))
    for n, (a, b) in enumerate(vertices):
        gx, gy = m(a, b)
        c = plt.Circle((gx, gy), kwargs.get('size_c', 5), color='black')
        ax.add_artist(c)
        ax.text(gx, gy, "v%d" % n, size=kwargs.get('size_v', 12),
                color=kwargs.get('color_v', "red"))
    return ax


def connect_streets(st1, st2):
    """
    Tells if streets `st1`, `st2` are connected.

    @param      st1     street 1
    @param      st2     street 2
    @return             tuple or tuple (0 or 1, 0 or 1)

    Each tuple means:

    * 0 or 1 mean first or last extremity or the first street
    * 0 or 1 mean first or last extremity or the second street

    ``((0, 1),)`` means the first point of the first street is connected
    to the second extremity of the second street.
    """
    a1, b1 = st1[0], st1[-1]
    a2, b2 = st2[0], st2[-1]
    connect = []
    if a1 == a2:
        connect.append((0, 0))
    if a1 == b2:
        connect.append((0, 1))
    if b1 == a2:
        connect.append((1, 0))
    if b1 == b2:
        connect.append((1, 1))
    return tuple(connect) if connect else None


def _complete_subset_streets(edges, shapes):
    """
    Extends a set of edges to have less extermities into the graph
    composed by the sets of edges.

    @param      edges       list of indices in shapes
    @param      shapes      streets
    @return                 added edges (indices)
    """
    sedges = set(edges)
    extension = []
    for i, shape in enumerate(shapes):
        if i in sedges:
            continue
        add = []
        for s in edges:
            if s != i:
                con = connect_streets(shapes[s].points, shapes[i].points)
                if con is not None:
                    add.extend([_[1] for _ in con])
        if len(set(add)) == 2:
            extension.append(i)
    return extension


def _enumerate_close(lon, lat, shapes, th=None):
    """
    Enumerate close streets from a starting point.

    @param      lon     longitude
    @param      lat     latitude
    @param      shapes  list of streets
    @param      th      threshold or None for all
    @return             iterator on *tuple(distance, i)*
    """
    from shapely.geometry import Point, LineString
    p = Point(lon, lat)
    for i, shape in enumerate(shapes):
        obj = LineString(shape.points)
        d = p.distance(obj)
        if th is None or d <= th:
            yield d, i


def seattle_streets_set_small(shapes, size=20):
    """
    Returns a small graph of streets.

    @param      shapes      list of streets
    @param      size        number of elements
    @return                 indices of edges, edges, vertices, distances
    """
    from shapely.geometry import LineString
    lon, lat = -122.34651954599997, 47.46947199700003
    x, y = shapes[0].points[0]
    closes = list(_enumerate_close(lon, lat, shapes))
    closes.sort()
    subset = [index for dist, index in closes[:20]]
    newset = list(set(subset + _complete_subset_streets(subset, shapes)))
    vertices, edges = build_streets_vertices(newset, shapes)
    distances = [LineString(shapes[i].points).length for i in newset]
    return newset, edges, vertices, distances
