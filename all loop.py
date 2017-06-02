# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 12:58:50 2017

@author: Pranit
"""

import queue
rows = 'ABCDEFGHI'
cols = '123456789'
pos_val = '123456789'
sudokus_start = []
sudokus_finish = []
count_failed = []
counter = 0
with open('sudokus_start.txt','r') as f:
    for row in f:
        sudokus_start.append(row.rstrip())
f.close()

with open('sudokus_finish.txt','r') as f:
    for row in f:
        sudokus_finish.append(row.rstrip())
f.close()

for examples in range(0,len(sudokus_start)):    
    row_key = []
    col_key = []
    unit_key = []
    keys = [i+j for i in rows for j in cols ]
    init_values = sudokus_start[examples]
    sudoku = dict(zip(keys,init_values))
    def unit(a,b):
        u = []
        for i in a:
            for j in b:
                u.append(i+j)
        return u
    def show_grid(Sudoku):
        for i in rows:
            for j in cols:
                print (Sudoku[i+j],'   ',)
            print ('\n')
    for i in rows:
        row_key.append([i+j  for j in cols])
    for j in cols:
        col_key.append([i+j for i in rows])
    unit_key = [unit(i,j) for i in ['ABC','DEF','GHI'] for j in ['123','456','789']]
   
    units = dict((s, [u for u in (row_key + col_key + unit_key) if s in u]) for s in sudoku)
    neighbors = dict((s, set(sum(units[s],[]))-set([s])) for s in sudoku)
       
    def AC3(sudok,vals):
        sud = dict(sudok)
        values = dict(vals)
        arc_queue = queue.Queue() 
        visited = set()
        for s,d in sud.items():
            if (d!='0'):
                visited.add(s)
                values[s] = d
                for peer in neighbors[s]:
                    tmp = values[peer]
                    new_val = tmp.replace(d,"")
                    if (len(new_val)==1):
                        if peer not in visited:                    
                            arc_queue.put(peer)
                    values[peer] = new_val
        while not arc_queue.empty():
                node_key = arc_queue.get()
                visited.add(node_key)
                d = values[node_key]
                for peer in neighbors[node_key]:
                    tmp = values[peer]
                    new_val = tmp.replace(d,"")
                    if (len(new_val)==1):
                        if peer not in visited:                    
                            arc_queue.put(peer)
                    values[peer] = new_val
    
        return values
    def legal(sol):
        flag = 1
        for s,d in sol.items():
            if len(d)==0:
                flag = 0
                break
        return flag
    def is_solved(updated):
        solution = dict(sudoku)
        unassigned=[]
        for s,d in updated.items():
            if len(d)>1:
                unassigned.append(s)
                solution[s] = '0'
            else:
                solution[s] = d                
    
        return (solution,unassigned)
    def backtrack(Sol_domain,solved):
        while not solved:
            if Sol_domain.qsize() == 0:
                break
            pos_sol = dict(Sol_domain.get())
            my_sol,unassigned = is_solved(pos_sol)
            if(len(unassigned)==0):
                solved = 1  
                break
            else:
                h = []
                for i in unassigned:
                    h.append(len(pos_sol[i]))
                choice = h.index(min(h))
                current_key = unassigned[choice]
                values_pos = pos_sol[current_key]
                for val in values_pos:
                    tmp_sol = dict(pos_sol)
                    tmp_sol[current_key] = val
                    tmp_sol_ac3 = AC3(my_sol,tmp_sol)
                    if legal(tmp_sol_ac3):
                        Sol_domain.put(tmp_sol_ac3)
    
        with open('output.txt','w+') as f:
            f.write(''.join([my_sol[key] for key in keys]))
        f.close()
        return
    par_sol = dict((s,pos_val) for s in sudoku)
    update = AC3(sudoku,par_sol)
    Sol_domain = queue.LifoQueue()
    Sol_domain.put(update)
    bt = 1
    solved = 0
    backtrack(Sol_domain,solved)
    with open('output.txt','r') as f:
        for row in f:
            if row == sudokus_finish[examples]:
                print ('1')
                counter = counter + 1
            else:
                print ('0')
                count_failed.append(examples)
    f.close()
