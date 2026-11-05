
variable "kubeconfig_path" {
  description = "Path to Jenkins kubeconfig Secret file"
  type        = string
  sensitive   = true
  default     = ""
}

variable "namespace" {
  description = "Streamlit Kubernetes namespace"
  type        = string
  default     = "terraform-system"
}

variable "create_namespace" {
  description = "Whether Terraform should create the namespace"
  type        = bool
  default     = false
}

variable "image_repo" {
  description = "Docker Hub image repository"
  type        = string
  default     = "shaikhdocker/sshuda-streamlit-app"
}

variable "image_tag" {
  description = "Docker image tag passed by Jenkins"
  type        = string
}

variable "replicas" {
  description = "Number of Streamlit replicas"
  type        = number
  default     = 10

  validation {
    condition     = var.replicas >= 1 && floor(var.replicas) == var.replicas
    error_message = "replicas must be a positive whole number."
  }
}
