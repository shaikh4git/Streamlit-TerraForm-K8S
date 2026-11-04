
output "namespace" {
  description = "Kubernetes namespace"
  value       = var.namespace
}

output "namespace_managed_by_terraform" {
  description = "Whether Terraform manages namespace creation"
  value       = var.create_namespace
}

output "deployment_name" {
  description = "Streamlit Deployment name"
  value       = kubernetes_deployment_v1.streamlit.metadata[0].name
}

output "service_name" {
  description = "Streamlit Service name"
  value       = kubernetes_service_v1.streamlit.metadata[0].name
}

/*output "service_url" {
  description = "Internal Kubernetes Service URL"
  value       = "http://${kubernetes_service_v1.streamlit.metadata[0].name}.${var.namespace}.svc.cluster.local"
  
} */

output "deployed_image" {
  description = "Streamlit Docker image"
  value       = "${var.image_repo}:${var.image_tag}"
}
