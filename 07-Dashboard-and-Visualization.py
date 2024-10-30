# Step 1: Import Libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Step 2: Load the dataset
file_path = r'D:\python\Data Science\Python\E-Commerce Sales Analysis\data\datasets\International sale Report.csv'
data = pd.read_csv(file_path)

# Preprocessing: Convert 'GROSS AMT' to numeric
data['GROSS AMT'] = pd.to_numeric(data['GROSS AMT'], errors='coerce')

# Step 3: Initialize the Dash app
app = dash.Dash(__name__)

# Step 4: Create layout for the dashboard
app.layout = html.Div([
    html.H1("Interactive Sales Dashboard"),
    
    # Dropdown to filter data by customer
    html.Label('Select Customer:'),
    dcc.Dropdown(id='customer-dropdown',
                 options=[{'label': cust, 'value': cust} for cust in data['CUSTOMER'].unique()],
                 value=data['CUSTOMER'].unique()[0]),

    # Dropdown to filter data by month
    html.Label('Select Month:'),
    dcc.Dropdown(id='month-dropdown',
                 options=[{'label': month, 'value': month} for month in data['Months'].unique()],
                 value=data['Months'].unique()[0]),

    # Graph for sales amount by SKU
    dcc.Graph(id='sales-bar-chart'),

    # Line chart showing sales trends over time
    dcc.Graph(id='sales-line-chart')
])

# Step 5: Define callbacks for interactivity
@app.callback(
    [Output('sales-bar-chart', 'figure'), Output('sales-line-chart', 'figure')],
    [Input('customer-dropdown', 'value'), Input('month-dropdown', 'value')]
)
def update_charts(selected_customer, selected_month):
    # Filter data based on dropdown selections
    filtered_data = data[(data['CUSTOMER'] == selected_customer) & (data['Months'] == selected_month)]
    
    # Bar chart: Total sales by SKU
    bar_chart = px.bar(filtered_data, x='SKU', y='GROSS AMT', title='Sales by SKU')

    # Line chart: Sales trend over time
    line_chart = px.line(filtered_data, x='DATE', y='GROSS AMT', title='Sales Trend Over Time')

    return bar_chart, line_chart

# Step 6: Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
