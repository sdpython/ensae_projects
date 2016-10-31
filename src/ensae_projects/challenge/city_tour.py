"""
@file
@brief  Function to solve the problem of the
`Route Inspection Problem <https://en.wikipedia.org/wiki/Route_inspection_problem>`_.
"""


class SolutionException(Exception):
    """
    wrong solution
    """
    pass


def distance_solution(edges_index, edges, distances, solution, exc=True):
    """
    Checks if a solution is a solution and returns the distance of it,
    None if it is not a solution. The function does not case about the order.

    @param      edges_index     list if indices of edges (if None --> range(len(edges))
    @param      edges           list of tuple (vertex A, vertex B)
    @param      distance        list of distances of each edge
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
    for k, d in degrees.items():
        if d % 2 == 0:
            even += 1
        else:
            odd += 1

    if odd > 2:
        if exc:
            if len(solution) < 10:
                raise SolutionException(
                    "Are you sure? The path is inconsistent.\n" + str(degrees))
            else:
                raise SolutionException(
                    "Are you sure? The path is inconsistent.")
        else:
            return None
    else:
        return sum(distances[corres[s]] for s in solution)
