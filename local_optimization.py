import json
import networkx as nx
from csv_to_json import create_json
import multiprocessing


def initialize_graph_from_json_file(json_file):
    with open(json_file, 'r') as file:
        json_data = json.load(file)

    graph = nx.DiGraph()

    for node_data in json_data['nodes']:
        graph.add_node(node_data['id'], group=node_data['group'], is_in_path=node_data['is_in_path'])

    for link in json_data['links']:
        reversed_association_rate = link.get('reversed_association_rate', 0.5)
        graph.add_edge(link['source'], link['target'], reversed_association_rate=reversed_association_rate,
                       is_part_of_path=link['is_part_of_path'])

    return graph


def save_graph_to_json(graph, json_file):
    # Nodes data from the graph
    nodes_data = [{'id': node, 'group': graph.nodes[node]['group'], 'is_in_path': graph.nodes[node].get('is_in_path', False)} for node in graph.nodes]

    # Links data from the graph
    links_data = [{'source': source, 'target': target, 'reversed_association_rate': graph[source][target]['reversed_association_rate'], 'is_part_of_path': graph[source][target].get('is_part_of_path', False), 'value': 0.5} for source, target in graph.edges]

    graph_data = {'nodes': nodes_data, 'links': links_data}

    with open(json_file, 'w') as json_file:
        json.dump(graph_data, json_file, indent=2)


def label_propagation(graph, start_node):
    # labels = {node: float('inf') for node in graph.nodes}
    labels = {node: 999999 for node in graph.nodes}
    labels[start_node] = 0

    while True:
        updated = False
        for node in graph.nodes:
            for predecessor in graph.predecessors(node):
                new_label = labels[predecessor] + graph[predecessor][node]['reversed_association_rate']
                if new_label < labels[node]:
                    labels[node] = new_label
                    updated = True

        if not updated:
            break

    labels = {node: round(label, 3) for node, label in labels.items()}

    return labels


def relax(node, labels, graph):
    new_label = 999999  # Initialize to positive infinity
    for predecessor in graph.predecessors(node):
        new_label = min(new_label, labels[predecessor] + graph[predecessor][node]['reversed_association_rate'])
    return new_label


def label_propagation_parallel(graph, start_node):
    labels = {node: 999999 for node in graph.nodes}
    labels[start_node] = 0

    with multiprocessing.Pool() as pool:
        while True:
            # A subset of nodes to process in each iteration
            nodes_to_process = graph.nodes
            results = pool.starmap(relax, [(node, labels, graph) for node in nodes_to_process])

            # Check for stability
            old_labels = labels.copy()

            # Update labels in the main thread
            for node, new_label in zip(nodes_to_process, results):
                labels[node] = min(labels[node], new_label)

            if old_labels == labels:
                break

    labels = {node: round(label, 3) for node, label in labels.items()}
    return labels


def find_path_to_root(graph, labels, node):
    path = [node]
    current_node = node
    path_labels = {node: labels[node]}

    graph.nodes[node]['is_in_path'] = True

    while labels[current_node] > 0:
        predecessors = list(graph.predecessors(current_node))

        if not predecessors:
            break

        best_predecessor = min(predecessors, key=lambda predecessor: labels[predecessor])

        # Set properties for the edges in the path
        graph[best_predecessor][current_node]['is_part_of_path'] = True

        current_node = best_predecessor
        path.append(current_node)
        path_labels[current_node] = labels[current_node]

        # Set properties for the nodes in the path
        graph.nodes[current_node]['is_in_path'] = True

    return path[::-1], path_labels


def save_labels_to_json(labels, output_file):
    labeled_data = {'labels': labels}

    with open(output_file, 'w') as json_file:
        json.dump(labeled_data, json_file, indent=2)


def main():
    create_json()
    json_file = 'static/json/graph_data.json'
    output_file = 'static/json/labeled_nodes.json'
    graph = initialize_graph_from_json_file(json_file)

    selected_node1 = 'work'
    selected_node2 = 'school'
    lca = nx.lowest_common_ancestor(graph, selected_node1, selected_node2)
    print("LCA: ", lca)
    # start_node = 'ROOT'
    start_node = lca

    # labels = label_propagation(graph, start_node)
    labels = label_propagation_parallel(graph, start_node)

    save_labels_to_json(labels, output_file)

    path_to_root1, path_labels1 = find_path_to_root(graph, labels, selected_node1)
    print(f"Shortest path from {selected_node1} to {lca}: {path_to_root1}")
    print(f"Labels along the path: {path_labels1}")

    path_to_root2, path_labels2 = find_path_to_root(graph, labels, selected_node2)
    print(f"Shortest path from {selected_node2} to {lca}: {path_to_root2}")
    print(f"Labels along the path: {path_labels2}")
    print("Node Properties:")
    for node, data in graph.nodes(data=True):
        print(f"{node}: {data}")

    print("Edge Properties:")
    for edge in graph.edges(data=True):
        print(f"{edge}: {data}")

    save_graph_to_json(graph, json_file)


if __name__ == "__main__":
    main()