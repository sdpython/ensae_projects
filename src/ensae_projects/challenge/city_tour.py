"""
@file
@brief  Function to solve the problem of the
`Route Inspection Problem <https://en.wikipedia.org/wiki/Route_inspection_problem>`_.
"""
import math
import random
import fractions


class SolutionException(Exception):
    """
    wrong solution
    """
    pass


def haversine_distance(lat1, lng1, lat2, lng2):
    """
    Computes `Haversine formula <http://en.wikipedia.org/wiki/Haversine_formula>`_.

    .. index:: Haversine

    @param      lat1    lattitude
    @param      lng1    longitude
    @param      lat2    lattitude
    @param      lng2    longitude
    @return             distance
    """
    radius = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lng2 - lng1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d


def distance_solution(edges_index, edges, distances, solution, exc=True):
    """
    Checks if a solution is really a solution and returns the distance of it,
    None if it is not a solution. The function does not case about the order.

    @param      edges_index     list of indices of edges (if None --> range(len(edges))
    @param      edges           list of tuple (vertex A, vertex B)
    @param      distances       list of distances of each edge
    @param      solution        proposed solutions (list of edge indices)
    @param      exc             raises an exception in case of error
    """
    if edges_index is None:
        edges_index = list(range(len(edges)))
    indices = set(edges_index)
    solset = set(solution)
    if len(indices) != len(solset):
        if exc:
            raise SolutionException("Different number of distinct edges:\nexpected={0} got={1}\n"
                                    "Did you cover all the edges?".format(len(indices), len(solset)))
        else:
            return None

    for s in solution:
        if s not in indices:
            raise SolutionException(
                "Index {0} is not in edges_index".format(s))

    doubles = {}
    for a, b in edges:
        if a > b:
            a, b = b, a
        if (a, b) in doubles:
            if exc:
                raise SolutionException(
                    "Edge {0} is duplicated in edges.".format((a, b)))
            else:
                return None
        doubles[a, b] = 1

    corres = {e: i for i, e in enumerate(edges_index)}
    degrees = {}
    for s in solution:
        a, b = edges[corres[s]]
        degrees[a] = degrees.get(a, 0) + 1
        degrees[b] = degrees.get(b, 0) + 1

    odd, even = 0, 0
    for d in degrees.values():
        if d % 2 == 0:
            even += 1
        else:
            odd += 1

    if odd > 2:
        if exc:
            red = list(sorted([(k, v)
                               for k, v in degrees.items() if v % 2 != 0]))
            if len(red) > 10:
                red = red[:10] + ["..."]
            raise SolutionException(
                "Are you sure? The path is inconsistent. Some help:\n" + str(red))
        else:
            return None
    else:
        return sum(distances[corres[s]] for s in solution)


def compute_degrees(edges):
    """
    Compute the degree of vertices.

    @param      edges       list of tuple
    @return                 dictionary {key: degree}
    """
    res = {}
    for a, b in edges:
        res[a] = res.get(a, 0) + 1
        res[b] = res.get(b, 0) + 1
    return res


def euler_path(edges_index, edges, solution):
    """
    Computes an Eulerian path.

    .. index:: Eulerian

    @param      edges_index     list of indices of edges (if None --> range(len(edges))
    @param      edges           list of tuple (vertex A, vertex B)
    @param      solution        proposed solutions (list of edge indices)
    @return                     path, list of edges indices

    The function assumes every vertex in the graph defined by *edges*
    has an even degree.
    """
    if edges_index is None:
        edges_index = range(len(edges))
    pos = {k: i for i, k in enumerate(edges_index)}
    indices = [pos[s] for s in solution]
    edges = [edges[i] for i in indices]

    degrees = compute_degrees(edges)
    odd = {k: v for k, v in degrees.items() if v % 2 == 1}
    if len(odd) not in (0, 2):
        odd = list(sorted((k, v) for k, v in odd.items()))
        if len(odd) > 10:
            odd = odd[:10] + ["..."]
        raise SolutionException(
            "Some vertices have an odd degree. This is not allowed.\n" + str(odd))

    if len(odd) == 2:
        # we add an extra edge which we remove later
        odd = list(odd.keys())
        remove = (odd[0], odd[1])
        edges.append(remove)
    else:
        remove = None

    res = _euler_path(edges)
    pathi = [_[1][0] for _ in res]
    if remove is not None:
        index = pathi.index(len(edges) - 1)
        if index == 0:
            pathi = pathi[1:]
        elif index == len(edges) - 1:
            pathi = pathi[:-1]
        else:
            pathi = pathi[index + 1:] + pathi[:index]
    pathi = [solution[i] for i in pathi]
    return pathi


def _euler_path(edges):
    """
    Computes an Eulerian path.

    @param      edges           edges
    @return                     path, list of (vertex,edge)

    The function assumes every vertex in the graph defined by *edges*
    has an even degree.
    """
    alledges = {}
    edges_from = {}
    for i, k in enumerate(edges):
        if isinstance(k, list):
            k = tuple(k)
        v = (i,) + k
        alledges[k] = v
        a, b = k
        alledges[b, a] = alledges[a, b]
        if a not in edges_from:
            edges_from[a] = []
        if b not in edges_from:
            edges_from[b] = []
        edges_from[a].append(alledges[a, b])
        edges_from[b].append(alledges[a, b])

    degre = {}
    for a, v in edges_from.items():
        t = len(v)
        degre[t] = degre.get(t, 0) + 1

    two = [a for a, v in edges_from.items() if len(v) == 2]
    odd = [a for a, v in edges_from.items() if len(v) % 2 == 1]
    if len(odd) not in (0, 2):
        add = "\n" + str(odd) if len(odd) < 10 else ""
        raise SolutionException(
            "Some vertices have an odd degree. This is not allowed." + add)

    begin = two[0]

    # checking
    for v, le in edges_from.items():
        for e in le:
            to = e[1] if v != e[1] else e[2]
            if to not in edges_from:
                raise SolutionException(
                    "Unable to find vertex {0} for edge ({0},{1}).".format(to, v))
            if to == v:
                raise SolutionException("Circular edge {0}.".format(to))

    # loop
    path = _explore_path(edges_from, begin)
    for p in path:
        if len(p) == 0:
            raise NotImplementedError("This exception should not happen.")
    while len(edges_from) > 0:
        start = None
        for i, p in enumerate(path):
            if p[0] in edges_from:
                start = i, p
                break
        sub = _explore_path(edges_from, start[1][0])
        i = start[0]
        path[i:i + 1] = path[i:i + 1] + sub
    return path


def _delete_edge(edges_from, n, to):
    """
    Removes an edge from the graph.

    @param      edges_from      structure which contains the edges (will be modified)
    @param      n               first vertex
    @param      to              second vertex
    @return                     the edge
    """
    le = edges_from[to]
    f = None
    for i, e in enumerate(le):
        if (e[1] == to and e[2] == n) or (e[2] == to and e[1] == n):
            f = i
            break

    assert f is not None
    del le[f]
    if len(le) == 0:
        del edges_from[to]

    le = edges_from[n]
    f = None
    for i, e in enumerate(le):
        if (e[1] == to and e[2] == n) or (e[2] == to and e[1] == n):
            f = i
            break

    assert f is not None
    keep = le[f]
    del le[f]
    if len(le) == 0:
        del edges_from[n]

    return keep


def _explore_path(edges_from, begin):
    """
    Explores an Eulerian path, remove used edges from *edges_from*.

    @param      edges_from      structure which contains the edges (will be modified)
    @param      begin           first vertex to use
    @return                     path
    """
    path = [(begin, None)]
    stay = True
    while stay and len(edges_from) > 0:

        n = path[-1][0]
        if n not in edges_from:
            # fin
            break
        le = edges_from[n]

        if len(le) == 1:
            h = 0
            e = le[h]
            to = e[1] if n != e[1] else e[2]
        else:
            to = None
            nb = 100
            while to is None or to == begin:
                h = random.randint(0, len(le) - 1) if len(le) > 1 else 0
                e = le[h]
                to = e[1] if n != e[1] else e[2]
                nb -= 1
                if nb < 0:
                    raise NotImplementedError(
                        "Algorithm issue {0}".format(len(path)))

        if len(edges_from[to]) == 1:
            if begin != to:
                raise NotImplementedError("Wrong algorithm.")
            else:
                stay = False

        keep = _delete_edge(edges_from, n, to)
        path.append((to, keep))

    return path[1:]


def distance_vertices(edges, vertices, distances):
    """
    Computes the length of edges if distances is None.

    @param      edges           list of tuple (vertex A, vertex B)
    @param      vertices        locations of the vertices
    @param      distances       distances (None or list of floats)
    @return                     distances (list of float)
    """
    if distances is None:
        distances = []
    while len(distances) < len(edges):
        distances.append(None)
    for i, edge in enumerate(edges):
        if distances[i] is not None:
            continue
        a, b = edge
        va = vertices[a]
        vb = vertices[b]
        d = haversine_distance(va[0], va[1], vb[0], vb[1])
        distances[i] = d
    return distances


def bellman_distances(edges, distances, fLOG=None):
    """
    Computes shortest distances between all vertices.
    It assumes edges are symmetric.

    @param      edges           list of tuple (vertex A, vertex B)
    @param      distances       distances (list of floats)
    @param      fLOG            logging function
    @return                     dictionary of distances

    This function could be implemented based on
    `shortest_path <https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.shortest_path.html>`_.
    """
    dist = {(a, b): d for d, (a, b) in zip(distances, edges)}
    dist.update({(b, a): d for d, (a, b) in zip(distances, edges)})
    dist0 = dist.copy()

    iter = 0  # pylint: disable=W0622
    up = dist
    while len(up) > 0:
        iter += 1
        up = {}
        for (a, b), d1 in dist.items():
            if (a, b) not in dist0 and (a, b) not in up:
                # no need to continue as no update during the last iteration
                continue
            for (aa, bb), d2 in dist.items():
                # not the most efficient
                if b == aa and a != bb:
                    d = d1 + d2
                    if (a, bb) not in dist or dist[a, bb] > d:
                        up[a, bb] = d
                        up[bb, a] = d
        dist.update(up)
        if fLOG:
            sum_values = sum(dist.values())
            mes = "iteration={0} modif={1} #dist={2} sum_values={3} avg={4}".format(
                iter, len(up), len(dist), sum_values, sum_values / len(dist))
            fLOG("[bellman_distances] " + mes)

    return dist


def dijkstra_path(edges, distances, va, vb):
    """
    Returns the best path between two vertices.
    Uses `Dikjstra <https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm>`_ algorithm.

    @param      edges       list of edges.
    @param      distances   list of distances
    @param      va          first vertex
    @param      vb          last vertex
    @return                 list of edges

    This function could be implemented based on
    `shortest_path <https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.shortest_path.html>`_.
    """
    dist = {va: 0}
    prev = {va: None}
    modif = 1
    while modif > 0:
        modif = 0
        for (a, b), d in zip(edges, distances):
            if a in dist:
                d2 = dist[a] + d
                if b not in dist or dist[b] > d2:
                    dist[b] = d2
                    prev[b] = a
                    modif += 1
            if b in dist:
                d2 = dist[b] + d
                if a not in dist or dist[a] > d2:
                    dist[a] = d2
                    prev[a] = b
                    modif += 1
    rev = {(a, b): i for i, (a, b) in enumerate(edges)}
    rev.update({(b, a): i for i, (a, b) in enumerate(edges)})
    path = []
    v = vb
    while v is not None:
        path.append(v)
        v = prev[v]
    path.reverse()
    return [rev[a, b] for a, b in zip(path[:-1], path[1:])]


def matching_vertices(distances, algo="blossom"):
    """
    Finds the best match between vertices.

    @param      distances       result of function @bellman_distances but
                                only for odd vertices (odd = odd degree),
                                dictionary { (vi,vj) : distance}
    @param      algo            algorithm (see below)
    @return                     sequences of best matches.

    If ``algo=='hungarian'``,
    the function relies on `linear_sum_assignment
    <https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html>`_
    from `scipy <https://docs.scipy.org/doc/scipy-0.18.1/>`_ which uses the
    `Hungarian Algorithm <https://en.wikipedia.org/wiki/Hungarian_algorithm>`_.
    Vertex index do not have to start from zero and be continuous.
    The function will handle that particular case. However, the method
    works for a bi-partite matching and is not suitable here unless
    the algorithm is modified. Not done (yet?).

    If ``algo=='blossom'``, it uses the
    `Blossom algorithm <https://en.wikipedia.org/wiki/Blossom_algorithm>`_
    which is known to be in :math:`O(n^3)` and finds the optimal matching.

    If ``algo=='basic'``, the function sorts the distances
    by increasing order and builds new edges as they come in this list.
    It does not return an optimal solution but is much faster
    when the graph is big.
    """
    if not isinstance(distances, dict):
        raise TypeError(
            "Unexpected type for distances, this should be a dictionary.")
    from numpy import empty
    from scipy.optimize import linear_sum_assignment
    unique = set(_[0] for _ in distances) | set(_[1] for _ in distances)
    mapping = {}
    rev = {}
    for s in unique:
        n = len(mapping)
        mapping[s] = n
        rev[n] = s
    mx = len(mapping)

    # Hungarian algorithm
    if algo == "hungarian":
        cost = empty((mx, mx))
        mx = abs(max(distances.values())) * len(mapping) * 10
        cost[:] = mx
        for (i, j), v in distances.items():
            if i == j:
                raise ValueError(
                    "Unreasonable case: {0} == {1}, v={2}".format(i, j, v))
            cost[mapping[i], mapping[j]] = v

        row_ind, col_ind = linear_sum_assignment(cost)
        pairs = [(rev[i], rev[j]) for i, j in zip(row_ind, col_ind)]
        for a, b in pairs:
            if a == b:
                raise ValueError("Issue with one pair a == b.\n{0}".format(
                    "\n".join(str(_) for _ in pairs)))

        # we remove duplicates
        done = set()
        final = []
        for a, b in pairs:
            if (a, b) not in done:
                final.append((a, b))
                done.add((b, a))
        if len(final) * 2 != len(pairs):
            mes = "final={0}\n{3}={1}\ncost\n{2}".format(
                final, pairs, cost, algo)
            raise ValueError(
                "Did you use the tweak? The matching should be symmetric.\n" + mes)
        return final
    elif algo == "basic":
        # we sort pair by increasing order
        dists = [(v, i, j) for (i, j), v in distances.items()]
        dists.sort()

        # the graph is fully connected so we don't need to check
        # if selecting an edge leads to an impossible solution
        vdone = set()
        pairs = []
        for v, i, j in dists:
            if i not in vdone and j not in vdone:
                pairs.append((i, j))
                vdone.add(i)
                vdone.add(j)
        return pairs

    elif algo == "blossom":
        from .blossom import Vertex, StructureUpToDate, TreeStructureChanged, MaximumDualReached, INF

        vertices = {}
        for v in mapping:
            vertices[v] = Vertex(v)
        for (i, j), v in distances.items():
            f = fractions.Fraction(v)
            vertices[i].add_edge_to(vertices[j], f)

        def update_tree_structures(roots):
            try:
                while True:
                    try:
                        for root in roots:
                            root.alter_tree(roots)
                        raise StructureUpToDate()
                    except TreeStructureChanged:
                        pass
            except StructureUpToDate:
                pass

        def get_max_delta(roots):
            if len(roots) == 0:
                raise MaximumDualReached()
            delta = INF
            for root in roots:
                delta = min(delta, root.get_max_delta())
            assert delta >= 0
            return delta

        roots = set(vertices.values())

        try:
            while True:
                delta = get_max_delta(roots)
                for root in roots:
                    root.adjust_charge(delta)
                update_tree_structures(roots)
        except MaximumDualReached:
            # done
            pass

        M = set()
        for v in vertices.values():
            M.update(e for e in v.edges if e.selected)

        pairs = [e.extremities for e in M]
        return pairs
    else:
        raise NotImplementedError("Not recognized: {0}".format(algo))


def best_euler_path(edges, vertices, distances, edges_index=None, algo="blossom", fLOG=None):
    """
    Computes the final solution for the Eulerian path.

    @param      edges           edges (list of tuple)
    @param      vertices        location of the vertices (not needed if distances are filled)
    @param      distances       distances for each edge (list of distance)
    @param      edges_index     list of indices of edges (if None --> range(len(edges))
    @param      algo            algorithm to use to computes the matching
                                (see @see fn matching_vertices)
    @param      fLOG            logging function
    @return                     list of edges as tuple, list of edges as indices, distance
    """
    if fLOG:
        fLOG("[best_euler_path] distance_vertices #edges={0}".format(
            len(edges)))
    distances = distance_vertices(edges, vertices, distances)
    if fLOG:
        fLOG("[best_euler_path] bellman_distances")
    dist = bellman_distances(edges, distances, fLOG=fLOG)
    if fLOG:
        fLOG("[best_euler_path] degrees and distances between odd vertices")
    degrees = compute_degrees(edges)
    odd = {k: v for k, v in degrees.items() if v % 2 != 0}
    odd_dist = {k: v for k, v in dist.items() if k[0] in odd and k[1] in odd}
    if fLOG:
        fLOG("[best_euler_path] matching #odd={0}, #odd_dist={1}".format(
            len(odd), len(odd_dist)))
    pairs = matching_vertices(odd_dist, algo=algo)
    if fLOG:
        fLOG("[best_euler_path] build solution")
    solution = list(edges)
    for va, vb in pairs:
        dij = dijkstra_path(edges, distances, va, vb)
        solution.extend([edges[e] for e in dij])
    if fLOG:
        fLOG("[best_euler_path] order edges to get the path #edges={0}".format(
            len(solution)))
    if edges_index is None:
        edges_index = list(range(len(edges)))
    mapping = {}
    rev = {}
    for edge, index in zip(edges, edges_index):
        mapping[edge] = index
        rev[index] = edge
    sol_index = [mapping[e] for e in solution]
    euler_index = euler_path(edges_index, edges, sol_index)
    euler = [rev[i] for i in euler_index]
    if fLOG:
        fLOG("[best_euler_path] done.")
    d = distance_solution(edges_index, edges, distances, sol_index)
    return euler, euler_index, d
