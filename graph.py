import pandas as pd

'''
Find a trajectory from A to B from dataframe. Expected is one single route from start to end.
dataset   : dataframe with vertices
start     : startpoint for trajectory to find
end       : endpoint to reach
from_field: for each row the startpoint of avertice
to_filed  : for each row the startpoint of avertice
key_pairs : filter vertices by matchping [key_pairs]. A keypair has the form [key_field, key_value], 
            key_filed is the column name in the dataframe, key_value is the required value in this column

returns the ordered dataframe of vertices to reach the end point from the start point. If no route is
possible, an empty dataframe is returned
throws an Exception when multiple routes are possible
'''
def trajectory_from_to(dataset, start, end, from_field='from', to_field='to', 
                       key_pairs = None):
    # Create dataset to work with
    data = dataset
    if key_pairs and len(key_pairs) > 0:
        for pair in key_pairs:
            data = data[data[pair[0]] == pair[1]]

    # Find startig point
    result = data[data[from_field] == start]
    if len(result) == 0:
        # STart point not found, return empty set
        return result
    if len(result) > 1:
        raise Exception('Multiple routes from point ' + start + 
                           '\nHint: Try filtering with key_pairs')

    # Find next until endpoint reached or no more items to add
    next = result[to_field].iloc[-1]
    #print(next)
    while  next != end:
        to_add = data[data[from_field] == next]
        if len(to_add) > 1:
            raise Exception('Multiple routes from point ' + next + 
                           '\nHint: Try filtering with key_pairs')
        result = result.append(to_add)
        if next == result[to_field].iloc[-1] :
            break
        next = result[to_field].iloc[-1]
        #print(next)

    # Reindex result and return
    if result.iloc[-1][to_field] == end:
        result = result.reset_index()
        return result
    else:
        # If endpoint not reachable, return empty set
        return result.iloc[0:0]
    

'''
Restore trajectory from a dataframe. Expected is one single route from start to end.
dataset   : dataframe with vertices
from_field: for each row the startpoint of avertice
to_filed  : for each row the startpoint of avertice
key_pairs : filter vertices by matchping [key_pairs]. A keypair has the form [key_field, key_value], 
            key_filed is the column name in the dataframe, key_value is the required value in this column

returns the ordered dataframe of vertices describing the trajectory. An exception is raised if the graph 
does not have a single startpoint and a single endpoint
'''
def trajectory_full(dataset, from_field='vertrek', to_field='bestemming', 
                       key_pairs = None):
    
    # Create dataset to work with
    data = dataset
    if key_pairs and len(key_pairs) > 0:
        for pair in key_pairs:
            data = data[data[pair[0]] == pair[1]]

    f = data[from_field]
    t = data[to_field]
    startpoints = f[~f.isin(t)]
    if len(startpoints) != 1:
        raise Exception("Not a single startpoint")
    endpoints = t[~t.isin(f)]
    if len(endpoints) != 1:
        raise Exception("Not a single endpoint")

    return trajectory_from_to(data, startpoints.iloc[0], endpoints.iloc[0],
                              from_field, to_field, key_pairs=None)


'''
Some test examples
''' 
df = pd.DataFrame(columns=['date', 'nr', 'from', 'to', 'data'])
df = df.append({'date': '2019-09-20', 'nr': 231, 'from': 'C', 'to': 'D', 'data': 1}, ignore_index=True)
df = df.append({'date': '2019-09-20', 'nr': 231,  'from': 'B', 'to': 'C', 'data': 2}, ignore_index=True)
df = df.append({'date': '2019-09-20', 'nr': 231,  'from': 'D', 'to': 'E', 'data': 3}, ignore_index=True)
df = df.append({'date': '2019-09-20', 'nr': 231,  'from': 'A', 'to': 'B', 'data': 0}, ignore_index=True)

trajectory_from_to(df,'A', 'D', from_field='from', to_field='to',
               key_pairs=[['date', '2019-09-20'],['nr', 231]])
               
#    index        date   nr from to data
# 0      3  2019-09-20  231    A  B    0
# 1      1  2019-09-20  231    B  C    2
# 2      0  2019-09-20  231    C  D    1

trajectory_full(df, from_field='from', to_field='to',
                 key_pairs=[['date', '2019-09-20'],['nr', 231]])
                 
#    index        date   nr from to data
# 0      3  2019-09-20  231    A  B    0
# 1      1  2019-09-20  231    B  C    2
# 2      0  2019-09-20  231    C  D    1
# 3      2  2019-09-20  231    D  E    3
