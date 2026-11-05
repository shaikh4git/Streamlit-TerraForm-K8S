
#!/usr/bin/env bash
set -euo pipefail
set +x
umask 077

: "${BOOTSTRAP_KUBECONFIG:?Missing bootstrap kubeconfig}"

NAMESPACE="terraform-system"
SA_NAME="terraform-deployer"
OUTPUT="${1:?Provide output kubeconfig path}"

mkdir -p "$(dirname "$OUTPUT")"

echo "Requesting fresh ServiceAccount token..."

TOKEN="$(
  kubectl \
    --kubeconfig="$BOOTSTRAP_KUBECONFIG" \
    create token "$SA_NAME" \
    -n "$NAMESPACE" \
    --duration=30m
)"

echo "Extracting Kubernetes CA..."

CA_DATA="$(
  kubectl \
    --kubeconfig="$BOOTSTRAP_KUBECONFIG" \
    config view --raw --minify \
    -o jsonpath='{.clusters[0].cluster.certificate-authority-data}'
)"

test -n "$CA_DATA"
test -n "$TOKEN"

# Generate standalone ServiceAccount kubeconfig.
# No administrator credentials are copied to this file.

cat > "$OUTPUT" <<EOF
apiVersion: v1
kind: Config
clusters:
- name: docker-desktop
  cluster:
    server: https://host.docker.internal:6443
    certificate-authority-data: ${CA_DATA}
    tls-server-name: kubernetes.default.svc
users:
- name: terraform-deployer
  user:
    token: ${TOKEN}
contexts:
- name: terraform-context
  context:
    cluster: docker-desktop
    user: terraform-deployer
    namespace: streamlit-terraform
current-context: terraform-context
EOF

unset TOKEN CA_DATA

chmod 600 "$OUTPUT"

echo "Verifying generated ServiceAccount kubeconfig..."

kubectl --kubeconfig="$OUTPUT" auth whoami

echo "Checking deployment permission..."

RESULT="$(
  kubectl --kubeconfig="$OUTPUT" \
    auth can-i create deployments \
    -n streamlit-terraform
)"

if [[ "$RESULT" != "yes" ]]; then
    echo "ERROR: ServiceAccount lacks deployment permissions."
    exit 1
fi

echo "ServiceAccount authentication verified."
