import math
import random

# The origin point, x = y = 0.
ORIGIN = (0.0,0.0,0.0)

MAX_X_COORDINATE = 1000
MAX_Y_COORDINATE = 1000

POINTS_TO_GENERATE = 10000000
# Indicate the number of clusters K. A value of zero or less will trigger a
# uniform distribution.
CLUSTER_NO = 4
# Level of diffusion around a cluster centroid.
DIFFUSION = 100

def dist2d(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def gen_point2d(diffusion, max_x=MAX_X_COORDINATE,
                          max_y=MAX_Y_COORDINATE):
    """Generate a single centroid. A centroid may not be too close to the
    maximum value of the dimension, no closer than 2*diffusion"""
    return (random.uniform(diffusion, max_x-2*diffusion),
            random.uniform(diffusion, max_y-2*diffusion), 0.0)

def gen_point_from_centroid2d(centroid, diffusion):
    """Generate a single (x,y,0.0) point centered around a centroid. """
    # TODO: refactor
    x =  random.uniform(centroid[0] - diffusion, centroid[0] + diffusion)
    y =  random.uniform(centroid[1] - diffusion, centroid[1] + diffusion)
    return (x,y,0.0)

def centroidgen2d(clusters, diffusion,
                  max_x=MAX_X_COORDINATE, max_y=MAX_Y_COORDINATE):
    """Generate centroids for each cluster. Each centroid must be at least
    2*diffusion away from all others."""
    # TODO: this is a brute force solution, may need to optimize.
    centroids = []
    for _ in xrange(clusters):
        centroid = gen_point2d(diffusion)
        for other_centroid in centroids:
            while (dist2d(centroid, other_centroid) < 2 * diffusion):
                centroid = gen_point2d(diffusion)
        centroids.append(centroid)
    return centroids

def pointgen2d(num=POINTS_TO_GENERATE, clusters=CLUSTER_NO,
               max_x=MAX_X_COORDINATE, max_y=MAX_Y_COORDINATE,
               diffusion=DIFFUSION):
    """Generate a vector list of random (x,y,0) points. The values x and y are
    bounded by max_x and max_y values. If the number of clusters is > 0 then
    the values will be clustered into that many random groups with the
    specified level of diffusion."""

    centroids = centroidgen2d(CLUSTER_NO, DIFFUSION)
    if (clusters > 0):
        points = [gen_point_from_centroid2d(centroids[i%clusters], DIFFUSION) 
                  for i in xrange(num)]
    else:
        points = [gen_point2d(DIFFUSION) for i in xrange(num)]
    return (points, centroids)

def main():
    points, centroids = pointgen2d(num=100)
    for ci, centroid in enumerate(centroids):
        print ci, ': ', centroid
        print '---------------------'
        for p in points[ci::CLUSTER_NO]:
            print p
        print '---------------------'

if __name__ == '__main__':
    main()