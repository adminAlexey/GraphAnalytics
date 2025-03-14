import os
import json
from flask import Flask, request, jsonify
import pandas as pd
import networkx as nx
from pyvis.network import Network
import pyvis
import math
import graphviz

# Путь к директории pyvis
pyvis_path = os.path.dirname(pyvis.__file__)
template_folder_path = os.path.join(pyvis_path, 'templates')

with open('templates/template.html', 'r') as file:
    new_content_graph = file.read()

with open('templates/mini_template.html', 'r') as file:
    new_content_mini_graph = file.read()

with open(template_folder_path + '/template_graph_analytics.html', 'w') as file:
    file.write(new_content_graph)

with open(template_folder_path + '/template_mini_graph_analytics.html', 'w') as file:
    file.write(new_content_mini_graph)

# Конфигурация Flask
app = Flask(__name__)
SECURE_TOKEN = 'super secret'
 
print('back is run')
 
class Creator:
    def __init__(self):
        self.check_50_graphs = False
        self.df = pd.DataFrame()
        self.sender_column = 0
        self.flag_sender = 1
        self.receiver_column = 2
        self.flag_receiver = 3
        self.edge_column = 4
        self.map_colors = {
            'Отправитель': '#00FF00',
            'Получатель': '#00FF00'
        }
        self.options = """
            const options = {
            "nodes": {
                "borderWidth": null,
                "borderWidthSelected": 30,
                "opacity": null,
                "font": {
                "size": 80,
                "strokeWidth": 20
                },
                "scaling": {
                "min": 30,
                "max": 80
                },
                "shadow": {
                "enabled": true
                },
                "size": null
            },
            "edges": {
                "endPointOffset": {
                "to": 15
                },
                "color": {
                "inherit": true
                },
                "font": {
                "size": 50,
                "strokeWidth": 25
                },
                "scaling": {
                "min": 1,
                "max": 10
                },
                "selfReferenceSize": null,
                "selfReference": {
                "angle": 0.7853981633974483
                },
                "shadow": {
                "enabled": true
                },
                "smooth": {
                "forceDirection": "none"
                }
            },
            "manipulation": {
                "enabled": true
            },
            "physics": {
                "enabled" : true,
                "repulsion": {
                "centralGravity": 0.02,
                "springLength": 1000,
                "springConstant": 0.04,
                "nodeDistance": 1000
                },
                "minVelocity": 0.75,
                "solver": "repulsion"
            }
            }
        """

    def df_to_dict(self):
        """Функция создает словарь, где ключи - это отправители, а значения - множества получателей"""
        transfers = {}
        for i in range(len(self.table_nodes)):
            sender = str(self.table_nodes[i][self.sender_column]).title().strip()#.replace('Ё', 'Е').replace('ё', 'е')            # нормализовать ИВАНОВ ИВАН в Иванов Иван
            reciever = str(self.table_nodes[i][self.receiver_column]).title().strip()#.replace('Ё', 'Е').replace('ё', 'е')   # нормализовать ИВАНОВ ИВАН в Иванов Иван
 
            if sender not in transfers:                                                                              # если ключ (отправитель) не в словаре
                transfers[sender] = set()                                                                           # создать множество по ключу
                transfers[sender].add(reciever)                                                             # добавить в множество ноду (получателя)
            else:
                transfers[sender].add(reciever)                                                             # иначе добавить в множество ноду (получателя)
 
            if reciever not in transfers:                                                                           # если ключ (получатель) не в словаре
                transfers[reciever] = set()                                                                        # создать множество по ключу
 
        return transfers
 
    def create_graph(self, graph, id=''):
        g = Network(height='80vh', bgcolor='grey', directed=True, filter_menu=True, select_menu=True, cdn_resources='in_line')
        mini_g = Network(notebook=False, directed=True, bgcolor="gray", cdn_resources='in_line')
        layout = nx.spring_layout(graph)
        # mini_g.from_nx(graph, default_node_size=30)

        edge_color_map = {
            (10000, 100000): 'yellow',
            (100000, 1000000): '#8B0000',
            (1000000, float('inf')): 'black'
        }
        edge_color = 'green'

        for _, row in self.df.iterrows():
            sender = str(row.iloc[self.sender_column]).title()
            receiver = str(row.iloc[self.receiver_column]).title()
            color_sender = str(row.iloc[self.flag_sender])
            color_receiver = str(row.iloc[self.flag_receiver])
            amount = str(row[self.edge_column])
            for node in graph.nodes():
                if str(node).title() == sender:  
                    edge_value = math.ceil(float(amount)/50)
                    for (min_val, max_val), color in edge_color_map.items():
                        if min_val <= edge_value < max_val:
                            edge_color = color
                            break    

                    g.add_node(sender, shape='dot', color=color_sender, label=sender, title=sender, value=170)
                    g.add_node(receiver, shape='dot', color=color_receiver, label=receiver, title=receiver, value=170)
                    g.add_edge(sender, receiver, value=edge_value, label=amount) # , color=edge_color
                    
                    mini_g.add_node(sender, shape='dot', color=color_sender, label=sender, title=sender, value=30)
                    mini_g.add_node(receiver, shape='dot', color=color_receiver, label=receiver, title=receiver, value=30)
                    mini_g.add_edge(sender, receiver, value=edge_value, color=edge_color, label=amount)

        for node in mini_g.nodes:
            node_id = node["id"]
            if node_id in layout:
                node["x"], node["y"] = layout[node_id][0]*10000, layout[node_id][1]*10000
        
        mini_g.toggle_physics(False)   
        # graph_png = graphviz.Digraph(engine='fdp', graph_attr={'size': '5,5', 'dpi': '1000', 'penwidth': '10'})
        # penwidth = '1'
        # if len(graph.nodes()) > 15:
        #     penwidth = '5'
        # if len(graph.nodes()) > 50:
        #     penwidth = '10'

        # for edge in graph.edges():
        #     graph_png.edge(edge[0], edge[1], penwidth=penwidth)

        # graph_png.node_attr.update(penwidth=penwidth)
        # graph_png.render(f'graph{id}', directory='./pngs', format='png', cleanup=True)
        g.set_template_dir(template_folder_path, 'template_graph_analytics.html')
        html = g.generate_html()
        with open(f'graphs/graph{id}.html', "w+", encoding='utf-8') as out:
            out.write(html)

        g.heading = f'graph{id}'

        self.add_legend(f'graphs/graph{id}.html')

        mini_g.set_template_dir(template_folder_path, 'template_mini_graph_analytics.html')
        mini_html = mini_g.generate_html()
        with open(f'mini_graphs/graph{id}.html', "w+", encoding='utf-8') as out:
            out.write(mini_html)

        return g
    
# region create_mini_graph
#     def create_mini_graph(self, nodes, table, id=''):
#         g = Network(height='80vh', bgcolor='grey', directed=True,filter_menu=True, select_menu=True, cdn_resources='in_line')
#         g.set_options(self.options)
#         for e in nodes.edges():
#             for row in range(len(table)):
#                 if e[0] == sender and e[1] == reciever or e[1] == sender and e[0] == reciever:
#                     g.add_node(sender, shape=figure1, label=sender_new, color=color1, title=sender, value=v1)
#                     g.add_node(reciever, shape=figure2, label=reciever_new, color=color2, title=reciever, value=v2)
#                     g.add_edge(sender, reciever, value=str(table[row][4]), label=str(table[row][4]))
 
#         g.write_html(f'graphs/MiniGraphGroup{id}.html')
#         return g
# endregion
 
    def add_legend(self, filename):
        """На граф добавляется легенда (описание основных обозначений)"""       
        with open(filename, 'r+', encoding='utf-8') as old:   # открываем старый файл и новый
            lines = old.readlines()
            text = ''.join(lines)
            nodes_text = 'nodes = new vis.DataSet(['

            for index, (key, value) in enumerate(self.map_colors.items()):
                x = 14000 / len(self.map_colors) * index
                if index % 2 == 0:
                    y = -250
                else:
                    y = 250
                color = value
                name = key
                unicode_name = ''.join(f'\\u{ord(char):04x}' for char in name)
                nodes_text += '{"color": "' + f'{color}", "id": {index}, "label": "{unicode_name}", "shape": "dot", "x": {x}, "y": {y}' + '}'
                if len(self.map_colors) - index > 1:
                    nodes_text += ', '
            nodes_text += ']);'

            legend_text = """
                function drawGraph1() {
                    var container = document.getElementById('legend');
                    """ + nodes_text + """
                    edges = new vis.DataSet([]);
                    nodeColors1 = {};
                    allNodes1 = nodes.get({ returnType: "Object" });
                    for (nodeId in allNodes1) {
                        nodeColors1[nodeId] = allNodes1[nodeId].color;
                    }
                    allEdges = edges.get({ returnType: "Object" });
                    data = {nodes: nodes, edges: edges};
                    var options = {"nodes": {"borderWidth": 0.1, "borderWidthSelected": 30, "opacity": 1, "font": {"size": 80, "strokeWidth": 20}, "scaling": {"min": 30, "max": 80}, "shadow": {"enabled": true}, "size": 150}, "edges": {"endPointOffset": {"to": 15}, "color": {"inherit": true}, "font": {"size": 50, "strokeWidth": 20}, "selfReferenceSize": null, "selfReference": {"angle": 0.7853981633974483}, "shadow": {"enabled": true}, "smooth": {"forceDirection": "none"}}, "manipulation": {"enabled": false}, "physics": {"enabled": "false", "repulsion": {"centralGravity": 0.02, "springLength": 500, "springConstant": 0.04, "nodeDistance": 500}, "minVelocity": 0.75, "solver": "repulsion"}};
                    network = new vis.Network(container, data, options);
                    return network;
                }
                drawGraph1();
                """
            substring = '// This method is responsible for drawing the graph, returns the drawn network'
            index = text.find(substring)
            new_text = text[:index + len(substring)] + legend_text + text[index + len(substring):]
        with open(filename, 'w', encoding='utf-8') as new:
            new.write(new_text)
 
    def build(self):
        self.table_nodes = self.df.values.tolist()
        g = nx.Graph(self.df_to_dict())
        subgraphs = [g.subgraph(c).copy() for c in nx.connected_components(g)]
        subgraphs = sorted(subgraphs, key=lambda x: len(x), reverse=True)
        g = self.create_graph(g, '_общий')
        graphs_json = {}
        graphs_json[f'{g.heading}'] = {'nodes': g.nodes, 'edges': g.edges}
        excel = []
        if len(subgraphs) > 50:
            self.check_50_graphs = True
            subgraphs = subgraphs[:50]
        for id, graph in enumerate(subgraphs[:50], start=1):
            print('graph', id)
            if len(graph.nodes()) > 1000:
                g = self.create_graph(graph, id) #g = self.create_mini_graph(graph, id)
            else:
                g = self.create_graph(graph, id)
 
            graphs_json[f'{g.heading}'] = {'nodes': g.nodes, 'edges': g.edges}
            for node in graph.nodes():
                excel.append([node, id])
        with open('result/graphs.json', 'w', encoding='utf-8') as file:
            json.dump(graphs_json, file, ensure_ascii=False, indent=4)
        pd.DataFrame(excel).to_excel('result/result_groups.xlsx', index=False)

creator = Creator()
 
@app.route('/upload', methods=['POST'])
def upload():
    global creator
    try:
        creator.df = pd.DataFrame(request.json.get('file_df'))
        creator.map_colors = request.json.get('map_colors')
        creator.build()
        if creator.check_50_graphs:
            return jsonify({"message": "File uploaded"}), 201
        else:
            return jsonify({"message": "File uploaded"}), 200
    except Exception as e:
        return jsonify({"message": e}), 500

@app.route('/view', methods=['POST'])
def view():
    if request.json.get('start'):
        list_names = []
        for graph in os.listdir('graphs/'):
            if graph[:len("graph")] == 'graph' and graph[-5:] == '.html':
                list_names.append([graph[:-5]])
        return jsonify({
            "list_names" : list_names
        }), 200    
 
app.run(host='127.0.0.1', port=5000, debug=True)