
# Keep generated credentials out of Git
umask 077
mkdir -p "$HOME/.kube/jenkins-terraform"

KUBEFILE="$HOME/.kube/jenkins-terraform/config"

# Read the Kubernetes API URL
API_SERVER=$(kubectl config view --minify \
  -o jsonpath='{.clusters[0].cluster.server}')

# Extract the cluster CA certificate
kubectl config view --raw --minify \
  -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' \
  | base64 -D \
  > "$HOME/.kube/jenkins-terraform/ca.crt"

# Request a temporary ServiceAccount token
SA_TOKEN=$(kubectl create token terraform-deployer \
  -n streamlit-terraform \
  --duration=24h)

# Configure Kubernetes cluster
kubectl config --kubeconfig="$KUBEFILE" \
  set-cluster docker-desktop \
  --server="$API_SERVER" \
  --certificate-authority="$HOME/.kube/jenkins-terraform/ca.crt" \
  --embed-certs=true

# Configure ServiceAccount credentials
kubectl config --kubeconfig="$KUBEFILE" \
  set-credentials terraform-deployer \
  --token="$SA_TOKEN"

# Configure context
kubectl config --kubeconfig="$KUBEFILE" \
  set-context terraform-context \
  --cluster=docker-desktop \
  --user=terraform-deployer \
  --namespace=streamlit-terraform

# Select context
kubectl config --kubeconfig="$KUBEFILE" \
  use-context terraform-context

# Restrict file permissions
chmod 600 "$KUBEFILE"

unset SA_TOKEN
