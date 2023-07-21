import sys
from queue import PriorityQueue
def Search(starting_city, end_city, all_connections,type,heuristic):
    nodes_total_popped, nodes_total_generated, total_expanded_nodes = 0, 0, 0
    dict_the_path_start_to_end = dict()
    if type == 'uninform':
        visitedNodes_, queue, nodes_total_generated = set(), PriorityQueue(), nodes_total_generated + 1
        queue.put((0, [starting_city]))
        while queue:
            cost, path = queue.get()
            current, nodes_total_popped  = path[len(path) - 1], nodes_total_popped+1
            if current not in visitedNodes_:
                visitedNodes_.add(current)
                if current == end_city:
                    total_expanded_nodes, dict_the_path_start_to_end['cost'],dict_the_path_start_to_end['path']  = total_expanded_nodes+1,cost, path
                    print("Nodes Popped:",nodes_total_popped,'\nNodes Expanded:',int((nodes_total_popped+1)/2),"\nNodes Generated:",  nodes_total_generated ,'\nDistance:', dict_the_path_start_to_end['cost'],'km','\nRoute: ')
                    for i in range(len(dict_the_path_start_to_end['path']) - 1):print(dict_the_path_start_to_end['path'][i]," to ",dict_the_path_start_to_end['path'][i + 1],", ",all_connections[dict_the_path_start_to_end['path'][i]][dict_the_path_start_to_end['path'][i + 1]]," km",sep="")
                    sys.exit()
                for child in all_connections[current]:
                    temp, nodes_total_generated = path[:], nodes_total_generated+1
                    temp.append(child)
                    queue.put((float(cost) + float(all_connections[current][child]), temp))
            else:total_expanded_nodes = total_expanded_nodes + 1
            if queue.empty():
                print("Nodes Popped:", nodes_total_popped,'\nNodes Expanded:',int((nodes_total_popped+1)/2),"\nNodes Generated:", nodes_total_generated,"\nDistance: infinity \nRoute: \nNone")
                sys.exit()
    else:
        openSet, cameFrom, gScore, fScore = [starting_city], {}, {}, {}
        for h in heuristic.keys(): gScore[h], fScore[h] = float('inf'), float('inf')  
        gScore[starting_city], fScore[starting_city]  = 0, heuristic[starting_city]
        while len(openSet) != 0:
            minim, nodes_total_popped  = float('inf'), nodes_total_popped+1
            for node in openSet:
                if minim > fScore[node]:current, minim = node, fScore[node]
            if current == end_city:
                dict_the_path_start_to_end['cost'],dict_the_path_start_to_end['path'] = 0, []
                while current != "":
                    if current == starting_city:
                        total_expanded_nodes+=1
                        dict_the_path_start_to_end['path'].append(starting_city)
                        dict_the_path_start_to_end['path'].reverse()
                        print("Nodes Popped:",nodes_total_popped,'\nNodes Expanded:',int((nodes_total_popped+1)/2),"\nNodes Generated:",  nodes_total_generated + 1,'\nDistance:', dict_the_path_start_to_end['cost'],'km','\nRoute: ')
                        for i in range(len(dict_the_path_start_to_end['path']) - 1):print(dict_the_path_start_to_end['path'][i]," to ",dict_the_path_start_to_end['path'][i + 1],", ",all_connections[dict_the_path_start_to_end['path'][i]][dict_the_path_start_to_end['path'][i + 1]]," km",sep="")
                        sys.exit()
                    dict_the_path_start_to_end['path'].append(current)
                    dict_the_path_start_to_end['cost'] =  dict_the_path_start_to_end['cost'] + all_connections[current][cameFrom[current]]
                    current = cameFrom[current]
            openSet.remove(current)
            for neighbor in all_connections[current].keys():
                nodes_total_generated += 1
                tentative_gScore = gScore[current] + all_connections[current][neighbor]
                if tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor], gScore[neighbor]  = current, tentative_gScore 
                    fScore[neighbor] = gScore[neighbor] + heuristic[neighbor]
                    if neighbor not in openSet:openSet.append(neighbor)
        print("Nodes Popped:", nodes_total_popped,'\nNodes Expanded:',int((nodes_total_popped+1)/2),"\nNodes Generated:", nodes_total_generated,"\nDistance: infinity \nRoute: \nNone")
        sys.exit()
if __name__ == '__main__':
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print('Incorrect number of arguments\n')
        sys.exit()
    all_connections = dict()
    for each in open(sys.argv[1], 'r'):
        if each.rstrip('\n').rstrip('\r') == 'END OF INPUT':break
        else:all_connections.setdefault(each.rstrip('\n').rstrip('\r').split(' ')[0], {})[each.rstrip('\n').rstrip('\r').split(' ')[1]], all_connections.setdefault(each.rstrip('\n').rstrip('\r').split(' ')[1], {})[each.rstrip('\n').rstrip('\r').split(' ')[0]] = float(each.rstrip('\n').rstrip('\r').split(' ')[2]), float(each.rstrip('\n').rstrip('\r').split(' ')[2])
    if sys.argv[2] not in all_connections.keys() or sys.argv[3] not in all_connections.keys():
        print('Start node or ending node is not present')
        sys.exit()
    if len(sys.argv) == 4: Search(sys.argv[2], sys.argv[3], all_connections ,'uninform','')
    elif len(sys.argv) == 5:
        HeuristicsData_ = dict()
        for each in open(sys.argv[4], 'r'):
            if each.rstrip('\n').rstrip('\r') == 'END OF INPUT': break
            else: HeuristicsData_[each.rstrip('\n').rstrip('\r').split(' ')[0]] = float(each.rstrip('\n').rstrip('\r').split(' ')[1])
        Search(sys.argv[2], sys.argv[3], all_connections ,'inform',HeuristicsData_)