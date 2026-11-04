
output "namespace" {
  description = "Namespace where Streamlit is deployed"
  value       = "streamlit-terraform"
}

output "deployment_name" {
  description = "Name of the Streamlit Deployment"
  value       = kubernetes_deployment_v1.streamlit.metadata[0].name
}

output "service_name" {
  description = "Name of the Streamlit Service"
  value       = kubernetes_service_v1.streamlit.metadata[0].name
}

output "service_url" {
  description = "Internal Kubernetes Service URL"
  value       = "http://${kubernetes_service_v1.streamlit.metadata[0].name}.streamlit-terraform.svc.cluster.local:8501"
}
