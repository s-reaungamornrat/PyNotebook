import os
import sys
import csv
from graph_algorithm import *
from graph import *

def read_edges(filename):

  with open(filename, 'r') as input_data_file:
      input_data = input_data_file.read()

  lines = input_data.split('\n')
  first_line = lines[0].split()
  node_cnt = int(first_line[0])
  edge_cnt = int(first_line[1])
  #print('Node counts {}, edge count {}'.format(node_count, edge_count))
      
  edges = []
  for i in range(1, len(lines)):
      vertices = lines[i].split()
      #print(vertices)
      if len(vertices): edges.append((int(vertices[0]), int(vertices[1])))
  
  for e in edges:
      print('{} {}'.format(e[0], e[1]))
      
  return node_cnt, edge_cnt, edges

def write_assignments(filename, infile, assignments):

  colors = [ c for i, c in assignments.items()]
  num_colors = len(set(colors))
  
  print('{} : num_colors {} \n{}'.format(infile, num_colors, colors))
  with open(filename, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([infile, 'num_colors'])
    writer.writerow(colors)
    
        
def check_consistence_constraint(graph, assignments):
    
    for idx, color in assignments.items():
        child_colors = [assignments[cidx] for cidx in graph.vertices[idx].child_indices]
        #print('\nIn check_consistence_constraint')
        print('Vertex {} assigned color {} connected vertices {} with corresponding colors {}'.format(idx, color, graph.vertices[idx].child_indices, child_colors))
        if color in child_colors:
            raise ValueError('Error : Arc consistence is violated')
    return True
    
if __name__ == '__main__':
  
  data_folder = './data'
  num_node = 50
  affix = 3
  
  filename = os.path.join(data_folder, ''.join(['gc_', str(num_node), '_', str(affix)]))
  
  node_cnt, edge_cnt, edges = read_edges(filename)
  #print('\nEdges ', edges)
    
  graph = Graph(edges)
  degrees = graph.get_degrees()
  
  initial_domain = list(range(max(degrees)))
  print('\nFilename {}_{}: initial domain{}'.format(num_node, affix, initial_domain))
  graph.set_initial_domains(initial_domain)
  assignments = dynamic_variable_forward_checking(graph)
  satisfied = check_consistence_constraint(graph, assignments)
  if not satisfied:
      print('No Solution Found')
  assignment_list = []
  for i, v in graph.vertices.items():
      assignment_list.append(assignments[v.index])
  num_colors = len(set(assignment_list))
  
  print('\n\nNumber of colors {} \nAssignments {}'.format(num_colors, assignment_list))
    
