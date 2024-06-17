# views.py
from django.shortcuts import render
from django.http import HttpResponse
from google.cloud import bigquery
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'bqops/index.html')

@csrf_exempt
def fetch_week_info(request):
    if request.method == 'POST':
        table = request.POST.get('table', '')
        print(table)

        # Map the selected option to the corresponding BigQuery table
        table_map = {
            'table1': 'your-dataset.table1',
            'table2': 'your-dataset.table2',
            'table3': 'your-dataset.table3',
            'table4': 'your-dataset.table4',
        }

        if table not in table_map:
            return HttpResponse("Invalid table selection", status=400)
        
        selected_table = table_map[table]

        client = bigquery.Client()
        query = f"""
        SELECT * FROM `{selected_table}`
        WHERE DATE_COLUMN >= CURRENT_DATE() - INTERVAL 7 DAY
        LIMIT 50
        """
        query_job = client.query(query)
        results = query_job.result()
        
        # Create table
        table_html = "<table class='table table-bordered'><thead><tr>"
        for field in results.schema:
            table_html += f"<th>{field.name}</th>"
        table_html += "</tr></thead><tbody>"

        for row in results:
            table_html += "<tr>"
            for value in row.values():
                table_html += f"<td>{value}</td>"
            table_html += "</tr>"

        table_html += "</tbody></table>"

        return HttpResponse(table_html)
    return HttpResponse("Invalid request method", status=405)
