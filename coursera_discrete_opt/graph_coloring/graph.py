import copy
import numpy as np

class Node:
    
    def __init__(self, parent = None, color= None, index = -1, degree = -1):
        
        self.color = color
        self.index = index
        self.degree = degree
        self.parent = parent
        self.child_indices = set()
        self.depth = 0
        if parent:
            self.depth = parent.depth+1    
            
    def __repr__(self):
        """Use by calling repr(node)"""
        return "Node(c: " + repr(self.color) + ", idx: " + repr(self.index) + ", deg: " + repr(self.degree) + ")"    
    
    def expand(self, index):
        if index in self.child_indices:
            #print('Index already exists in the children list')
            return False
        else:
            self.child_indices.append(index)
            #print('Node %d: add child index %d' % (self.index, index))
            return True
            
    def set_color(self, color):
        self.color = color
        
    def __lt__(self, other):
        return self.degree > other.degree
    
class Graph:
    
    def __init__(self, edges=None, initial_domain=None, vertices=None, domains=None, degrees=None):
        
        self.edges = edges
        self.initial_domain = initial_domain
        self.assignments = dict()
        
        if not vertices: self.vertices = dict()
        else: self.vertices = vertices
            
        if not domains: self.domains = dict()
        else: self.domains = domains
            
        if not degrees: self.degrees = dict()
        else: self.degrees = degrees        
        
        if edges and not (vertices and domains and degrees):
            #print('Graph: set edges ')
            self.set_edges(self.edges)
            
    def clear_assignments(self):
        self.assignments.clear()
    
    def get_degrees(self):
        
        return  [d for i, d in self.degrees.items()]
    
    def set_initial_domains(self, initial_domain):
        
        self.initial_domain = initial_domain
        
        #print('In set_initial_domains, initial domains ', self.initial_domain)
        for i, v in self.vertices.items():
            self.domains[v.index] = copy.deepcopy(self.initial_domain)
        #print('In set_initial_domains, All domains ', self.domains)

    def add_vertex(self, vertex, child):
        print('\nIn graph.add_vertex, vertex {}, child {}'.format(vertex, child))
        if vertex in self.vertices:
            self.vertices[vertex].degree +=1
            self.vertices[vertex].child_indices.add(child)
            #print('Increase vertex {}, degree {}, children {}'.format(vertex, self.vertices[vertex].degree,\
            #                                                          self.vertices[vertex].child_indices))
        else:
            self.vertices[vertex] = Node(parent = None, color= None, index = vertex, degree = 1)
            self.vertices[vertex].child_indices.add(child)
            #print('Add vertex {}, degree {}, children {}'.format(vertex, self.vertices[vertex].degree,\
            #                                                     self.vertices[vertex].child_indices))
        print('In graph.add_vertex, vertex  node {}, \nchildren {}'.format(self.vertices[vertex] , self.vertices[vertex].child_indices))
        
    def set_edges(self, edges):

        for edge in edges:
            self.add_vertex(edge[0], edge[1])
            self.add_vertex(edge[1], edge[0])
            if edge[0] not in self.domains:
                self.domains[edge[0]] = self.initial_domain
            if edge[1] not in self.domains:
                self.domains[edge[1]] = self.initial_domain            

        for i, vertex in self.vertices.items():
            #print(vertex)
            self.degrees[vertex.index] = vertex.degree
            
    def get_sorted_by_degrees(self):
        
        variables, vertex_degs = list(), list()
        for i, d in self.degrees.items():
            variables.append(i)
            vertex_degs.append(d)
        
        variables = np.asarray(variables)
        vertex_degs = np.asarray(vertex_degs)
        indices = np.argsort(vertex_degs)[::-1]
        #print('Indices {}, vertex degrees {}'.format(variables[indices], vertex_degs[indices]))
        return variables
    
            
    def get_high_degree_var(self):
        
        var, deg = None, 0
        for i, d in self.degrees.items():
            if i in self.assignments:
                continue
            if d > deg: 
                deg = d
                var = i
        #print('In get_high_degree_var, var {} deg {}'.format(var, deg))
        return var
    
    def get_small_domain_var(self, cdomains=None, deg_break_ties=True):
        
        #print('\n------------In graph.get_small_domain_var, copied domains are ', cdomains)
        
        idj = None
        
        if cdomains == None:
            cdomains = self.domains
 
        dsizes = np.asarray([len(d) for i, d in cdomains.items() if i not in self.assignments])
        vindices = np.asarray([i for i, d in cdomains.items() if i not in self.assignments])
        
        if len(vindices) == 1:
            return vindices[0]
            
        sorted_args = np.argsort(dsizes)
        sorted_dsizes = dsizes[sorted_args]
        sorted_vindices = vindices[sorted_args]
        #print('In get_small_domain_var, sorted sizes ', sorted_dsizes)
        #print('In get_small_domain_var, sorted indices ', sorted_vindices)
        
        for i in range(1, len(sorted_vindices)):
            idj, idk = sorted_vindices[i-1], sorted_vindices[i]
            if sorted_dsizes[i-1] == sorted_dsizes[i]:
                if deg_break_ties:
                    if self.degrees[idj] >= self.degrees[idk]: 
                        #print('-------In graph.get_small_domain_var, vertex {} degree {} >= {}'.format(idj, self.degrees[idj], self.degrees[idk]))
                        return idj
                    else:
                        #print('-------In graph.get_small_domain_var, vertex {} degree {} >= {}'.format(idk, self.degrees[idk], self.degrees[idj]))
                        return idk
                else: 
                    #print('------In graph.get_small_domain_var, vertex {} size {} <= {}'.format(idj, sorted_dsizes[i-1], sorted_dsizes[i-1]))
                    return idj
            else:
                return idj
                
        #print('In graph.get_small_domain_var, indices {}, domain size {}'.format(idj, cdomains))
        
        return idj
                            