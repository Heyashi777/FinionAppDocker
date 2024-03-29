# Импортируем нужные библиотеки
import dash
import os
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import numpy as np
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import csv
from sklearn.linear_model import LinearRegression
import datetime

# Функция, которая строит стобчатый график и линию тренда
def line_new(name):
    global fig_lines
    
    x_0, x_1, x_2, x_3, x_4 = np.array([]), np.array([]), np.array([]), np.array([]), np.array([])
    x_5, x_6, x_7, x_8, x_9 = np.array([]), np.array([]), np.array([]), np.array([]), np.array([])
    x_10, x_11, x_12, x_13, x_14 = np.array([]), np.array([]), np.array([]), np.array([]), np.array([])
    x_15 = np.array([])
    
    clasters_name_1 = ['Не обработан', 'В работе', 'Нужно позже', 'Потребность выявлена',
                       'Нет услуги, нужной клиенту', 'КП отправлено', 'Качественный лид',
                       'Ложный старт', 'Не можем отправить сообщение', 'Дорого',
                       'Не оставлял заявку', 'Провал', 'Техническая заявка',
                       'Не подходит по условиям', 'Перестал отвечать (спустя 14 дней)',
                       'Выбрал другую компанию']
    month = ['Январь','Февраль','Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
             'Октябрь', 'Ноябрь', 'Декабрь']
    
    for j in range(16):
        for i in range(1, 13):
            y = len (
                main_data[ (main_data['Кем создан'] == name) &
                           (main_data['Дата создания.4'] == i) &
                           (main_data['Стадия'] == clasters_name_1[j])
                         ] 
                    )
            if j == 0:
                x_0 = np.append(x_0, y)
            elif j == 1:
                x_1 = np.append(x_1, y)
            elif j == 2:
                x_2 = np.append(x_2, y)
            elif j == 3:
                x_3 = np.append(x_3, y)
            elif j == 4:
                x_4 = np.append(x_4, y)
            elif j == 5:
                x_5 = np.append(x_5, y)
            elif j == 6:
                x_6 = np.append(x_6, y)
            elif j == 7:
                x_7 = np.append(x_7, y)
            elif j == 8:
                x_8 = np.append(x_8, y)
            elif j == 9:
                x_9 = np.append(x_9, y)
            elif j == 10:
                x_10 = np.append(x_10, y)
            elif j == 11:
                x_11 = np.append(x_11, y)
            elif j == 12:
                x_12 = np.append(x_12, y)
            elif j == 13:
                x_13 = np.append(x_13, y)
            elif j == 14:
                x_14 = np.append(x_14, y)
            elif j == 15:
                x_15 = np.append(x_15, y)
                
    array = [x_0, x_1, x_2, x_3, x_4,x_5, x_6, x_7, x_8, x_9,x_10, x_11, x_12, x_13, x_14,x_15 ]   
    array_1 = np.array([])
    
    for i in range( len(array) ):
        df = pd.DataFrame()
        df['count'] = array[i]
        Y=df['count']
        X=df.index
        # regression
        reg = LinearRegression().fit(np.vstack(X), Y)
        df['bestfit'] = reg.predict(np.vstack(X))
        array_1 = np.append(array_1, df['bestfit'])
        
    fig_lines = make_subplots(rows = 8, cols = 2, subplot_titles = clasters_name_1)
    fig_lines.update_layout(height=1800, width=1250, title_text="Графики кол-во людей на разных стадиях")
    fig_lines.update_xaxes(title_text="Месяц")
    fig_lines.update_yaxes(title_text="Кол-во клиентов")
    
    for i in range(1,9):
        fig_lines.add_trace(go.Bar(name='кол-во человек в месяц', x=month, y=array[i - 1],
                                   showlegend=False,marker_color=('#0E2432')), row = i, col = 1)
        fig_lines.add_trace(go.Scatter(name='линия тренда', x=month, y=array_1[0 + (i-1)*12 : 12 + (i-1)*12],
                                       mode='lines',showlegend=False,marker_color=('#BFA168')), row = i, col = 1)
    for i in range(1,9):
        fig_lines.add_trace(go.Bar(name='кол-во человек в месяц', x=month, y=array[7 + i],
                                   showlegend=False,marker_color=('#0E2432')), row = i, col = 2)
        fig_lines.add_trace(go.Scatter(name='линия тренда', x=month, y=array_1[0 + (7+i)*12 : 12 + (7+i)*12],
                                       mode='lines',showlegend=False,marker_color=('#BFA168')), row = i, col = 2)

# Берём локальные данные с компьютера, где собрана база данных по лидам. Планируется подключение к SQL-серверу
main_data = pd.read_excel('/Users/erickgaydin/Desktop/main_data_c.xlsx')
# Записываем в переменные основные стадии, месяцы и т.д., чтобы удобно работали циклы перебора
month = ['Январь','Февраль','Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
         'Ноябрь', 'Декабрь']
clasters_name = ['Всего людей в работе','Не обработан', 'В работе', 'Потребность выявлена',
                 'КП отправлено', 'Качественный лид',  'Не оставлял заявку',
                 'Перестал отвечать (спустя 14 дней)']
name_consultants = ['Анастасия Шипулина', 'Ксения Комарова', 'Юлия Збрыкина', 'Елена Шавернева', 'Ксения Цветкова',
                    'Анастасия Деккер', 'Юлия Богданова',
                    'Валерий Данилов', 'Алина Позднякова']
clasters_name_hell = ['Всего людей в работе', 'Нет услуги, нужной клиенту','Ложный старт','Дорого','Провал','Не подходит по условиям',
                      'Выбрал другую компанию','Нужно позже']
# Функция, которая строит таблицу: у какого консультанта сколько клиентов 
def how_clients_all():
    global data_how_clients
    data_how_clients = pd.DataFrame()
    data_how_clients['Имя'] = range(len(name_consultants))
    data_how_clients['Кол-во человек'] = range(len(name_consultants))
    for i in range( len(name_consultants) ):
        data_how_clients.at[i,'Имя'] = name_consultants[i]
        data_how_clients.at[i,'Кол-во человек'] = len(main_data[ (main_data['Кем создан'] == name_consultants[i])
                                                                & (main_data['Дата создания.4'] == 12 ) ])
        
# Функция, которая строит 16 графиков по кол-ву людей на каждой стадии по месяцам

def lines_clasters(name):
    global fig_lines
    x_0, x_1, x_2, x_3, x_4 = np.array([]), np.array([]), np.array([]), np.array([]), np.array([])
    x_5, x_6, x_7, x_8, x_9 = np.array([]), np.array([]), np.array([]), np.array([]), np.array([])
    x_10, x_11, x_12, x_13, x_14 = np.array([]), np.array([]), np.array([]), np.array([]), np.array([])
    x_15 = np.array([])
    clasters_name_1 = ['Не обработан', 'В работе', 'Нужно позже', 'Потребность выявлена',
                       'Нет услуги, нужной клиенту', 'КП отправлено', 'Качественный лид',
                       'Ложный старт', 'Не можем отправить сообщение', 'Дорого',
                       'Не оставлял заявку', 'Провал', 'Техническая заявка',
                       'Не подходит по условиям', 'Перестал отвечать (спустя 14 дней)',
                       'Выбрал другую компанию']
    month = ['Январь','Февраль','Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
             'Октябрь', 'Ноябрь', 'Декабрь']
    for j in range(16):
        for i in range(1, 13):
            y = len (
                main_data[ (main_data['Кем создан'] == name) &
                           (main_data['Дата создания.4'] == i) &
                           (main_data['Стадия'] == clasters_name_1[j])
                         ] 
                    )
            if j == 0:
                x_0 = np.append(x_0, y)
            elif j == 1:
                x_1 = np.append(x_1, y)
            elif j == 2:
                x_2 = np.append(x_2, y)
            elif j == 3:
                x_3 = np.append(x_3, y)
            elif j == 4:
                x_4 = np.append(x_4, y)
            elif j == 5:
                x_5 = np.append(x_5, y)
            elif j == 6:
                x_6 = np.append(x_6, y)
            elif j == 7:
                x_7 = np.append(x_7, y)
            elif j == 8:
                x_8 = np.append(x_8, y)
            elif j == 9:
                x_9 = np.append(x_9, y)
            elif j == 10:
                x_10 = np.append(x_10, y)
            elif j == 11:
                x_11 = np.append(x_11, y)
            elif j == 12:
                x_12 = np.append(x_12, y)
            elif j == 13:
                x_13 = np.append(x_13, y)
            elif j == 14:
                x_14 = np.append(x_14, y)
            elif j == 15:
                x_15 = np.append(x_15, y)
    fig_lines = make_subplots(rows = 8, cols = 2, subplot_titles = clasters_name_1)
    fig_lines.update_layout(height=1800, width=1250, title_text="Графики кол-во людей на разных стадиях")
    fig_lines.update_xaxes(title_text="Месяц")
    fig_lines.update_yaxes(title_text="Кол-во клиентов")
    fig_lines.add_trace(go.Scatter(x=month, y=x_0, name = clasters_name_1[0],showlegend=False), row = 1, col = 1)
    fig_lines.add_trace(go.Scatter(x=month, y=x_1, name = clasters_name_1[1],showlegend=False), row = 1, col = 2)
    fig_lines.add_trace(go.Scatter(x=month, y=x_2, name = clasters_name_1[2],showlegend=False), row = 2, col = 1)
    fig_lines.add_trace(go.Scatter(x=month, y=x_3, name = clasters_name_1[3],showlegend=False), row = 2, col = 2)
    fig_lines.add_trace(go.Scatter(x=month, y=x_4, name = clasters_name_1[4],showlegend=False), row = 3, col = 1)
    fig_lines.add_trace(go.Scatter(x=month, y=x_5, name = clasters_name_1[5],showlegend=False), row = 3, col = 2)
    fig_lines.add_trace(go.Scatter(x=month, y=x_6, name = clasters_name_1[6],showlegend=False), row = 4, col = 1)
    fig_lines.add_trace(go.Scatter(x=month, y=x_7, name = clasters_name_1[7],showlegend=False), row = 4, col = 2)
    fig_lines.add_trace(go.Scatter(x=month, y=x_8, name = clasters_name_1[8],showlegend=False), row = 5, col = 1)
    fig_lines.add_trace(go.Scatter(x=month, y=x_9, name = clasters_name_1[9],showlegend=False), row = 5, col = 2)
    fig_lines.add_trace(go.Scatter(x=month, y=x_10, name = clasters_name_1[10],showlegend=False), row = 6, col = 1)
    fig_lines.add_trace(go.Scatter(x=month, y=x_11, name = clasters_name_1[11],showlegend=False), row = 6, col = 2)
    fig_lines.add_trace(go.Scatter(x=month, y=x_12, name = clasters_name_1[12],showlegend=False), row = 7, col = 1)
    fig_lines.add_trace(go.Scatter(x=month, y=x_13, name = clasters_name_1[13],showlegend=False), row = 7, col = 2)
    fig_lines.add_trace(go.Scatter(x=month, y=x_14, name = clasters_name_1[14],showlegend=False), row = 8, col = 1)
    fig_lines.add_trace(go.Scatter(x=month, y=x_15, name = clasters_name_1[15],showlegend=False), row = 8, col = 2)

# Функция, которая строит воронку продаж и воронку  провалов
def voronka(name):
    global x, x_1

    x = np.array([
                    len(
                        main_data[ (main_data['Кем создан'] == name) 
                        & (main_data['Дата создания.4'] == 12)] ) 
                ])

    for i in range( len(clasters_name) ):
        y =  len(
                 main_data[ (main_data['Кем создан'] == name) 
                 & (main_data['Дата создания.4'] == 12)
                 & (main_data['Стадия'] == clasters_name[i])] 
                )
        x = np.append(x, y)

    x_1 = np.array([
                    len(
                            main_data[ (main_data['Кем создан'] == name) 
                         & (main_data['Дата создания.4'] == 12)] 
                        ) 
                    ])

    for i in range( len(clasters_name_hell) ):
        y =  len(
                    main_data[ (main_data['Кем создан'] == name) 
                 & (main_data['Дата создания.4'] == 12)
                 & (main_data['Стадия'] == clasters_name_hell[i])] 
                )
        x_1 = np.append(x_1, y)

# Функия, которая строит таблицу, где показано, от куда консультанты брали лиды
def lead_from_main():
    global df_1
    partners_name = main_data['Источник'].unique()
    df_1 = pd.DataFrame()
    df_1['Источник'] = range(len(partners_name))
    df_1['Кол-во лидов'] = range(len(partners_name))
    for i in range( len(partners_name) ):
        df_1.at[i, 'Источник'] = partners_name[i]
        df_1.at[i, 'Кол-во лидов'] = len(
                                            main_data[
                                                        (main_data['Дата создания.4']== 12)&
                                                        (main_data['Источник']== partners_name[i])
                                                      ]
                                        )
    df_1 = df_1[ df_1['Кол-во лидов'] > 0 ]
# Функция, которая такая же, как и прошлая
def lead_from(name):
    global df
    partners_name = main_data['Источник'].unique()
    df = pd.DataFrame()
    df['Источник'] = range(len(partners_name))
    df['Кол-во лидов'] = range(len(partners_name))
    for i in range( len(partners_name) ):
        df.at[i, 'Источник'] = partners_name[i]
        df.at[i, 'Кол-во лидов'] = len(
                                        main_data[ 
                                                       (main_data['Кем создан']== name)
                                                     & (main_data['Источник']== partners_name[i])
                                                     & (main_data['Дата создания.4']== 12)
                                                 ]
                                        )
    df = df[ df['Кол-во лидов'] > 0 ]  
########################################################
########################################################
# Добавляем стиль в приложение
#Второй вариант вариант
external_stylesheets = ['https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap']
colors = {
    'background': '#111111',
    'text': '#0e2230'
}
#Первый вариант 
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Создаём приложение 
app = dash.Dash(name=__name__, external_stylesheets=external_stylesheets)
# Делаем наполнение приложения, а именно: кнопки на консультантов и заглавие приложения
app.layout = html.Div([
    html.H1('Аналитика Finion',
                   style={"font-family": "'Press Start 2P'",
                          'textAlign': 'center', 'color': 'black', 'fontSize': 30}),
    dcc.Tabs(id="tabs", value='tab-0', children=[
        dcc.Tab(label='Ксения Комарова', value='tab-2'),
        dcc.Tab(label='Анастасия Деккер', value='tab-3'),
        dcc.Tab(label='Юлия Богданова', value='tab-4'),
        dcc.Tab(label='Елена Шавернева', value='tab-5'),
        dcc.Tab(label="Ксения Цветкова", value='tab-6'),
        dcc.Tab(label="Юлия Збрыкина", value='tab-7'),
        dcc.Tab(label="Анастасия Шипулина", value='tab-8'),
        dcc.Tab(label="<Без имени>", value='tab-9'),
        dcc.Tab(label='Администратор Портала', value='tab-10'),      
    ]),
    html.Div(id='tabs-content')
    ])

@callback(Output('tabs-content', 'children',allow_duplicate=False),
              Input('tabs', 'value'), prevent_initial_call=True)

# Наполняем кнопки смыслом, а именно для каждой: 
# 1) Количество клиентов в прошлый месяц - потенциально сделать шкалу выбора, которая позволила бы смотреть за конкретный месяц
# 2) Где консультант взял лиды - таблица, где написано сколько людей от куда 
# 3) Воронка продаж - классическая воронка продаж
# 4) Воронка провалов - не сколько воронка прям, сколько данные в % и в кол-во по провалам
# 5) Графики по стадиям - графики за 2023 год по стадиям и кол-во людей на них 

def render_content(tab):
        
    if tab == 'tab-2':
        # Запускаем функции, которые делают глобальные переменные с графиками и таблицами
        name_c = 'Ксения Комарова'
        voronka(name_c)
        fig_twins = make_subplots(rows = 1, cols = 1 ) 
        fig_twins.add_trace(go.Funnel(
                                    y = clasters_name,
                                    x = x,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2",
                                                        "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2" ]}
                                 ),
                                    row = 1, col = 1
                        )
        fig_twins_1 = make_subplots(rows = 1, cols = 1 ) 
        fig_twins_1.add_trace(go.Funnel(
                                    y = clasters_name_hell,
                                    x = x_1,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#c34532", "#c34532", "#c34532", "#c34532", "#c34532",
                                                        "#c34532", "#c34532", "#c34532"]}
                                    ),
                                    row = 1, col = 1
                        )
        lead_from(name_c)
        line_new(name_c)
        #lines_clasters(name_c)
         # Создаём наполнение кнопки
        return html.Div([
            html.H4('Человек в работе:', 
                           style={
                                    'textAlign': 'left',
                                    'color': colors['text']
                                 }
                   ),
            html.H4( len(main_data[ (main_data['Кем создан'] == name_c) 
                     & (main_data['Дата создания.4'] == 12)] ) ),
            dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns], id='tbl'),
            html.H4('Воронка продаж', 
                           style={
                                    'textAlign': 'left',
                                    'color': colors['text']
                                 }
                   ),
            dcc.Graph(id="graph", figure=fig_twins),
            html.Hr(),
            html.H4('Воронка провалов', 
                           style={
                                    'textAlign': 'left',
                                    'color': colors['text']
                                 }
                   ),
            dcc.Graph(id="graph", figure=fig_twins_1),
            html.Hr(),
            html.H4('Динамика по стадиям', 
                           style={
                                    'textAlign': 'left',
                                    'color': colors['text']
                                 }
                   ),
            dcc.Graph(id="graph", figure=fig_lines)
        ])
            
    if tab == 'tab-3':
            
        name_c = 'Анастасия Деккер'
        voronka(name_c)
        fig_twins = make_subplots(rows = 1, cols = 1 ) 
        fig_twins.add_trace(go.Funnel(
                                    y = clasters_name,
                                    x = x,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2",
                                                        "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2" ]}
                                 ),
                                    row = 1, col = 1
                        )
        fig_twins_1 = make_subplots(rows = 1, cols = 1 ) 
        fig_twins_1.add_trace(go.Funnel(
                                    y = clasters_name_hell,
                                    x = x_1,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#c34532", "#c34532", "#c34532", "#c34532", "#c34532",
                                                        "#c34532", "#c34532", "#c34532"]}
                                    ),
                                    row = 1, col = 1
                        )
        lead_from(name_c)
        line_new(name_c)
        #lines_clasters(name_c)
        return html.Div([
            html.H4('Человек в работе:'),
            html.H4( len(main_data[ (main_data['Кем создан'] == name_c) 
                     & (main_data['Дата создания.4'] == 12)] ) ),
            dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns], id='tbl'),
            html.H4('Воронка продаж'),
            dcc.Graph(id="graph", figure=fig_twins),
            html.Hr(),
            html.H4('Воронка провалов'),
            dcc.Graph(id="graph", figure=fig_twins_1),
            html.Hr(),
            dcc.Graph(id="graph", figure=fig_lines),
        ])
    if tab == 'tab-4':
        name_c = 'Юлия Богданова'
        voronka(name_c)
        fig_twins = make_subplots(rows = 1, cols = 1 ) 
        fig_twins.add_trace(go.Funnel(
                                    y = clasters_name,
                                    x = x,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2",
                                                        "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2" ]}
                                 ),
                                    row = 1, col = 1
                        )
        fig_twins_1 = make_subplots(rows = 1, cols = 1 ) 
        fig_twins_1.add_trace(go.Funnel(
                                    y = clasters_name_hell,
                                    x = x_1,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#c34532", "#c34532", "#c34532", "#c34532", "#c34532",
                                                        "#c34532", "#c34532", "#c34532"]}
                                    ),
                                    row = 1, col = 1
                        )
        lead_from(name_c)
        line_new(name_c)
        #lines_clasters(name_c)
        return html.Div([
            html.H4('Человек в работе:'),
            html.H4( len(main_data[ (main_data['Кем создан'] == name_c) 
                     & (main_data['Дата создания.4'] == 12)] ) ),
            dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns], id='tbl'),
            html.H4('Воронка продаж'),
            dcc.Graph(id="graph", figure=fig_twins),
            html.Hr(),
            html.H4('Воронка провалов'),
            dcc.Graph(id="graph", figure=fig_twins_1),
            html.Hr(),
            dcc.Graph(id="graph", figure=fig_lines),
        ])
    if tab == 'tab-5':
        name_c = 'Елена Шавернева'
        voronka(name_c)
        fig_twins = make_subplots(rows = 1, cols = 1 ) 
        fig_twins.add_trace(go.Funnel(
                                    y = clasters_name,
                                    x = x,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2",
                                                        "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2" ]}
                                 ),
                                    row = 1, col = 1
                        )
        fig_twins_1 = make_subplots(rows = 1, cols = 1 ) 
        fig_twins_1.add_trace(go.Funnel(
                                    y = clasters_name_hell,
                                    x = x_1,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#c34532", "#c34532", "#c34532", "#c34532", "#c34532",
                                                        "#c34532", "#c34532", "#c34532"]}
                                    ),
                                    row = 1, col = 1
                        )
        lead_from(name_c)
        line_new(name_c)
        #lines_clasters(name_c)
        return html.Div([
            html.H4('Человек в работе:'),
            html.H4( len(main_data[ (main_data['Кем создан'] == name_c) 
                     & (main_data['Дата создания.4'] == 12)] ) ),
            dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns], id='tbl'),
            html.H4('Воронка продаж'),
            dcc.Graph(id="graph", figure=fig_twins),
            html.Hr(),
            html.H4('Воронка провалов'),
            dcc.Graph(id="graph", figure=fig_twins_1),
            html.Hr(),
            dcc.Graph(id="graph", figure=fig_lines),
        ])
    if tab == 'tab-6':
        name_c = "Ксения Цветкова"
        voronka(name_c)
        fig_twins = make_subplots(rows = 1, cols = 1 ) 
        fig_twins.add_trace(go.Funnel(
                                    y = clasters_name,
                                    x = x,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2",
                                                        "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2" ]}
                                 ),
                                    row = 1, col = 1
                        )
        fig_twins_1 = make_subplots(rows = 1, cols = 1 ) 
        fig_twins_1.add_trace(go.Funnel(
                                    y = clasters_name_hell,
                                    x = x_1,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#c34532", "#c34532", "#c34532", "#c34532", "#c34532",
                                                        "#c34532", "#c34532", "#c34532"]}
                                    ),
                                    row = 1, col = 1
                        )
        lead_from(name_c)
        line_new(name_c)
        #lines_clasters(name_c)
        return html.Div([
            html.H4('Человек в работе:'),
            html.H4( len(main_data[ (main_data['Кем создан'] == name_c) 
                     & (main_data['Дата создания.4'] == 12)] ) ),
            dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns], id='tbl'),
            html.H4('Воронка продаж'),
            dcc.Graph(id="graph", figure=fig_twins),
            html.Hr(),
            html.H4('Воронка провалов'),
            dcc.Graph(id="graph", figure=fig_twins_1),
            html.Hr(),
            dcc.Graph(id="graph", figure=fig_lines),
        ])
    if tab == 'tab-7':
        name_c = "Юлия Збрыкина"
        voronka(name_c)
        fig_twins = make_subplots(rows = 1, cols = 1 ) 
        fig_twins.add_trace(go.Funnel(
                                    y = clasters_name,
                                    x = x,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2",
                                                        "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2" ]}
                                 ),
                                    row = 1, col = 1
                        )
        fig_twins_1 = make_subplots(rows = 1, cols = 1 ) 
        fig_twins_1.add_trace(go.Funnel(
                                    y = clasters_name_hell,
                                    x = x_1,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#c34532", "#c34532", "#c34532", "#c34532", "#c34532",
                                                        "#c34532", "#c34532", "#c34532"]}
                                    ),
                                    row = 1, col = 1
                        )
        lead_from(name_c)
        line_new(name_c)
        #lines_clasters(name_c)
        return html.Div([
            html.H4('Человек в работе:'),
            html.H4( len(main_data[ (main_data['Кем создан'] == name_c) 
                     & (main_data['Дата создания.4'] == 12)] ) ),
            dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns], id='tbl'),
            html.H4('Воронка продаж'),
            dcc.Graph(id="graph", figure=fig_twins),
            html.Hr(),
            html.H4('Воронка провалов'),
            dcc.Graph(id="graph", figure=fig_twins_1),
            html.Hr(),
            dcc.Graph(id="graph", figure=fig_lines),
        ])   
    if tab == 'tab-8':
        name_c = "Анастасия Шипулина"
        voronka(name_c)
        fig_twins = make_subplots(rows = 1, cols = 1 ) 
        fig_twins.add_trace(go.Funnel(
                                    y = clasters_name,
                                    x = x,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2",
                                                        "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2" ]}
                                 ),
                                    row = 1, col = 1
                        )
        fig_twins_1 = make_subplots(rows = 1, cols = 1 ) 
        fig_twins_1.add_trace(go.Funnel(
                                    y = clasters_name_hell,
                                    x = x_1,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#c34532", "#c34532", "#c34532", "#c34532", "#c34532",
                                                        "#c34532", "#c34532", "#c34532"]}
                                    ),
                                    row = 1, col = 1
                        )
        lead_from(name_c)
        line_new(name_c)
        #lines_clasters(name_c)
        return html.Div([
            html.H4('Человек в работе:'),
            html.H4( len(main_data[ (main_data['Кем создан'] == name_c) 
                     & (main_data['Дата создания.4'] == 12)] ) ),
            dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns], id='tbl'),
            html.H4('Воронка продаж'),
            dcc.Graph(id="graph", figure=fig_twins),
            html.Hr(),
            html.H4('Воронка провалов'),
            dcc.Graph(id="graph", figure=fig_twins_1),
            html.Hr(),
            dcc.Graph(id="graph", figure=fig_lines),
        ])   
    if tab == 'tab-9':
        name_c = "<Без имени>"
        voronka(name_c)
        fig_twins = make_subplots(rows = 1, cols = 1 ) 
        fig_twins.add_trace(go.Funnel(
                                    y = clasters_name,
                                    x = x,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2",
                                                        "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2" ]}
                                 ),
                                    row = 1, col = 1
                        )
        fig_twins_1 = make_subplots(rows = 1, cols = 1 ) 
        fig_twins_1.add_trace(go.Funnel(
                                    y = clasters_name_hell,
                                    x = x_1,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#c34532", "#c34532", "#c34532", "#c34532", "#c34532",
                                                        "#c34532", "#c34532", "#c34532"]}
                                    ),
                                    row = 1, col = 1
                        )
        lead_from(name_c)
        line_new(name_c)
        #lines_clasters(name_c)
        return html.Div([
            html.H4('Человек в работе:'),
            html.H4( len(main_data[ (main_data['Кем создан'] == name_c) 
                     & (main_data['Дата создания.4'] == 12)] ) ),
            dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns], id='tbl'),
            html.H4('Воронка продаж'),
            dcc.Graph(id="graph", figure=fig_twins),
            html.Hr(),
            html.H4('Воронка провалов'),
            dcc.Graph(id="graph", figure=fig_twins_1),
            html.Hr(),
            dcc.Graph(id="graph", figure=fig_lines),
        ])
    if tab == 'tab-10':
        name_c = "Администратор Портала"
        voronka(name_c)
        fig_twins = make_subplots(rows = 1, cols = 1 ) 
        fig_twins.add_trace(go.Funnel(
                                    y = clasters_name,
                                    x = x,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2",
                                                        "#4e67a2", "#4e67a2", "#4e67a2", "#4e67a2" ]}
                                 ),
                                    row = 1, col = 1
                        )
        fig_twins_1 = make_subplots(rows = 1, cols = 1 ) 
        fig_twins_1.add_trace(go.Funnel(
                                    y = clasters_name_hell,
                                    x = x_1,
                                    textposition = "inside",
                                    textinfo = "value+percent initial",
                                    marker = {"color": ["#c34532", "#c34532", "#c34532", "#c34532", "#c34532",
                                                        "#c34532", "#c34532", "#c34532"]}
                                    ),
                                    row = 1, col = 1
                        )
        lead_from(name_c)
        line_new(name_c)
        #lines_clasters(name_c)
        return html.Div([
            html.H4('Человек в работе:'),
            html.H4( len(main_data[ (main_data['Кем создан'] == name_c) 
                     & (main_data['Дата создания.4'] == 12)] ) ),
            dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns], id='tbl'),
            html.H4('Воронка продаж'),
            dcc.Graph(id="graph", figure=fig_twins),
            html.Hr(),
            html.H4('Воронка провалов'),
            dcc.Graph(id="graph", figure=fig_twins_1),
            html.Hr(),
            dcc.Graph(id="graph", figure=fig_lines),
        ])    
       
# Запускаем приложение, порт можно любой
if __name__ == '__main__':
    port = os.environ.get('dash_port')
    debug = os.environ.get('dash_debug')=="True"
    app.run_server(debug=debug, host="0.0.0.0", port=port)
