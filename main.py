import functions_framework
import requests
from google.cloud import bigquery
import os
import json

API_ENDPOINT = "https://jsonplaceholder.typicode.com/posts"

@functions_framework.http
def ingest_posts(request):
    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        posts = response.json()

        # Ingest to BigQuery
        project_id = os.getenv("GCP_PROJECT")
        client = bigquery.Client()
        table_id = "spartan-buckeye-459010-i0.pinnacle_tennis.testfunction"
        errors = client.insert_rows_json(table_id, posts)

        if errors:
            raise RuntimeError(errors)

        return json.dumps({"status": "success", "rows_ingested": len(posts)}), 200
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}), 500