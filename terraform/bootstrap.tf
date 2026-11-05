
resource "kubernetes_service_account_v1" "terraform_deployer" {
  metadata {
    name      = "terraform-deployer"
    namespace = var.namespace
  }

  depends_on = [kubernetes_namespace_v1.streamlit]
}

resource "kubernetes_role_v1" "terraform_deployer" {
  metadata {
    name      = "terraform-deployer-role"
    namespace = var.namespace
  }

  rule {
    api_groups = ["apps"]
    resources  = ["deployments"]
    verbs = [
      "get", "list", "watch",
      "create", "update", "patch", "delete"
    ]
  }

  rule {
    api_groups = [""]
    resources  = ["services"]
    verbs = [
      "get", "list", "watch",
      "create", "update", "patch", "delete"
    ]
  }

  depends_on = [kubernetes_namespace_v1.streamlit]
}

resource "kubernetes_role_binding_v1" "terraform_deployer" {
  metadata {
    name      = "terraform-deployer-binding"
    namespace = var.namespace
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Role"
    name      = kubernetes_role_v1.terraform_deployer.metadata[0].name
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account_v1.terraform_deployer.metadata[0].name
    namespace = var.namespace
  }
}
