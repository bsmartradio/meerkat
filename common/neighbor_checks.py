import numpy as np
from shapely.geometry import LinearRing
import matplotlib.pyplot as plt
from numpy.linalg import norm


def ellipse_polyline(ellipses, n=100):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    st = np.sin(t)
    ct = np.cos(t)
    result = []

    for x0, y0, a, b, t in ellipses:
        t = np.deg2rad(t)
        sa = np.sin(t)
        ca = np.cos(t)
        p = np.empty((n, 2))
        p[:, 0] = x0 + a * ca * ct - b * sa * st
        p[:, 1] = y0 + a * sa * ct + b * ca * st
        result.append(p)

    return result


def check_overlap(table, full_table, location, name):
    a = table['a'].data * 0.000277778
    b = table['b'].data * 0.000277778
    lon = table['lon'].data
    lat = table['lat'].data
    pa = table['pa'].data

    for i in range(len(a)):

        for j in range(i + 1, len(a)):
            ellipses = [(lon[i], lat[i], a[i], b[i], pa[i]), (lon[j], lat[j], a[j], b[j], pa[j])]
            a_out, b_out = ellipse_polyline(ellipses)
            x, y = intersections(a_out, b_out)

            if x:
                full_table['overlap'][i] = True
                full_table['overlap'][j] = True
                plt.plot(x, y, "o")
                plt.plot(a_out[:, 0], a_out[:, 1])
                plt.plot(b_out[:, 0], b_out[:, 1])

    plt.savefig(location + name + 'overlapping_edge.png')
    return full_table


def fit_deviation(valuesOne, valuesTwo):
    point_one = np.array([0.0, 0.0])
    point_two = np.array([10.0, 10.0])
    point_three = np.empty([len(valuesOne), 2])
    point_three[:, 0] = valuesOne
    point_three[:, 1] = valuesTwo

    return np.cross(point_two - point_one, point_three - point_one) / norm(point_two - point_one)


def intersections(a, b):
    ea = LinearRing(a)
    eb = LinearRing(b)
    mp = ea.intersection(eb)

    if mp.is_empty:
        return [], []
    elif mp.geom_type == 'Point':
        return [mp.x], [mp.y]
    elif mp.geom_type == 'MultiPoint':
        return [p.x for p in mp], [p.y for p in mp]
    else:
        raise ValueError('something unexpected: ' + mp.geom_type)


def overlap_check(neighbor_vot, center_lon, neighbor_lon):
    # Mark both if it is in the overlap region and if it is marked as too close
    # to the edge
    overlap_index = []
    if max(center_lon) > max(neighbor_lon):
        lon = neighbor_vot['lon'][np.where(neighbor_vot['lon'] > min(center_lon))]
        index = np.where(neighbor_vot['lon'] > min(center_lon))
        lat = neighbor_vot['lat'][np.where(neighbor_vot['lon'] > min(center_lon))]

    else:
        lon = neighbor_vot['lon'][np.where(neighbor_vot['lon'] < max(center_lon))]
        index = np.where(neighbor_vot['lon'] < max(center_lon))
        lat = neighbor_vot['lat'][np.where(neighbor_vot['lon'] < max(center_lon))]

    return np.array([lon, lat]), overlap_index.append(index)


def check_edge_points(data_cubes, phot_tables, lon_range):
    for i in range(3):
        for index, j in enumerate(data_cubes[i].vot_table['lon']):

            if j <= (lon_range[i, 0] + .01):
                phot_tables[i]['edge'][index] = True
            elif j >= (lon_range[i, 1] - .01):
                phot_tables[i]['edge'][index] = True

    return phot_tables
