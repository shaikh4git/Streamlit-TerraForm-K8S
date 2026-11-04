
variable "kubeconfig_path" {
  description = "Kubernetes kubeconfig file path"
  type        = string
  default     = "~/.kube/config"
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
