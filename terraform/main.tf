
terraform {
  required_version = ">= 1.9.0"

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 3.0"
    }
  }
}

# Kubernetes provider configuration
provider "kubernetes" {
  config_path = var.kubeconfig_path
}

# Namespace
resource "kubernetes_namespace_v1" "streamlit" {
  metadata {
    name = "streamlit-terraform"
  }
}

# Streamlit Deployment
resource "kubernetes_deployment_v1" "streamlit" {
  metadata {
    name      = "streamlit"
    namespace = kubernetes_namespace_v1.streamlit.metadata[0].name
    labels = {
      app = "streamlit"
    }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = "streamlit"
      }
    }

    strategy {
      type = "RollingUpdate"

      rolling_update {
        max_surge       = "1"
        max_unavailable = "0"
      }
    }

    template {
      metadata {
        labels = {
          app = "streamlit"
        }
      }

      spec {
        container {
          name  = "streamlit"
          image = "${var.image_repo}:${var.image_tag}"

          image_pull_policy = "Always"

          port {
            container_port = 8501
          }

          readiness_probe {
            http_get {
              path = "/_stcore/health"
              port = 8501
            }
            initial_delay_seconds = 5
            period_seconds        = 10
          }

          resources {
            requests = {
              cpu    = "50m"
              memory = "64Mi"
            }

            limits = {
              cpu    = "250m"
              memory = "256Mi"
            }
          }
        }
      }
    }
  }

  wait_for_rollout = true
}

# ClusterIP Service
resource "kubernetes_service_v1" "streamlit" {
  metadata {
    name      = "streamlit-service"
    namespace = kubernetes_namespace_v1.streamlit.metadata[0].name
  }

  spec {
    selector = {
      app = "streamlit"
    }

    port {
      port        = 80
      target_port = 8501
      protocol    = "TCP"
    }

    type = "ClusterIP"
  }
}
