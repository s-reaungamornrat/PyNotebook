import copy
import numpy as np
from collections import deque

debug = False

def revise(D1, D2):
    
    #print('In Revise, D1 {}, D2 {}'.format(D1, D2))
    def eligible(d1, D2):
        eligible = False
        for d2 in D2: 
            if d1 != d2: 
                eligible = True
                break
        return eligible
                
    change = False
    revised_D1 = []
    for d1 in D1:
        if not eligible(d1, D2): 
            #print('In Revise, D1 {}, D2 {}, remove d1 {}'.format(D1,D2,d1))
            change = True
        else:
            revised_D1.append(d1)
            
    if change and debug: print('In Revise, Return changed D1 {}'.format(revised_D1))
    return change, revised_D1

def full_arc_consistency(edges, curr_domains, prev_domains):
    '''
        domains = {v1:D1, v2:D2,...}
    '''
    ldomains = copy.deepcopy(curr_domains)
    
    #print('In FAC, domains ', ldomains)
    arc_que = deque()
    for edge in edges:
        arc_que.append(edge)
        arc_que.append((edge[1], edge[0]))
    #print('In FAC, arc_que ', arc_que)

    while arc_que:
        arc = arc_que.popleft()
        #print('arc ', arc)
        change, d = revise(ldomains[arc[0]], ldomains[arc[1]])
        if change:
            if len(d) == 0:
                if debug: print('In FAC, Full arc consistency is violated, returned reversed domains ', prev_domains)
                return False, prev_domains
            
            ldomains[arc[0]] = d
            recheck_arc = [edge for edge in edges if edge[1]==arc[0] and edge[0] != arc[1] and edge[0] != arc[0]]+\
                        [(edge[1], edge[0]) for edge in edges if edge[0]==arc[0] and edge[1] != arc[1] and edge[1] != arc[0]]
            arc_que.extend(recheck_arc)
            
    return True, ldomains # arg pass by reference so value of global domain changed automatically 
    
def select_value(domain):
    d = copy.deepcopy(domain)
    if len(d) == 1:
        value = domain[0]
        return value, []
    elif len(d) >1: 
        value = domain[0]
        d.remove(value)
        return value, d
    else:
        return None, None
    
def directed_arc_consistency(vertices, v1, c1, v2, c2):
    """
        v1->v1
    """
    if v2 in vertices[v1].child_indices:
        if c1 == c2:
            return False
    return True
    
def select_value_forward_checking(i, domains, vertices):
    
    ldomains = {k:copy.deepcopy(v) for k, v in domains.items()}
    if debug: print('\n\nIn select_value_forward_checking, Copied domains ', ldomains)
    domain = ldomains[i]
    if debug: print('In select_value_forward_checking, Vertex {}, Domain {}'.format(i, domain))
    while domain:
        #print('Domains ', ldomains)
        a_i,domain = select_value(domain)
        if domain == None:
            raise ValueError('In select_value_forward_checking, select_value return None')
        else:
            domain = domain
            #print('-----Domain i ', domain)
        #print('Domains ', ldomains)
        if debug: print('In select_value_forward_checking, Selected value ', a_i)
        invalid_assignment = False
        #print('In select_value_forward_checking, vertices[i].child_indices ', vertices[i].child_indices)
        for k in vertices[i].child_indices: 
            if debug: print('-----In select_value_forward_checking, Domain {} of cidx {} in {}'.format(ldomains[k], k, vertices[i].child_indices))
            for a_k in ldomains[k]:
                #print('\n------In select_value_forward_checking, value {} in domain {} of vertex {}'.format(a_k, ldomains[k], k))
                if debug: print('\n------In select_value_forward_checking, between {} and {} : directed_arc_consistency ({},{}) is {}'.format(i, k ,a_i, a_k, directed_arc_consistency(vertices, i, a_i, k, a_k)))
                if not directed_arc_consistency(vertices, i, a_i, k, a_k):
                    ldomains[k].remove(a_k)
                    if debug: print('------In select_value_forward_checking, remove value {} so not exist in domain {}'.format(a_k, ldomains[k]))
            if len(ldomains[k]) == 0:
                invalid_assignment = True
                #print('In select_value_forward_checking, invalid assignment')
                break
        if invalid_assignment:
            for k in vertices[i].child_indices: 
                #print('In select_value_forward_checking, for vertex {}, reverse domains {} to previous domains{}'.format(k, ldomains[k] ,copy.deepcopy(domains[k]) ))
                ldomains[k] = copy.deepcopy(domains[k])
        else:
            #print('In select_value_forward_checking, returned domain {} with color {}'.format(ldomains, a_i))
            ldomains[i] = [a_i]
            return ldomains, a_i
        
        #print('In select_value_forward_checking, return old domains ', ldomains)
        
    return ldomains, None
  
def is_all_assigned(assignments, vertices, variables):
    
    if len(variables) == len(vertices):
        for v in variables:
            if assignments[v] == None:
                return False
            child_colors = [assignments[cidx] for cidx in vertices[v].child_indices]
            if assignments[v] in child_colors:
                return False
        return True
        # check wherther assignments are similar
        #colors = [c for i, c in graph.assignments.items()]
        #if len(colors) != len(set(colors)):
        #    raise ValueError('Similar colors detected')
        #else:
        #    return True
        
    return False
def reverse_domain(prev_domains, curr_domains, var, vertices):
    
    c = None
    if len(curr_domains[var]) > 0: c = curr_domains[var][0]
        
    if debug: print('In reverse_domain, var {} assigned color {} '.format(var, c))
    idomain = copy.deepcopy(prev_domains[var])
    #print('In reverse_domain, Previous i domain ', idomain)
    if c != None:
        idomain.remove(c)
        if debug: print('In reverse_domain, Remove c {} from i domain {}'.format(c, idomain))
    curr_domains[var] = idomain    
    #print('In reverse_domain, var {} vertices {}'.format(var, vertices))
    for cv in vertices[var].child_indices:
        curr_domains[cv] = copy.deepcopy(prev_domains[cv])
    if debug: print('In reverse_domain, Result domain {}'.format(curr_domains))
    return curr_domains
        
def dynamic_variable_forward_checking(graph):
    
    if debug:
        print('In dynamic_variable_forward_checking, vertices ', graph.vertices)
        print('In dynamic_variable_forward_checking, assignments ', graph.assignments)        
        print('In dynamic_variable_forward_checking, degrees ', graph.degrees)
        print('In dynamic_variable_forward_checking, domains ', graph.domains)    
      
    #print('\n-------In dynamic_variable_forward_checking, assignemnets {}, length assignments {}, length vertices {}'.\
    #      format(graph.assignments, len(graph.assignments), len(graph.vertices)))
    
    if len(graph.assignments) == len(graph.vertices):
        return graph.assignments
    
    ldomains = copy.deepcopy(graph.domains)
    #v = smallest_domain_variable(graph, ldomains)
    ldomains_times = [copy.deepcopy(ldomains)]
    
    variables = [graph.get_high_degree_var()]
    #print('In dynamic_variable_forward_checking, variables ', variables)
    
    flag, ldomains = full_arc_consistency(graph.edges, ldomains, ldomains)
    if debug: print('In dynamic_variable_forward_checking, FAC is {} returned domain {}'.format(flag, ldomains))
    if not flag: return None
    
    i, num_vars = 0, len(graph.vertices)
    
    while i >= 0 and i < num_vars:
        
        #print('i {} , len domains {}'.format(i, len(ldomains_times)))
        ldomains = ldomains_times[i]
        
        #print('\nIn dynamic_variable_forward_checking, i {}, numvars {}'.format(i, num_vars))
        var = variables[i]
        if debug: print('In dynamic_variable_forward_checking, start number {} with var {} in variables {}'.format(i, var, variables))
        
        if i == 0 and len(ldomains[var]) == 0:
            if debug: print('In dynamic_variable_forward_checking, empty start node var {}'.format(var))
            return None
        
        #if var in graph.assignments:
            #print('In dynamic_variable_forward_checking, Varible {} has already been assigned value {}'.format(var, graph.assignments[var]))
            #raise ValueError('Varible {} has already been assigned value {}'.format(var, graph.assignments[var]))
            
        if debug: print('In dynamic_variable_forward_checking, {} call select_value_forward_checking with vertex {}'.format(i, var))
        domains, c = select_value_forward_checking(var, ldomains, graph.vertices)
        if debug: print('In dynamic_variable_forward_checking, select_value_forward_checking returns color {} & domains {}'.format(c,domains))        
        flag, domains = full_arc_consistency(graph.edges, domains, ldomains)
        if debug: print('In dynamic_variable_forward_checking, Full arc consistency is {} returned domain {}'.format(flag, domains))
        if c == None or not flag:
            domains = reverse_domain(ldomains, domains, var, graph.vertices)
            flag, ldomains = full_arc_consistency(graph.edges, domains, ldomains)
            if debug and not flag:
                print('In dynamic_variable_forward_checking, domain inconsistence {} after reverse domain fixed to {}'.format(domains, ldomains))
            ldomains_times[i] = ldomains
            #i-=1
            if len(ldomains[var]) == 0:
                if debug: print('Assignments to be back track ', graph.assignments)
                for k in range(i, len(variables)):
                    if variables[k] in graph.assignments: 
                        del graph.assignments[variables[k]]
                if debug: print('Assignments ready for back track ', graph.assignments)
                i -= 1
                if debug: print('In dynamic_variable_forward_checking, {} backtrack to {}'.format(i+1, i))  
            elif debug:
                print('In dynamic_variable_forward_checking, {} check next color {} branch'.format(i, ldomains[var])) 
                
            if debug: print('\n------------------------at i {}, domain is {}'.format(i, ldomains_times[i]))
            #print('All domains {}'.format(ldomains_times))

        else:
            ldomains = domains
            #if var in graph.assignments:
                #raise ValueError('Vertex %d has already been assigned value' % var)
            graph.assignments[var] = c
            if debug: 
                print('In dynamic_variable_forward_checking, assign color {} to vertex {}'.format(c, var))
                print('In dynamic_variable_forward_checking, assignments {}'.format(graph.assignments))
            
            if is_all_assigned(graph.assignments, graph.vertices, variables):
                flag, ldomains = full_arc_consistency(graph.edges, ldomains, ldomains)
                if not flag:
                    print('\n\nIn dynamic_variable_forward_checking, Complete assignment is not consistence')
                    return False
                else:
                    return graph.assignments
                
            # remove this selected value from the stored domian of var 
            if i >= 0:
                ldomains_times[i][var].remove(c)
                if debug: print('In dynamic_variable_forward_checking, var {} domain after assignment {}'.format(var, ldomains_times[i][var]))
            if i < num_vars:
                i+=1
                v = graph.get_small_domain_var(ldomains)
                if i < len(ldomains_times):
                    if debug: print('i {} replace existing domain {} by {}'.format(i, ldomains_times[i], ldomains))
                    ldomains_times[i] = copy.deepcopy(ldomains)
                    variables[i] = v
                else:
                    if debug: print('i {} add domain {}'.format(i, ldomains))
                    ldomains_times.append(copy.deepcopy(ldomains))
                    variables.append(v)
                
                if debug:
                    print('Local domains ', ldomains_times)
                    print('In dynamic_variable_forward_checking, next var {} with the smallest domain'.format(v))
                
    if i <= 0:
        return None
    else:
        return graph.assignments
        
            