from google.cloud import bigquery

def location_to_bq(event, context):
    # Construct a BigQuery client object.
    client = bigquery.Client()

    table_id = "felyx-assignement.INTEGRATION_IN.location"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("row", "INTEGER"),
            bigquery.SchemaField("id", "STRING"),
            bigquery.SchemaField("wgs84_polygon", "STRING"),
        ],
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )

    file_name = event["name"]
    bucket_name = event["bucket"]
    uri = "gs://{}/{}".format(bucket_name, file_name)

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)  # Make an API request.
    print("Loaded {} rows.".format(destination_table.num_rows))