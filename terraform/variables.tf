

variable "kubeconfig_path" {
  description = "Path to the Kubernetes kubeconfig"
  type        = string
  sensitive   = true
}

variable "image_repo" {
  description = "Docker Hub image repository"
  type        = string
  default     = "shaikhdocker/sshuda-streamlit-app"
}

variable "image_tag" {
  description = "Docker image tag to deploy"
  type        = string
}

variable "replicas" {
  description = "Number of Streamlit replicas"
  type        = number
  default     = 2
}
