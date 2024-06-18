from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from google.cloud import bigquery
import requests
import json
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/fetch_week_info", response_class=HTMLResponse)
async def fetch_week_info(request: Request, table: str = Form(...)):
    table_map = {
        'table1': 'your-dataset.table1',
        'table2': 'your-dataset.table2',
        'table3': 'your-dataset.table3',
        'table4': 'your-dataset.table4',
    }

    if table not in table_map:
        return HTMLResponse("Invalid table selection", status_code=400)

    selected_table = table_map[table]

    client = bigquery.Client()
    query = f"""
    SELECT * FROM `{selected_table}`
    WHERE DATE_COLUMN >= CURRENT_DATE() - INTERVAL 7 DAY
    LIMIT 50
    """
    query_job = client.query(query)
    results = query_job.result()

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

    return HTMLResponse(table_html)

@app.post("/trigger_dag", response_class=HTMLResponse)
async def trigger_dag():
    composer_env_name = "your-composer-environment-name"
    composer_location = "your-composer-location"
    dag_name = "your-dag-name"
    api_version = "v1"
    project_id = "your-gcp-project-id"
    gcp_token = "your-gcp-auth-token"

    url = f"https://composer.googleapis.com/{api_version}/projects/{project_id}/locations/{composer_location}/environments/{composer_env_name}:triggerDag"
    headers = {
        "Authorization": f"Bearer {gcp_token}",
        "Content-Type": "application/json"
    }
    data = {
        "dagName": dag_name
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return HTMLResponse("DAG triggered successfully")
    else:
        return HTMLResponse(f"Failed to trigger DAG: {response.text}", status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
