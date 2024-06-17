# views.py
from django.shortcuts import render
from django.http import HttpResponse
from google.cloud import bigquery

def index(request):
    return render(request, 'bqops/index.html')

def fetch_week_info(request):
    client = bigquery.Client()
    query = """
    SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` 
    WHERE state = "TX"
    LIMIT 10;
    """
    query_job = client.query(query)
    results = query_job.result()
    
    # Create table
    table_html = "<table border='1'><tr>"
    for field in results.schema:
        table_html += f"<th>{field.name}</th>"
    table_html += "</tr>"

    for row in results:
        table_html += "<tr>"
        for value in row.values():
            table_html += f"<td>{value}</td>"
        table_html += "</tr>"

    table_html += "</table>"

    return HttpResponse(table_html)
