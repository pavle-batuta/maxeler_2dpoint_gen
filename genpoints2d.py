import argparse
import math
import random
import struct

from itertools import izip

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

# The origin point, x = y = 0.
ORIGIN = (0.0,0.0,0.0)

# Level of diffusion around a cluster centroid.
DIFFUSION = 100

DEFAULT_MAX_X_COORDINATE = 1000
DEFAULT_MAX_Y_COORDINATE = 1000
# Default centroid values:
DEFAULT_CENTROID_LIST = [(800.0,800.0,3.0), (800.0,400.0,2.0),
                         (400.0,800.0,1.0), (400.0,400.0,0.0)]
DEFAULT_CLUSTER_NO = len(DEFAULT_CENTROID_LIST)

DEFAULT_OUTPUT_FILE = 'test.dat'

USE_DEFAULT_CENTROIDS = False


def dist2d(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def gen_point2d(diffusion, max_x, max_y, z_payload=0.0):
    """Generate a single centroid. A centroid may not be too close to the
    maximum value of the dimension, no closer than 2*diffusion"""
    return (random.uniform(2*diffusion, max_x-2*diffusion),
            random.uniform(2*diffusion, max_y-2*diffusion), z_payload)

def gen_point_from_centroid2d(centroid, diffusion):
    """Generate a single (x,y,0.0) point centered around a centroid. """
    # TODO: refactor
    x =  random.uniform(centroid[0] - diffusion, centroid[0] + diffusion)
    y =  random.uniform(centroid[1] - diffusion, centroid[1] + diffusion)
    z_payload = centroid[2]  # Get the Z payload from the centroid.
    return (x,y,z_payload)

def centroidgen2d(clusters, diffusion, max_x, max_y):
    """Generate centroids for each cluster. Each centroid must be at least
    2*diffusion away from all others."""
    # TODO: this is a brute force solution, may need to optimize.
    centroids = []
    for _ in xrange(clusters):
        centroid = gen_point2d(diffusion, max_x, max_y)
        for other_centroid in centroids:
            while (dist2d(centroid, other_centroid) < 2 * diffusion):
                centroid = gen_point2d(diffusion, max_x, max_y,
                                       z_payload=float(i))
        centroids.append(centroid)
    return centroids

def pointgen2d(num, diffusion, clusters, max_x, max_y, std_pattern=False):
    """Generate a vector list of random (x,y,0) points. The values x and y are
    bounded by max_x and max_y values. If the number of clusters is > 0 then
    the values will be clustered into that many random groups with the
    specified level of diffusion."""

    if std_pattern:
        centroids = DEFAULT_CENTROID_LIST
    else:
        centroids = centroidgen2d(clusters, diffusion, max_x, max_y)

    if (len(centroids) > 0):
        points = [gen_point_from_centroid2d(
                  centroids[i%len(centroids)], diffusion) 
                  for i in xrange(num)]
    else:
        points = [gen_point2d(diffusion, max_x, max_y) for i in xrange(num)]
    return (points, centroids)

def plot_points(points):
    xs, ys, zs = izip(*points)
    plt.scatter(xs, ys)
    plt.show()

def check_neg(v):
    lv = int(v)
    if (lv < 0):
        raise argparse.ArgumentTypeError("%s is an invalid positive integer"
                                         % v)
    return lv

def arg_parsing():
    description_string = """Generate a 2d list of points that can be spread
                            into clusters. Points are stored as double
                            precision values in (x,y,cl) format, where cl is
                            the assigned cluser number or zero."""
    parser = argparse.ArgumentParser(description=description_string)
    parser.add_argument('num_points', metavar='N', type=check_neg,
                       help='Number of 2d points to be generated.')
    parser.add_argument('--clusters','-c', action='store', dest='num_clusters',
                        type=check_neg, default=0, metavar='K',
                        help='Number of clusters to create.')
    parser.add_argument('--std-pattern', action='store_true',
                        dest='std_pattern',
                        help="""Use a standard pattern of 4 clusters. May not
                        be used with -c.""")
    parser.add_argument('--plot', '-p', action='store_true', dest='do_plot',
                        help='Plot the values upon generating.')
    parser.add_argument('-o', dest='output_file', action='store',
                        default=DEFAULT_OUTPUT_FILE,
                        help='Output file name.')
    parser.add_argument('--diffusion','-D', action='store', dest='diffusion',
                        type=check_neg, default=DIFFUSION,
                        help='Maximum dispersal from centroid center.')
    parser.add_argument('--max', action='store', dest='max_coords', nargs=2,
                        type=check_neg,
                        default=[DEFAULT_MAX_X_COORDINATE,
                                 DEFAULT_MAX_Y_COORDINATE],
                        help='Max values for X and Y axis')
    args = parser.parse_args()
    if (args.std_pattern and args.num_clusters):
        raise ValueError("""You may not specify the number of clusters for
                         standard patterns""")
    return args

def main():
    args = arg_parsing()
    points, centroids = pointgen2d(num=args.num_points,
                                   clusters=args.num_clusters,
                                   diffusion=args.diffusion,
                                   std_pattern=args.std_pattern,
                                   max_x=args.max_coords[0],
                                   max_y=args.max_coords[1])
    if (plt and args.do_plot):
        plot_points(points)
    out_file = open(args.output_file, 'wb')
    for point in points:
        out_file.write(struct.pack('d'*len(point), *point))
    out_file.close()

if __name__ == '__main__':
    main()
