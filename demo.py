import streamlit as st
import time
import pandas as pd

# Сырое демо, требует прокрутки и больше указаний где что нажать и что подсветить
# Также необходимо добавить пояснение по динамическому графу с примером

# Настройка страницы
st.set_page_config(page_title="Demo", layout="wide")

if 'page_loaded' not in st.session_state:
    st.session_state.page_loaded = False
if 'map_colors' not in st.session_state:
    st.session_state.map_colors = {
        'Отправитель': '#00FF00',
        'Получатель': '#00FF00'
    }
if 'demo_selected_columns' not in st.session_state:
    st.session_state.demo_selected_columns = []

# включаю для тестов
# st.session_state.page_loaded = True

# Основной CSS для анимации
css = """
<style>
div.block-container {
    padding-top: 3rem;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fadeIn {
    animation-name: fadeIn;
    animation-duration: 1s;
    animation-timing-function: ease-in-out;
    animation-fill-mode: both;
    width: 100%; /* Занимаем всю доступную ширину */
    margin-left: 20px !important; /* Отступ слева */
    margin-right: 20px !important; /* Отступ справа */
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

df = pd.DataFrame({
    'элемент1': ['шмурдик', 'грымзик', 'запырка', 'дубаратор', 'бушка', 'запырка'],
    'особые отметки элемента1': ['волосат', 'рогат', 'пушист', 'рогат', 'нежен', 'зеленоват'],
    'элемент2': ['кафля', 'уузка', 'грымзик', 'запырка', 'шмурдик', 'дубаратор'],
    'особые отметки элемента2': ['мягковат', 'нахален', 'рогат', 'пушист', 'волосат', 'рогат'],
    'связь': ['друг', 'враг', 'брат', 'друг', 'знакомый', 'сосед'],
    'лишний столбец': ['0', '1', '2', '3', '4', '5'],
    'другой столбец': ['красный', 'черный', 'острый', 'зеленый', 'плоский', 'синий'],
})

def animated_text(text, tag="h2", delay=1):
    return f"""
    <div class="fadeIn" style="animation-delay: {delay}s;">
        <{tag}>{text}</{tag}>
    </div>
    """

# Функция обновления выбранных столбцов
def update_selected_columns(column):
    if column in st.session_state.demo_selected_columns:
        st.session_state.demo_selected_columns.remove(column)
    else:
        st.session_state.demo_selected_columns.append(column)

# Первичная загрузка страницы
if not st.session_state.page_loaded:
    # Шаг 1: Анимированный текст
    header_placeholder = st.empty()
    with header_placeholder.container():
        st.markdown(animated_text("Добро пожаловать в демо", tag='h1', delay=1), unsafe_allow_html=True)
        time.sleep(2)  # Пауза перед следующим шагом

    # Шаг 2: Выбор файла
    file_uploader_placeholder = st.empty()
    with file_uploader_placeholder.container():
        st.markdown(animated_text("1. Выберите файл", tag='h1', delay=2), unsafe_allow_html=True)
        time.sleep(3)  # Пауза перед показом file_uploader
        uploaded_file = st.file_uploader(
            "Загрузите excel или csv файл", 
            type={"xlsx", "csv", "tsv"}
        )

    # Шаг 3: Инструкции
    instructions_placeholder = st.empty()
    with instructions_placeholder.container():
        styled_text = """
            <div style="font-family: Arial, sans-serif; line-height: 1.6;">
                <p style="font-size: 18px;">
                    После загрузки файла
                </p>
                <p style="font-size: 16px;">
                    <strong>Выберите столбцы</strong>:
                </p>
                <ul style="list-style-type: disc; padding-left: 20px; font-size: 16px;">
                    <li>
                        Просмотр взаимосвязей 
                        <span style="color: #28A745; font-weight: bold;">ЭЛЕМЕНТ1</span>, 
                        <span style="color: #28A745; font-weight: bold;">ЭЛЕМЕНТ2</span>
                    </li>
                    <li>
                        Базовый анализ: 
                        <span style="color: #DC3545; text-decoration: underline;">ОТПРАВИТЕЛЬ</span>, 
                        <span style="color: #DC3545; text-decoration: underline;">ПОЛУЧАТЕЛЬ</span>, 
                        <span style="color: #DC3545; text-decoration: underline;">СУММА</span>
                    </li>
                    <li>
                        Расширенный анализ (с изменением цвета нод): 
                        <span style="color: #FFC107; font-weight: bold;">ОТПРАВИТЕЛЬ</span>, 
                        <span style="color: #FFC107; font-weight: bold;">ФЛАГ_ОТПРАВИТЕЛЯ</span>, 
                        <span style="color: #FFC107; font-weight: bold;">ПОЛУЧАТЕЛЬ</span>, 
                        <span style="color: #FFC107; font-weight: bold;">ФЛАГ_ПОЛУЧАТЕЛЯ</span>, 
                        <span style="color: #FFC107; font-weight: bold;">СУММА</span>
                    </li>
                </ul>
            </div>
        """
        st.markdown((animated_text(styled_text, tag='div', delay=1)), unsafe_allow_html=True)
        time.sleep(2)  # Пауза перед следующим шагом

    # Шаг 4: Данные
    dataframe_placeholder = st.empty()
    with dataframe_placeholder.container():
        st.divider()
        st.markdown(animated_text("2. Работа с данными", tag='h1', delay=1), unsafe_allow_html=True)
        st.markdown(animated_text("Далее необходимо выбрать нужные для построения графа столбцы", tag='p', delay=2), unsafe_allow_html=True)
        time.sleep(3)  # Пауза перед показом данных

        st.dataframe(df)

    # Устанавливаем флаг, что страница загружена
    st.session_state.page_loaded = True
else:
    # Шаг 1: Анимированный текст
    header_placeholder = st.empty()
    with header_placeholder.container():
        st.markdown(animated_text("Добро пожаловать в демо", tag='h1', delay=0), unsafe_allow_html=True)

    # Шаг 2: Выбор файла
    file_uploader_placeholder = st.empty()
    with file_uploader_placeholder.container():
        st.markdown(animated_text("1. Выберите файл", tag='h1', delay=0), unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Загрузите excel или csv файл", 
            type={"xlsx", "csv", "tsv"}
        )

    # Шаг 3: Инструкции
    instructions_placeholder = st.empty()
    with instructions_placeholder.container():
        styled_text = """
            <div style="font-family: Arial, sans-serif; line-height: 1.6;">
                <p style="font-size: 18px;">
                    После загрузки файла
                </p>
                <p style="font-size: 16px;">
                    <strong>Выберите столбцы</strong>:
                </p>
                <ul style="list-style-type: disc; padding-left: 20px; font-size: 16px;">
                    <li>
                        Просмотр взаимосвязей 
                        <span style="color: #28A745; font-weight: bold;">ЭЛЕМЕНТ1</span>, 
                        <span style="color: #28A745; font-weight: bold;">ЭЛЕМЕНТ2</span>
                    </li>
                    <li>
                        Базовый анализ: 
                        <span style="color: #DC3545; text-decoration: underline;">ОТПРАВИТЕЛЬ</span>, 
                        <span style="color: #DC3545; text-decoration: underline;">ПОЛУЧАТЕЛЬ</span>, 
                        <span style="color: #DC3545; text-decoration: underline;">СУММА</span>
                    </li>
                    <li>
                        Расширенный анализ (с изменением цвета нод): 
                        <span style="color: #FFC107; font-weight: bold;">ОТПРАВИТЕЛЬ</span>, 
                        <span style="color: #FFC107; font-weight: bold;">ФЛАГ_ОТПРАВИТЕЛЯ</span>, 
                        <span style="color: #FFC107; font-weight: bold;">ПОЛУЧАТЕЛЬ</span>, 
                        <span style="color: #FFC107; font-weight: bold;">ФЛАГ_ПОЛУЧАТЕЛЯ</span>, 
                        <span style="color: #FFC107; font-weight: bold;">СУММА</span>
                    </li>
                </ul>
            </div>
        """
        st.markdown((animated_text(styled_text, tag='div', delay=0)), unsafe_allow_html=True)

    # Шаг 4: Данные
    dataframe_placeholder = st.empty()
    with dataframe_placeholder.container():
        st.divider()
        st.markdown(animated_text("2. Работа с данными", tag='h1', delay=0), unsafe_allow_html=True)
        st.markdown(animated_text("Далее необходимо выбрать нужные для построения графа столбцы", tag='p', delay=0), unsafe_allow_html=True)

        st.dataframe(df)

# Отображение чекбоксов (после загрузки страницы)
checkboxes_placeholder = st.empty()
with checkboxes_placeholder.container():
    cols = st.columns(len(df.columns))
    for idx, col_name in enumerate(df):
        with cols[idx]:
            st.checkbox(
                col_name,
                key=f"{col_name}",  # Уникальный ключ для каждого чекбокса
                value=col_name in st.session_state.demo_selected_columns,
                on_change=update_selected_columns,
                args=(col_name,)
            )

column1, column2 = st.columns([2, 1])

if st.session_state.demo_selected_columns == ['элемент1', 'элемент2']:
    # st.components.v1.html("""""")
    st.success("Выбраны столбцы для графа взаимосвязей")
elif st.session_state.demo_selected_columns == ['элемент1', 'элемент2', 'связь']:
    # st.components.v1.html("""""")
    st.success("Выбраны столбцы для базового анализа графа")
elif st.session_state.demo_selected_columns == ['элемент1', 'особые отметки элемента1', 'элемент2', 'особые отметки элемента2', 'связь']:
    # st.components.v1.html("""""")
    with column1:
        st.success("Выбраны столбцы для расширенного анализ графа")
    with column2:
        st.success("Выберите свойства и цвета для них")
        def add_color():
            name_new_color = st.selectbox(
                "Выберите флаг",
                options=pd.concat([df.iloc[:, 1], df.iloc[:, 3]], ignore_index=True).drop_duplicates(),  # Отображаемые варианты
                key=f'selectbox'
            )
            with st.form(key=f'form'):
                add_button = st.form_submit_button("Добавить")
                new_color = st.color_picker('выберите цвет', '#00FF00', key=f'form_{name_new_color}')
                if add_button and (name_new_color, new_color) not in st.session_state.map_colors:
                    st.session_state.map_colors[name_new_color] = new_color
            for key, value in st.session_state.map_colors.items():
                st.color_picker(key, value, key=f'form_{key}_{value}')
        add_color()
    

with column1:
    if st.session_state.demo_selected_columns:
        selected_df = df[st.session_state.demo_selected_columns]
        st.write("Датафрейм с выбранными столбцами:")
        st.dataframe(selected_df)
    else:
        st.write("Столбцы не выбраны.")
if len(st.session_state.map_colors.items()) > 2:
    st.divider()
    st.markdown(animated_text("Вы настоящий специалист по графам\n и готовы к самостоятельной работе", tag='h1', delay=1), unsafe_allow_html=True)
    time.sleep(2)
    if st.button('Завершить демо'):
        st.session_state.map_colors = {
            'Отправитель': '#00FF00',
            'Получатель': '#00FF00'
        }
        st.switch_page("pages/Load_data.py")