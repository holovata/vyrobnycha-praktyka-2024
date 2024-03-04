import networkx as nx
from flask import Flask, render_template, request
from local_optimization import find_path_to_root, initialize_graph_from_json_file, label_propagation, save_labels_to_json, save_graph_to_json, label_propagation_parallel
from csv_to_json import create_json

app = Flask(__name__)

'''with open('static/json/graph_data.json', 'r') as f:
    graphData = json.load(f)

with open('static/json/labeled_nodes.json', 'r') as f:
    labelsData = json.load(f)'''


@app.route('/network25', methods=['GET', 'POST'])
def sem_network():
    return render_template('network.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('word_submission.html')


@app.route('/word1', methods=['POST'])
def handle_word1():
    if request.method == 'POST':
        word1 = request.form['word1']
        # Processing to be added...
        return render_template('word_submission.html', word1=word1)


@app.route('/word2', methods=['POST'])
def handle_word2():
    if request.method == 'POST':
        word2 = request.form['word2']
        # Process to be added...
        return render_template('word_submission.html', word2=word2)


@app.route('/path', methods=['GET', 'POST'])
def show_path():
    # if request.method == 'POST':
    app.jinja_env.cache = {}
    create_json()
    graph = initialize_graph_from_json_file('static/json/graph_data.json')

    print("hello")
    word1 = request.args.get('word1', '')
    word2 = request.args.get('word2', '')
    print("Word1:", word1)
    print("Word2:", word2)
    lca = nx.lowest_common_ancestor(graph, word1, word2)
    # lca = find_lca(graph, word1, word2)
    print("LCA: ", lca)
    # labels = label_propagation(graph, 'ROOT')
    # start_node = lca
    # labels = label_propagation(graph, lca)
    labels = label_propagation_parallel(graph, lca)

    path_to_root1, path_labels1 = find_path_to_root(graph, labels, word1)
    print(f"Shortest path from {word1} to {lca}: {path_to_root1}")
    print(f"Labels along the path: {path_labels1}")
    path_to_root2, path_labels2 = find_path_to_root(graph, labels, word2)
    print(f"Shortest path from {word2} to {lca}: {path_to_root2}")
    print(f"Labels along the path: {path_labels2}")

    save_graph_to_json(graph, 'static/json/graph_data.json')
    print("graph saved")

    save_labels_to_json(labels, 'static/json/labeled_nodes.json')
    print("labels saved")

    return render_template('network.html', word1=word1, word2=word2, path1=path_to_root1, path_labels1=path_labels1,
                           path2=path_to_root2, path_labels2=path_labels2)

    # return render_template('network.html')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)