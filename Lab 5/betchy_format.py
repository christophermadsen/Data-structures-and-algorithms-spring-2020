import pandas as pd
import numpy as np
import os

for b in range(1, 3):
    for l in range(1, 4):
        name = 'board'+ str(b) +'_list'+ str(l) +'.txt'
        print('\nTrying to process', name)
        if not os.path.exists(name):
            print("\t No solution file found")
        else:
            with open(name) as f:
                board, layer = [], None
                for line in f:
                    if line[:3] == '###':
                        if layer is not None:
                            board.append(layer)
                        layer = []
                    else:
                        s = line.split()
                        if len(s) > 1:
                            row = []
                            correct = True
                            for e in s:
                                if e == 'GA':
                                    row.append(-1)
                                elif e == '__':
                                    row.append(0)
                                else:
                                    try:
                                        row.append(int(e))
                                    except ValueError:
                                        print("\t Could not parse element:", e)
                                        break
                            layer.append(row) 
                board.append(layer)
            try:
                parsed = np.array(board)
                z, y, x = parsed.shape
                print("\t Found", z, "layers")
                print("\t with dimenions", str(x)+"x"+str(y))
                
                gates = np.where(parsed[0, :, :].T == -1)
                gates = list(zip(gates[0], gates[1]))
                print("\t and", len(gates), "gates")
                print("\t located at", gates)
            except Exception as e:
                print("\t Unmatched board dimensions!")

print("\n\nNOTE: I did NOT check any wirings or the correctness of solutions!\n")        
