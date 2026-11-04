set -eu
umask 077

KUBEFILE="$HOME/.kube/jenkins-terraform/config"
CAFILE="$HOME/.kube/jenkins-terraform/ca.crt"

mkdir -p "$HOME/.kube/jenkins-terraform"

# Make sure the CA certificate already exists
test -s "$CAFILE"

# Back up the existing custom file, if present
if [ -f "$KUBEFILE" ]; then
    cp "$KUBEFILE" "${KUBEFILE}.backup"
fi

# Generate a new isolated kubeconfig
TMPFILE=$(mktemp "$HOME/.kube/jenkins-terraform/config.XXXXXX")

# Obtain a temporary ServiceAccount token
SA_TOKEN=$(kubectl create token terraform-deployer \
  -n streamlit-terraform \
  --duration=24h)

# Configure Kubernetes API endpoint and TLS verification
kubectl config --kubeconfig="$TMPFILE" \
  set-cluster docker-desktop \
  --server=https://host.docker.internal:6443 \
  --certificate-authority="$CAFILE" \
  --embed-certs=true \
  --tls-server-name=kubernetes.default.svc

# Configure ServiceAccount authentication
kubectl config --kubeconfig="$TMPFILE" \
  set-credentials terraform-deployer \
  --token="$SA_TOKEN"

# Associate cluster and ServiceAccount
kubectl config --kubeconfig="$TMPFILE" \
  set-context terraform-context \
  --cluster=docker-desktop \
  --user=terraform-deployer \
  --namespace=streamlit-terraform

# Select the new context
kubectl config --kubeconfig="$TMPFILE" \
  use-context terraform-context

chmod 600 "$TMPFILE"
mv "$TMPFILE" "$KUBEFILE"
unset SA_TOKEN