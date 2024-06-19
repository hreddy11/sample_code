import json
from flask import Blueprint, request, render_template, jsonify
from airflow.models import DagRun
from airflow.utils.state import State
from airflow import settings
from airflow.api.common.experimental.trigger_dag import trigger_dag

my_plugin_bp = Blueprint("my_plugin_bp", __name__, template_folder='templates', static_folder='static', static_url_path='/static/my_plugin')

@my_plugin_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@my_plugin_bp.route("/fetch_week_info", methods=["POST"])
def fetch_week_info():
    table = request.form.get("table")
    session = settings.Session()

    # Get the last run time of the specified DAG
    last_run = session.query(DagRun).filter(DagRun.dag_id == table).order_by(DagRun.execution_date.desc()).first()
    last_run_time = last_run.execution_date if last_run else "No previous runs"

    # Trigger the specified DAG
    dag_run = trigger_dag(dag_id=table, run_id=f"manual__{time.strftime('%Y-%m-%dT%H:%M:%S')}")
    current_time = dag_run.execution_date
    status = dag_run.state

    return jsonify({
        "last_run_time": last_run_time,
        "current_time": current_time,
        "status": status
    })
