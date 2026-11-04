
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 3.4.0, < 4.0.0"
    }
  }
}

# Jenkins provides the kubeconfig path.
# If omitted, the provider reads KUBE_CONFIG_PATH.
/*
provider "kubernetes" {
  config_path = var.kubeconfig_path != "" ? var.kubeconfig_path : null
} */

provider "kubernetes" {}

# ----------------------------------------
# Conditional Kubernetes Namespace
# ----------------------------------------

resource "kubernetes_namespace_v1" "streamlit" {
  count = var.create_namespace ? 1 : 0

  metadata {
    name = var.namespace

    labels = {
      "app.kubernetes.io/managed-by" = "terraform"
    }
  }

  lifecycle {
    prevent_destroy = true
  }
}

# ----------------------------------------
# Streamlit Deployment
# ----------------------------------------

resource "kubernetes_deployment_v1" "streamlit" {

  metadata {
    name      = "streamlit-deploy"
    namespace = var.namespace

    labels = {
      app = "streamlit"
    }
  }

  spec {
    replicas               = var.replicas
    revision_history_limit = 3

    strategy {
      type = "RollingUpdate"

      rolling_update {
        max_surge       = "1"
        max_unavailable = "0"
      }
    }

    selector {
      match_labels = {
        app = "streamlit"
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
          name              = "streamlit"
          image             = "${var.image_repo}:${var.image_tag}"
          image_pull_policy = "IfNotPresent"

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
            timeout_seconds       = 1
            failure_threshold     = 3
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

  depends_on = [
    kubernetes_namespace_v1.streamlit
  ]
}

# ----------------------------------------
# Streamlit ClusterIP Service
# ----------------------------------------

resource "kubernetes_service_v1" "streamlit" {

  metadata {
    name      = "streamlit-service"
    namespace = var.namespace

    labels = {
      app = "streamlit"
    }
  }

  spec {
    selector = {
      app = "streamlit"
    }

    port {
      port        = 80
      target_port = 8501
    }

    type = "ClusterIP"
  }

  depends_on = [
    kubernetes_namespace_v1.streamlit
  ]
}
