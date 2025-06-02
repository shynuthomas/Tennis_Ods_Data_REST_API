import functions_framework
import requests
from google.cloud import bigquery
import os
import json
from datetime import datetime

API_ENDPOINT = "https://jsonplaceholder.typicode.com/posts"

@functions_framework.http
def ingest_posts(request):
    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        posts = response.json()

        # Add additional columns to each post
        enriched_posts = []
        for post in posts:
            post['source_name'] = "jsonplaceholder"
            post['created_time'] = datetime.utcnow().isoformat()
            enriched_posts.append(post)

        # Ingest to BigQuery
        client = bigquery.Client()
        table_id = "spartan-buckeye-459010-i0.pinnacle_tennis.tennis_event"
        errors = client.insert_rows_json(table_id, enriched_posts)

        if errors:
            raise RuntimeError(errors)

        return json.dumps({"status": "success", "rows_ingested": len(enriched_posts)}), 200
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}), 500
