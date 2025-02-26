# ##################################################
# 1) Load workpiece graph and feature graph data from  json file
# ##################################################

# Note: Available files are: workpiece_graph.json, feature_graph.json

import json
import networkx as nx
import matplotlib.pyplot as plt

with open('workpiece_graph.json', 'r') as f:
    workpiece_graph = json.load(f)

with open('feature_graph.json', 'r') as f:
    feature_graph = json.load(f)

# test push

# ##################################################
# 2) Create graphs from loaded data
# ##################################################

# Hint: The library networkx helps you to create a graph. You can use the nx.Graph() class to create a graph.
# Note: Other appraoches are also possible.

# Load the data from the json file and create a graph

"""def create_graph(Graph, file):
    graph = nx.Graph()
    graph.add_nodes_from(file['nodes'])
    graph.add_edges_from(file['edges'])
    return graph"""

G = nx.Graph()
G.add_nodes_from(workpiece_graph['nodes'])
G.add_edges_from(workpiece_graph['edges'])

H = nx.Graph()
H.add_nodes_from(feature_graph['nodes'])
H.add_edges_from(feature_graph['edges'])

# Note: Optional task - Visualize the graph

# Plotting function to visualize the workpiece and feature graphs side by side

def visualize_graph(G1, G2):
    plt.figure( figsize=(12, 6))
    plt.subplot(121)
    pos_workpiece = nx.spring_layout(G)
    nx.draw(G1, pos_workpiece, with_labels=True, node_size = 180)
    plt.title('Workpiece Graph')

    # Plot the feature graph
    plt.subplot(122)
    pos_feature = nx.spring_layout(H)
    nx.draw(G2, pos_feature, with_labels=True, node_color='grey', node_size = 450)
    plt.title('Feature Graph')
    
    plt.show()

# Example code:
# from pyvis.network import Network
# nt = Network()
# nt.from_nx(workpiece_graph)
# nt.show("graph.html", notebook=False)

# ##################################################
# 3) Check if the feature graph is a subgraph of the workpiece workpiece and find any other matching subgraphs
# ##################################################

# check if the feature graph is a subgraph of the workpiece graph

def is_subgraph(G, H):
    # check if nodes of H are in G
    node_check = all(node in G.nodes for node in H.nodes)
    # check if edges of H are in G
    edge_check = all(edge in G.edges for edge in H.edges)
    return node_check and edge_check

print("Is the feature graph a subgraph of the workpiece graph?", is_subgraph(G, H))

# find all matching subgraphs

from networkx.algorithms import isomorphism

GM = isomorphism.GraphMatcher(G, H)

def node_match(n1, n2):
    return n1['type'] == n2['type'] # matching nodes based on their type
def edge_match(e1, e2):
    return e1['angular_type'] == e2['angular_type'] # matching edges based on their angular type

GM = isomorphism.GraphMatcher(G, H, node_match=node_match, edge_match=edge_match)
matches = [match for match in GM.subgraph_isomorphisms_iter()]

# ##################################################
# 4) Results
# ##################################################

# Print results if matches are found. Return the number of matches and the node ids.

# The feature_graph in the 3D model is a hole
# finding all the matching subgraphs in the workpiece_graph

for i, match in enumerate(matches, start=1):
    print(f"Match {i}: {match}")

# Visualize workpiece_graph and feature_graph after console output

visualize_graph(G, H)