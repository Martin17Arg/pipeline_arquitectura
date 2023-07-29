import os
from google.cloud import bigquery

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/martin/.config/gcloud/application_default_credentials.json"

client = bigquery.Client()

query = """
	SELECT SUM(pr_antiguedad_prestamos) AS Suma
	, MAX(pr_antiguedad_prestamos) AS Max
	, MIN(pr_antiguedad_prestamos) AS Min
	, COUNT(pr_antiguedad_prestamos) AS Count
	FROM post_stage.measure_pr_antiguedad_prestamos
	"""

results = client.query(query).result()

campo = "Count"

for row in results:
	print(row[campo])
	#print(row.value)
