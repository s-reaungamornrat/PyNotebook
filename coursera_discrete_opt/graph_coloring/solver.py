#!/usr/bin/python
# -*- coding: utf-8 -*-
from graph_algorithm import *
from graph import *

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    #print('Node count %d, edge count %d' % (node_count, edge_count))

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
        
    #### play with graph
    graph = Graph()
    graph.set_edges(edges)
    #graph.print_graph()
    #print('---------------Start graph coloring ------------------')
    num_colors, solution, vertices, color_frequency = graph_coloring(graph.vertices)
    #print('In graph coloring, vertices')
    #print_graph(vertices)
    #print('Vertices ', vertices)
    vertex_colors = [(v.index, v.color) for k, v in vertices.items()]
    #print('Vertex color', [(v.index, v.color) for v in vertices])
    
    #######
    # build a trivial solution
    # every node has its own color

    # prepare the solution in the specified output format
    output_data = str(num_colors) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    return output_data#, vertex_colors, color_frequency


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
        ####
        #output_data, vertex_colors, color_frequency = solve_it(input_data)
        #print('\n\nVertex colors\n', vertex_colors)
        #print('\n\nColors frequence\n', color_frequency)
        #print('\n\n Output\n', output_data)
        ####
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

