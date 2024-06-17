# views.py
from django.shortcuts import render
from django.http import HttpResponse
from google.cloud import bigquery
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'bqops_new/index.html')

@csrf_exempt
def fetch_week_info(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')

        # Validate query here if needed
        if not query:
            return HttpResponse("Invalid query", status=400)
        
        client = bigquery.Client()
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
    return HttpResponse("Invalid request method", status=405)
