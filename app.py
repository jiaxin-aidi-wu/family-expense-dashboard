import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

IDEAL_BUDGET = 8000
MAX_BUDGET = 11429

external_stylesheets = [
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = '家庭支出看板'

app.layout = html.Div(className='container-fluid my-5', style={'font-family': 'Microsoft YaHei'}, children=[
    html.Div(className='row', children=[

        # 左侧边栏
        html.Div(className='col-md-3 d-flex flex-column justify-content-center', style={
            'background-color': '#e6f0fa',
            'border-radius': '10px',
            'min-height': '90vh',
            'padding': '40px'
        }, children=[
            html.H2('支出摘要', className='mb-4'),
            html.Div(id='summary', className='mb-4'),
            html.H5('预算使用进度', className='mb-2'),
            html.Div(id='progress-bar', className='progress mb-4', style={'height': '30px'}),
            html.Button('刷新数据', id='update-button', n_clicks=0, className='btn btn-primary')
        ]),

        # 右侧图表区
        html.Div(className='col-md-9', children=[
            html.Div(className='row', children=[
                html.Div(className='col-md-6 mb-4', children=[dcc.Graph(id='expense-pie')]),
                html.Div(className='col-md-6 mb-4', children=[dcc.Graph(id='daily-line')]),
            ]),
            html.Div(className='row', children=[
                html.Div(className='col-md-6 mb-4', children=[dcc.Graph(id='monthly-line')]),
                html.Div(className='col-md-6 mb-4', children=[dcc.Graph(id='payer-bar')]),
            ]),
        ]),
    ])
])

@app.callback(
    [Output('summary', 'children'),
     Output('progress-bar', 'children'),
     Output('expense-pie', 'figure'),
     Output('daily-line', 'figure'),
     Output('monthly-line', 'figure'),
     Output('payer-bar', 'figure')],
    Input('update-button', 'n_clicks')
)
def update_dashboard(n):
    df = pd.read_csv('family_budget.csv', parse_dates=['日期'])
    df['日'] = df['日期'].dt.date
    df['月份'] = df['日期'].dt.to_period('M').astype(str)

    total_expense = df['金额'].sum()
    over_amount = max(total_expense - MAX_BUDGET, 0)
    usage_pct = total_expense / IDEAL_BUDGET * 100

    summary = html.Div([
        html.H5(f'本月支出：¥{total_expense:,.2f}'),
        html.H5(f'理想预算：¥{IDEAL_BUDGET:,.2f}'),
        html.H5(f'最大预算：¥{MAX_BUDGET:,.2f}'),
        html.H5(
            f'超出部分：¥{over_amount:,.2f}' if over_amount > 0 else '未超出最大预算',
            style={'color': 'red' if over_amount > 0 else 'green'}
        )
    ])

    bar_class = 'progress-bar bg-danger' if over_amount > 0 else 'progress-bar bg-success'
    progress = html.Div(
        className=bar_class,
        role='progressbar',
        style={
            'width': f'{min(usage_pct, 100)}%',
            'font-weight': 'bold',
            'font-size': '16px'
        },
        children=f'{usage_pct:.1f} % 已用'
    )

    # 饼图
    expense_df = df.groupby('分类')['金额'].sum().reset_index()
    expense_fig = px.pie(expense_df, values='金额', names='分类', title='支出分布',
                         color_discrete_sequence=px.colors.qualitative.Set3)

    # 每日折线图
    daily = df.groupby('日')['金额'].sum().reset_index()
    daily_fig = px.line(daily, x='日', y='金额', markers=True, title='本月每日支出',
                        color_discrete_sequence=['#4682B4'])
    daily_fig.update_xaxes(title_text='日期', title_standoff=10)

    # 月度折线图
    monthly = df.groupby('月份')['金额'].sum().reset_index()
    monthly_fig = px.line(monthly, x='月份', y='金额', markers=True, title='年度月度支出趋势',
                          color_discrete_sequence=['#4682B4'])
    monthly_fig.add_hline(y=IDEAL_BUDGET, line_dash="dot", line_color="green", annotation_text="理想预算")
    monthly_fig.add_hline(y=MAX_BUDGET, line_dash="dash", line_color="red", annotation_text="最大预算")
    monthly_fig.update_xaxes(title_text='月份', title_standoff=10)

    # 堆叠柱状图
    payer_df = df.groupby(['支付人', '分类'])['金额'].sum().reset_index()
    total_per_payer = df.groupby('支付人')['金额'].sum().reset_index()
    total_per_payer.rename(columns={'金额': '总计'}, inplace=True)
    max_layer = payer_df.loc[payer_df.groupby('支付人')['金额'].idxmax()]
    payer_df = payer_df.merge(total_per_payer, on='支付人', how='left')
    payer_df['text'] = payer_df.apply(
        lambda row: f"{row['总计']:.2f} 元" if row.name in max_layer.index else '', axis=1)

    payer_fig = px.bar(
        payer_df, x='支付人', y='金额', color='分类',
        barmode='stack', title='各成员支出',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        text='text'
    )
    payer_fig.update_traces(
        textposition='outside',
        cliponaxis=False
    )

    unique_payers = df['支付人'].unique()
    if len(unique_payers) > 0:
        per_payer_budget = IDEAL_BUDGET / len(unique_payers)
        payer_fig.add_hline(y=per_payer_budget, line_dash='dot',
                            line_color='green', annotation_text='人均预算')

    return summary, [progress], expense_fig, daily_fig, monthly_fig, payer_fig

if __name__ == '__main__':
    app.run(debug=True)
