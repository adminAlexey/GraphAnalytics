import requests
import streamlit as st
import json
import webbrowser
import os

# добавить интерфейс поиска

BACKEND_URL = "http://127.0.0.1:5000"
print('front is run')

st.set_page_config(page_title="GraphAnalytics", layout="wide")
st.write('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

# Загрузка данных
response = requests.post(f"{BACKEND_URL}/view", json={"start": True})
list_names = json.loads(response.text)['list_names']

with open('result/graphs.json', 'r', encoding='utf-8') as file:
    loaded = json.load(file)

# Функция для получения статистики графа
def get_graph_stats(graph_name):
    graph_data = loaded[graph_name]
    num_nodes = len(graph_data['nodes'])
    num_edges = len(graph_data['edges'])
    try:
        total_weight = sum(float(edge['label']) for edge in graph_data['edges'])
    except:
        total_weight = 0
    return {
        'name': graph_name,
        'num_nodes': num_nodes,
        'num_edges': num_edges,
        'total_weight': total_weight
    }

graph_stats = [get_graph_stats(row[0]) for row in list_names]

col1, col2, col3 = st.columns([1, 2, 1])

# Сбор статистики для всех графов
with col1:
    # Выбор критерия сортировки в сайдбаре
    sort_by = st.selectbox("Сортировать по:", [
        "Количество узлов",
        "Количество рёбер",
        "Сумма переводов"
    ])
with col3:
    # Поле для поиска ноды
    search_node = st.text_input("Поиск ноды по имени:")
    if search_node:
        st.markdown("### Результаты поиска:")
        found = False
        for graph_name, graph_data in loaded.items():
            # Поиск ноды в текущем графе
            matching_nodes = [node for node in graph_data['nodes'] if search_node.lower() in node['title'].lower()]
            if matching_nodes:
                found = True
                st.markdown(f"#### Граф: {graph_name}")
                for node in matching_nodes:
                    st.markdown(f"- **Нода:** {node['title']} (ID: {node['id']})")
                    # Поиск связанных рёбер
                    connected_edges = [
                        edge for edge in graph_data['edges']
                        if edge['from'] == node['id'] or edge['to'] == node['id']
                    ]
                    if connected_edges:
                        st.markdown("  **Связанные рёбра:**")
                        for edge in connected_edges:
                            st.markdown(
                                f"  - От: {edge['from']} → К: {edge['to']} (Вес: {edge['label']})"
                            )
                    else:
                        st.markdown("  **Связанные рёбра:** Нет")
        if not found:
            st.markdown("Нода не найдена.")

# Определение ключа для сортировки
if sort_by == "Количество узлов":
    sort_key = 'num_nodes'
elif sort_by == "Количество рёбер":
    sort_key = 'num_edges'
else:
    sort_key = 'total_weight'

# Сортировка графов
sorted_graphs = sorted(graph_stats, key=lambda x: x[sort_key], reverse=True)
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Отображение отсортированных графов
for graph in sorted_graphs:
    graph_name = graph['name']
    with st.container():
        column1, column2 = st.columns([1, 1])
        with column1:
            st.markdown(f"""
                ### {graph_name}
                Количество нод: {graph['num_nodes']}      
                Количество рёбер: {graph['num_edges']}  
                Сумма переводов: {graph['total_weight']}  
                """, unsafe_allow_html=True)
            if graph_name != 'graph_общий':
                open_button = st.button('Открыть динамический граф', key=graph_name)
                if open_button:
                    webbrowser.open_new_tab(f'{current_dir}\\graphs\\{graph_name}.html')

        with column2:
            # st.image(Image.open(f'pngs/{graph_name}.png'))
            with open(f'{current_dir}\\mini_graphs\\{graph_name}.html', 'r') as file:
                html = file.read()


            st.components.v1.html(html, height=500)

        st.markdown(f'<hr>', unsafe_allow_html=True)