import pandas as pd
import json


def create_json():
    df = pd.read_csv('data/100most_used_filtered_with_strength_filtered.csv')

    with open('data/100most_used.txt', 'r', encoding='utf-8') as file:
        cues = [line.strip() for line in file]

    # Create (ROOT) and its links
    # root_data = {'source': 'ROOT', 'cue': 'ROOT', 'target': 'ROOT', 'R1': 'ROOT', 'R1.Strength': 2}
    links = [{'source': '', 'cue': 'ROOT', 'target': '', 'R1': cue, 'R1.Strength': 2} for cue in cues]

    # df = pd.concat([df, pd.DataFrame([root_data]), pd.DataFrame(links)])
    df = pd.concat([df, pd.DataFrame(links)])

    f = open("data/100most_used_with_root.csv", "w")
    f.truncate()
    f.close()
    df.to_csv('data/100most_used_with_root.csv', index=False)

    df2 = pd.read_csv('data/100most_used_with_root.csv')

    # List of nodes
    nodes_set = set(df2['cue']) | set(df2['R1'])
    nodes = [{'id': word, 'group': 0, 'is_in_path': False} for word in nodes_set]

    # List of links
    links = [
        {
            'source': row['cue'],
            'target': row['R1'],
            # 'value': row['R1.Strength'] * 50 if row['source'] != 'ROOT' else 0.5,
            'value': 0.5,
            'reversed_association_rate': round(1 / row['R1.Strength'], 3),
            'is_part_of_path': False
        }
        for _, row in df2.iterrows()
    ]

    graph_data = {'nodes': nodes, 'links': links}

    with open('static/json/graph_data.json', 'w') as json_file:
        json.dump(graph_data, json_file, indent=2)


def create_json_test():
    df = pd.read_csv('data/25most_used_filtered_with_strength_filtered.csv')

    with open('data/25most_used.txt', 'r', encoding='utf-8') as file:
        cues = [line.strip() for line in file]

    # root_data = {'source': 'ROOT', 'cue': 'ROOT', 'target': 'ROOT', 'R1': 'ROOT', 'R1.Strength': 2}
    links = [{'source': '', 'cue': 'ROOT', 'target': '', 'R1': cue, 'R1.Strength': 2} for cue in cues]

    # df = pd.concat([df, pd.DataFrame([root_data]), pd.DataFrame(links)])
    df = pd.concat([df, pd.DataFrame(links)])

    f = open("data/25most_used_with_root.csv", "w")
    f.truncate()
    f.close()
    df.to_csv('data/25most_used_with_root.csv', index=False)

    df2 = pd.read_csv('data/25most_used_with_root.csv')
    print(df2.shape)

    nodes_set = set(df2['cue']) | set(df2['R1'])  # Объединение слов из 'cue' и 'R1'
    nodes = [{'id': word, 'group': 0, 'is_in_path': False} for word in nodes_set]

    links = [
        {
            'source': row['cue'],
            'target': row['R1'],
            # 'value': row['R1.Strength'] * 50 if row['source'] != 'ROOT' else 0.5,
            'value': 0.5,
            'reversed_association_rate': round(1 / row['R1.Strength'], 3),
            'is_part_of_path': False
        }
        for _, row in df2.iterrows()
    ]

    graph_data = {'nodes': nodes, 'links': links}

    with open('static/json/graph_data_test.json', 'w') as json_file:
        json.dump(graph_data, json_file, indent=2)


create_json()