#!/usr/bin/env bash
set -eu
set +x
umask 077

# ---- Settings (override with environment variables) ----
KCTX="${KCTX:-docker-desktop}"                       # admin context used for bootstrap
RBAC_FILE="${RBAC_FILE:-./jenkins-rbac-serviceaccount.yaml}"
NAMESPACE_FILE="${NAMESPACE_FILE:-./terraform-namespace.yaml}"
SA="terraform-deployer"
SA_NS="terraform-system"
APP_NS="${APP_NS:-streamlit-terraform}"
DURATION="${DURATION:-240h}"
OUT="${OUT:-./terraform-kubeconfig}"
BOOTSTRAP_OUT="${BOOTSTRAP_OUT:-./bootstrap-kubeconfig}"

k() { kubectl --context "$KCTX" "$@"; }

# ---- Pre-flight checks ----
for f in "$RBAC_FILE" "$NAMESPACE_FILE"; do
  [ -s "$f" ] || { echo "Missing $f" >&2; exit 1; }
done
k cluster-info >/dev/null 2>&1 || { echo "Cannot reach cluster with context '$KCTX'" >&2; exit 1; }
echo "Using context: $KCTX"

TMPS=()
cleanup() { rm -f "${TMPS[@]}" 2>/dev/null || true; }
trap cleanup EXIT

API_SERVER="$(k config view --minify -o jsonpath='{.clusters[0].cluster.server}')"
API_PORT="${API_SERVER##*:}"
SERVER="${SERVER:-https://host.docker.internal:${API_PORT}}"

backup_if_exists() {
  if [ -f "$1" ]; then cp -p "$1" "$1.backup.$(date +%Y%m%d-%H%M%S)"; fi
}

# ---- 1. Bootstrap (admin) kubeconfig for Jenkins ----
BTMP="$(mktemp ./bootstrap.XXXXXX)"; TMPS+=("$BTMP")
k config view --raw --minify --flatten > "$BTMP"
CLUSTER_NAME="$(kubectl --kubeconfig "$BTMP" config view --minify -o jsonpath='{.clusters[0].name}')"
kubectl config --kubeconfig="$BTMP" set-cluster "$CLUSTER_NAME" \
  --server="$SERVER" --tls-server-name=kubernetes.default.svc
chmod 600 "$BTMP"
backup_if_exists "$BOOTSTRAP_OUT"
mv "$BTMP" "$BOOTSTRAP_OUT"
echo "Created $BOOTSTRAP_OUT (ADMIN kubeconfig, server $SERVER)"

# ---- 2. Permanent namespaces, ServiceAccount and RBAC ----
k apply -f "$RBAC_FILE"
k apply -f "$NAMESPACE_FILE"

# ---- 3. Cluster CA for the ServiceAccount kubeconfig ----
CA_TMP="$(mktemp)"; TMPS+=("$CA_TMP")
k config view --raw --minify \
  -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' | base64 -d > "$CA_TMP"
[ -s "$CA_TMP" ] || { echo "Could not read cluster CA" >&2; exit 1; }

# ---- 4. ServiceAccount token and kubeconfig ----
TOKEN="$(k create token "$SA" -n "$SA_NS" --duration="$DURATION")"
TMP="$(mktemp ./kubeconfig.XXXXXX)"; TMPS+=("$TMP")
kubectl config --kubeconfig="$TMP" set-cluster docker-desktop \
  --server="$SERVER" --certificate-authority="$CA_TMP" --embed-certs=true \
  --tls-server-name=kubernetes.default.svc
kubectl config --kubeconfig="$TMP" set-credentials "$SA" --token="$TOKEN"
kubectl config --kubeconfig="$TMP" set-context terraform-context \
  --cluster=docker-desktop --user="$SA" --namespace="$APP_NS"
kubectl config --kubeconfig="$TMP" use-context terraform-context
chmod 600 "$TMP"
backup_if_exists "$OUT"
mv "$TMP" "$OUT"
unset TOKEN

echo "Created $OUT (ServiceAccount token valid for $DURATION)"
echo "Test: ./test-kubeconfig.sh $OUT"
