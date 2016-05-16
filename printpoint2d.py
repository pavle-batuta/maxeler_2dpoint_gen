import argparse
import struct

from itertools import izip

try:
    import numpy as np
except ImportError:
    np = None
try:
    import matplotlib.pyplot as plt
except:
    plt = None

RESOLUTION_PERCENTAGE = {'low':20, 'medium':50, 'high':80, 'full':100}
COLOR_LIST = ['b','g','r','c','m','y']

def arg_parsing():
    description_string = """Input a list of 2d points in the format (x,y,c)
    where c is a cluster number, You can then compare the list with another
    file or plot the points"""
    parser = argparse.ArgumentParser(description=description_string)
    parser.add_argument('input', type=argparse.FileType('r'),
                        help='Input file')
    parser.add_argument('-c', '--compare-to', dest='other', default=None,
                        type=argparse.FileType('r'),
                        help='File to compare')
    parser.add_argument('-p','--plot', action='store_true', dest='do_plot',
                        help='Plot the input file.')
    parser.add_argument('--resolution', choices=['low', 'med', 'high', 'full'],
                        default='full',
                        help=('Choose resolution for rendering points: '
                        'low (render 20%% of points), '
                        'medium (render 50%% of points), '
                        'high (render 80%% of points) or '
                        'full (default): render all points.')
                        )
    return parser.parse_args()

def read_file_chunks(file, chunk_size=8*3):
    """Lazy function (generator) for reading chunks of files. Deafult size is
    8b."""
    while True:
        data = file.read(chunk_size)
        if not data:
            break
        yield data

def compare_files(first, second, more=False):
    total_chunks = 0
    different_chunks = 0
    for chunk1,chunk2 in izip(read_file_chunks(first, chunk_size=8*3),
                              read_file_chunks(second, chunk_size=8*3)):
        if(chunk1 != chunk2):
            # TODO: additional information?
            different_chunks+=1
        total_chunks += 1
    return (total_chunks, different_chunks)

def plot_points_colored(points):
    xs, ys, cs = izip(*read_file_chunks(first, chunk_size=8*3))
    plt.scatter(xs, ys)
    plt.gray()
    

def main():
    args = arg_parsing()
    if (args.other):
        cmp_res = compare_files(first=args.input, second=args.other)
    if (args.do_plot):
        print plt
        if plt:
            plot_points_colored()
        else:
            print ("Cannot plot, missing matplotlib dependency.")

    

if __name__ == '__main__':
    main()
