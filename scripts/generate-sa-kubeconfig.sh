#!/usr/bin/env bash
set -euo pipefail
set +x
umask 077

: "${BOOTSTRAP_KUBECONFIG:?Missing bootstrap kubeconfig}"
OUT="${1:?Usage: generate-sa-kubeconfig.sh <output-path>}"

SA="${SA_NAME:-terraform-deployer}"
SA_NS="${SA_NAMESPACE:-terraform-system}"
APP_NS="${APP_NAMESPACE:-streamlit-terraform}"
DURATION="${TOKEN_DURATION:-1h}"

BK() { kubectl --kubeconfig="$BOOTSTRAP_KUBECONFIG" "$@"; }

# Reuse the address and TLS name that the bootstrap kubeconfig already uses
SERVER="$(BK config view --minify -o jsonpath='{.clusters[0].cluster.server}')"
TLS_NAME="$(BK config view --minify -o jsonpath='{.clusters[0].cluster.tls-server-name}')"
TLS_NAME="${TLS_NAME:-kubernetes.default.svc}"
echo "Using server: $SERVER (tls-server-name: $TLS_NAME)"

echo "Requesting fresh ServiceAccount token..."
TOKEN="$(BK -n "$SA_NS" create token "$SA" --duration="$DURATION")"
[ -n "$TOKEN" ] || { echo "Empty token" >&2; exit 1; }

echo "Extracting Kubernetes CA..."
CA_FILE="$(mktemp)"
trap 'rm -f "$CA_FILE"' EXIT
BK config view --raw --minify -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' | base64 -d > "$CA_FILE"
[ -s "$CA_FILE" ] || { echo "Could not read cluster CA" >&2; exit 1; }

mkdir -p "$(dirname "$OUT")"
rm -f "$OUT"
kubectl config --kubeconfig="$OUT" set-cluster docker-desktop \
  --server="$SERVER" --certificate-authority="$CA_FILE" --embed-certs=true \
  --tls-server-name="$TLS_NAME" >/dev/null
kubectl config --kubeconfig="$OUT" set-credentials "$SA" --token="$TOKEN" >/dev/null
kubectl config --kubeconfig="$OUT" set-context terraform-context \
  --cluster=docker-desktop --user="$SA" --namespace="$APP_NS" >/dev/null
kubectl config --kubeconfig="$OUT" use-context terraform-context >/dev/null
chmod 600 "$OUT"
unset TOKEN

echo "Verifying generated ServiceAccount kubeconfig..."
kubectl --kubeconfig="$OUT" -n "$APP_NS" auth can-i create deployments
