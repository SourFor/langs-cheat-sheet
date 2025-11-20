helm repo add apache-airflow https://airflow.apache.org

helm repo update

helm pull apache-airflow/airflow --untar

helm package airflow

helm login <private_registry_url> -u <username>

helm push airflow-1.18.0.tgz oci://<private_registry_url>/path/to/helm/charts

helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace