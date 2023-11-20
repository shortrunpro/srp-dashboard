from django.shortcuts import render
import pandas as pd
from plotly.offline import plot
import plotly.express as px
import plotly.io as pio
from datetime import datetime, timedelta
import xmlrpc.client
import pandas as pd
import calendar

import numpy as np

currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year
test = calendar.month_name[currentMonth]


def key():
    return 'https://federalbrace.com:8099', 'PRODUCTION', 'admin', 'Sh0rtRp@dm1n%20#'
url, db, username, password = key()
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
ver = common.version()
uid = common.authenticate(db, username, password, {})
test = common.login(db, username, password)
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def index(request):
    day = str(currentDay) + '/' + calendar.month_abbr[currentMonth] + '/' + str(currentYear)
    dt = datetime.strptime(day, '%d/%b/%Y')
    start = dt - timedelta(days=dt.weekday()+3)
    end = start + timedelta(days=7) 
    week_range = start.strftime('%d/%b/%Y') + ' - ' + end.strftime('%d/%b/%Y')
    df = sale_order_model(start, end)
    df['date_order'] = pd.to_datetime(df['date_order']).dt.strftime('%d/%b/%Y')
    df = df.groupby('date_order', as_index=False).sum()
    title1 = week_range + ': ${:,.2f}'.format(df['amount_total'].sum())
    fig = px.bar(
        df, title=title1, 
        x=df['date_order'], y=df['amount_total'], 
        text_auto='.2s', template='plotly_dark', 
        labels={'date_order': 'Date', 'amount_total': 'Totals'},
        )
        
    fig.update_layout(
        yaxis_tickprefix = '$', 
        yaxis_tickformat = ',.2f',
        margin=dict(l=50, r=50, t=50, b=50),
        
        )
    fig.update_traces(textposition="outside")
    bar = plot(fig, output_type="div")
    context = {'sales_graph': bar}
    
    return render(request, 'sales_dashboard.html', context)

def week(request):
    df = sale_order_model('2023-10-10, 04:00:00', '2023-10-17, 04:00:00')
    fig = px.histogram(df, x=df['date_order'], y=df['amount_total'], text_auto='.2s', template='plotly_dark', 
                         labels={'date_order': 'Date', 'amount_total': 'Totals'})
    fig.update_layout(yaxis_tickprefix = '$', yaxis_tickformat = ',.2f')
    fig.update_traces(textposition="outside")
    bar = plot(fig, output_type="div")
    context = {'sales_graph': bar}
    return render(request, 'sales_dashboard.html', context)
def month(request):
    today = str(currentYear) + '-' + str(currentMonth) + '-' + str(currentDay)
    currentDate = str(currentYear) + '-' + str(currentMonth) + '-01' 
    df = sale_order_model(currentDate, today)
    df['date_order'] = pd.to_datetime(df['date_order']).dt.strftime('%b/%d')
    df = df.groupby('date_order', as_index=False).sum()
    title1 = 'This Months Sales: ${:,.2f}'.format(df['amount_total'].sum())
    fig = px.bar(df, title=title1, x=df['date_order'], y=df['amount_total'], 
                        text_auto='.2s', template='plotly_dark',
                        labels={'date_order': 'Date', 'amount_total': 'Totals'})
    fig.update_layout(
        yaxis_tickprefix = '$', 
        yaxis_tickformat = ',.2f',
        margin=dict(l=50, r=50, t=50, b=50),
        )
    fig.update_traces(textposition="outside")
    bar = plot(fig, output_type="div")
    context = {'sales_graph': bar}
    print(currentDate + ' - ' + today)
    return render(request, 'sales_dashboard.html', context)

def sale_order_model(dateLow, dateHigh):
    sales = models.execute_kw(db, uid, password,
        'sale.order',  'search_read', [[['date_order', '>=', dateLow], ['date_order', '<=', dateHigh],
        ['state', '!=', 'sent'], ['state', '!=', 'cancel'], ['state', '!=', 'draft'], ['state', '!=', 'estimate'], ['amount_total', '>', 0]]],
        {'fields': ['name', 'amount_total', 'web_store_id', 'customer_name', 'name', 'margin', 'date_order', 'state', 'partner_id', 'team_id']})
    df = pd.DataFrame(sales)
    cleaning = ['web_store_id', 'team_id']
    for x in cleaning:
        df[x] = df[x].astype(str).str.replace("[\([{})\]']", '', regex=True).str.split(',').str[1].str.strip()
    df['partner_id'] = df['partner_id'].astype(str).str.replace('[', '', regex=False).str.split(',').str[0].str.strip().astype(int)
    df['name'] = df['name'].astype(str).str.strip()
    return df

