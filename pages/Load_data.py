import requests
import pandas as pd
import streamlit as st
import os

# провести код ревью

BACKEND_URL = "http://127.0.0.1:5000"
print('front is run')

st.set_page_config(page_title="GraphAnalytics", layout="wide")
 
def tooltip(message):
    return f"""
    <style>
    .tooltip {{
        position: relative;
        display: inline-block;
        cursor: pointer;
    }}
 
    .tooltip .tooltiptext {{
        visibility: hidden;
        width: 200px;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 5px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%; / Расположение подсказки /
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }}
 
    .tooltip:hover .tooltiptext {{
        visibility: visible;
        opacity: 1;
    }}
    </style>
 
    <div class="tooltip">⚠️
    <span class="tooltiptext">{message}</span>
    </div>
    """

os.makedirs('graphs/', exist_ok=True)
os.makedirs('mini_graphs/', exist_ok=True)
os.makedirs('result/', exist_ok=True)

if 'map_colors' not in st.session_state:
    st.session_state.map_colors = {
        'Отправитель': '#00FF00',
        'Получатель': '#00FF00'
    }
if 'selected_columns' not in st.session_state:
    st.session_state.selected_columns = []
if 'selected_options' not in st.session_state:
    st.session_state.selected_options = []
if 'clear_folders' not in st.session_state:
    st.session_state.clear_folders = True
    # Чистим папки
    for graph in os.listdir('graphs/'):
        try:
            os.remove('graphs/'+graph)
        except Exception as e:
            print('Ошибка удаления', e, graph)
    for png in os.listdir('mini_graphs/'):
        try:
            os.remove('mini_graphs/' + png)
        except Exception as e:
            print('Ошибка удаления', e, png)
    for other in os.listdir('result/'):
        try:
            os.remove('result/' + other)
        except Exception as e:
            print('Ошибка удаления', e, other)

st.title("Построение графа взаимосвязей")
st.divider()
st.markdown("### 1. Выберите файл", unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    uploaded_file = st.file_uploader("Загрузите excel или csv файл", type={"xlsx", 'csv', 'tsv'})
   
def update_selected_columns(column):
    if column in st.session_state.selected_columns:
        st.session_state.selected_columns.remove(column)
    else:
        st.session_state.selected_columns.append(column)
 
df = pd.DataFrame()
if uploaded_file:
    st.markdown("""
        *Выберите столбцы*:
        - Базовый анализ: *ОТПРАВИТЕЛЬ, ПОЛУЧАТЕЛЬ, СУММА*
        - Расширенный анализ (с изменением цвета нод): *ОТПРАВИТЕЛЬ, ФЛАГ_ОТПРАВИТЕЛЯ, ПОЛУЧАТЕЛЬ, ФЛАГ_ПОЛУЧАТЕЛЯ, СУММА*
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("### 2. Работа с данными", unsafe_allow_html=True)
 
    # Определяем тип файла
    file_extension = uploaded_file.name.split('.')[-1].lower()
 
    if file_extension == 'xlsx':
        # Чтение всех листов Excel
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names
        tabs = st.tabs(sheet_names)
 
        @st.cache_data
        def load_excel(file, sheet_name):
            df = pd.read_excel(file, sheet_name=sheet_name).astype(str)
            df.fillna('', inplace=True)
            return df
 
        # Отображение данных для каждого листа
        for i, tab in enumerate(tabs):
            test_df = load_excel(uploaded_file, sheet_names[i])
            with tab:
                st.markdown(f"### {sheet_names[i]}")
                if test_df.empty:
                    st.error('Пустой лист')
                    st.image('gifs/betterttv-meme.gif')
                else:
                    if len(load_excel(uploaded_file, sheet_names[i]).columns) < 3:
                        st.error('Для построения графа необходимо минимум 3 столба')
                    else:
                        st.dataframe(load_excel(uploaded_file, sheet_names[i]))
                        # Отображение чекбоксов по горизонтали
                        st.write("Выберите столбцы:")
                        # Создаем колонки для чекбоксов
                        cols = st.columns(len(load_excel(uploaded_file, sheet_names[i]).columns))  # Создаем столько колонок, сколько столбцов в датафрейме
 
                        for idx, col_name in enumerate(load_excel(uploaded_file, sheet_names[i]).columns):
                            with cols[idx]:

                                st.checkbox(
                                    col_name,
                                    key=f"{sheet_names[i]}_{col_name}",  # Уникальный ключ для каждого чекбокса
                                    value=col_name in st.session_state.selected_columns,
                                    on_change=update_selected_columns,
                                    args=(col_name,)
                                )
                        column1, column2 = st.columns([2, 1])
                        with column1:
                            if set(st.session_state.selected_columns) - set(load_excel(uploaded_file, sheet_names[i]).columns):
                                st.error(f'Отсутствуют столбцы: {set(st.session_state.selected_columns) - set(df.columns)}')
                            elif st.session_state.selected_columns:
                                selected_df = load_excel(uploaded_file, sheet_names[i])[st.session_state.selected_columns]
                                st.write("Датафрейм с выбранными столбцами:")
                                st.dataframe(selected_df)
                            else:
                                st.write("Столбцы не выбраны.")
 
                        with column2:
                            if len(st.session_state.selected_columns) == 5:
                                def add_color():
                                    name_new_color = st.selectbox(
                                        "Выберите флаг",
                                        options=pd.concat([load_excel(uploaded_file, sheet_names[i]).iloc[:, 1], load_excel(uploaded_file, sheet_names[i]).iloc[:, 3]], ignore_index=True).drop_duplicates(),  # Отображаемые варианты
                                        key=f'selectbox_{sheet_names[i]}'
                                    )
                                    with st.form(key=f'form_{sheet_names[i]}'):
                                        add_button = st.form_submit_button("Добавить")
                                        new_color = st.color_picker('введите обозначение', '#00FF00', key=f'form_{sheet_names[i]}_{name_new_color}')
                                        if add_button and (name_new_color, new_color) not in st.session_state.map_colors:
                                            st.session_state.map_colors[name_new_color] = new_color
 
                                    for key, value in st.session_state.map_colors.items():
                                        st.color_picker(key, value, key=f'form_{sheet_names[i]}{key}{value}')
                                add_color()
                            else:
                                st.warning('Выберите 5 столбцов, для редактирования цвета относительно флагов')
 
    elif file_extension in ['csv', 'tsv']:
        display_options = [", (запятая)", "; (точка с запятой)", "\\t (табуляция)", "| (вертикальная черта)", "пробел"]
        # Список реальных разделителей
        delimiter_options = [",", ";", "\t", "|", " "]

        # Выбор разделителя
        selected_display = st.selectbox(
            "Выберите разделитель",
            options=display_options,  # Отображаемые варианты
            index=0 if file_extension == 'csv' else 2,  # По умолчанию "," для CSV и "\\t" для TSV
            help="Выберите разделитель, используемый в вашем файле."
        )
        try:
            try:
                # Получение реального разделителя на основе выбранного отображаемого значения
                delimiter = delimiter_options[display_options.index(selected_display)]
            except:
                st.error("Неподдерживаемый разделитель")
            # Кэширование данных с учетом выбранного разделителя
            @st.cache_data
            def load_delimited_file(file, delimiter):
                # Попробуйте разные кодировки, если UTF-8 не работает
                try:
                    df = pd.read_csv(file, sep=delimiter, encoding='utf-8').astype(str)
                except UnicodeDecodeError:
                    df = pd.read_csv(file, sep=delimiter, encoding='windows-1251').astype(str)
                df.fillna('', inplace=True)
                return df
 
            df = load_delimited_file(uploaded_file, delimiter)
            st.dataframe(df)
 
            # Создаем колонки для чекбоксов
            cols = st.columns(len(df.columns))  # Создаем столько колонок, сколько столбцов в датафрейме
 
            # Отображение чекбоксов по горизонтали
            st.write("Выберите столбцы:")
            for idx, col_name in enumerate(df.columns):
                with cols[idx]:
                    st.checkbox(
                        col_name,
                        key=col_name,
                        value=col_name in st.session_state.selected_columns,
                        on_change=update_selected_columns,
                        args=(col_name,)
                    )
            column1, column2 = st.columns([2, 1])
            with column1:
                if st.session_state.selected_columns:
                    selected_df = df[st.session_state.selected_columns]
                    st.write("Датафрейм с выбранными столбцами:")
                    st.dataframe(selected_df)
                else:
                    st.write("Столбцы не выбраны.")
 
            with column2:
                if len(st.session_state.selected_columns) == 5:
                    def add_color():
                        name_new_color = st.selectbox(
                            "Выберите флаг",
                            options=pd.concat([df.iloc[:, 1], df.iloc[:, 3]], ignore_index=True).drop_duplicates(),  # Отображаемые варианты
                            key=f'selectbox_csv'
                        )
                        with st.form(key=f'form'):
                            add_button = st.form_submit_button("Добавить")
                            new_color = st.color_picker('введите обозначение', '#00FF00', key=f'form_{name_new_color}')
                            if add_button and (name_new_color, new_color) not in st.session_state.map_colors:
                                st.session_state.map_colors[name_new_color] = new_color
 
                        for key, value in st.session_state.map_colors.items():
                            st.color_picker(key, value, key=f'form_{key}{value}') 
                    add_color()
                else:
                    st.warning('Выберите 5 столбцов, для редактирования цвета относительно флагов')

        except Exception as e:
            st.error(f"ошибка построения {e}")
    else:
        st.error("Неподдерживаемый формат файла. Пожалуйста, загрузите файл в формате XLSX, CSV или TSV.")
 
 
 
    if len(st.session_state.selected_columns) != 5 and len(st.session_state.selected_columns) != 3 and len(st.session_state.selected_columns) != 2:
        st.markdown(tooltip('Количество столбцов должно быть 2, 3 или 5'), unsafe_allow_html=True)
    else:
        st.divider()
        col11, col22 = st.columns([1, 1])
        with col11:
            st.markdown("### 3. Сформировать графы", unsafe_allow_html=True)
            draw_graph_button = st.button('Построить графы')
        if draw_graph_button:
            if len(st.session_state.selected_columns) == 5:
                selected_df[st.session_state.selected_columns[1]] = selected_df[st.session_state.selected_columns[1]].map(st.session_state.map_colors).fillna('green')
                selected_df[st.session_state.selected_columns[3]] = selected_df[st.session_state.selected_columns[3]].map(st.session_state.map_colors).fillna('green')
            elif len(st.session_state.selected_columns) == 3:
                selected_df.insert(1, 'flag1', 'green')
                selected_df.insert(3, 'flag2', 'green')
            else:
                selected_df.insert(1, 'flag1', 'green')
                selected_df.insert(3, 'flag3', 'green')                
                selected_df.insert(4, 'amount', '')

            with col11:
                text_spinner = "Построение графов"
                with st.spinner(text_spinner):
                    with col22:
                        st.image("gifs/snoop-dogg-dance.gif")
                        # st.image("gifs/pedro-raccoon.gif")

                    response = requests.post(f"{BACKEND_URL}/upload", json={
                        "file_df": selected_df.astype('str').values.tolist(),
                        'map_colors': st.session_state.map_colors,
                    })
                    
                    if response.status_code == 200:
                        st.success(f"Графы построились")
                        st.balloons()
                    elif response.status_code == 201:
                        st.warning(f"Построились 50 наибольших графов")
                        st.balloons()
                    else:
                        st.error("Ошибка" + response.text[len('"message": "')+1:-3])