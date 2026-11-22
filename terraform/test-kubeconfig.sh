#!/usr/bin/env bash
set -u
KC="${1:-./terraform-kubeconfig}"
NS="${NS:-streamlit-terraform}"
IMAGE="${IMAGE:-shaikhdocker/devops-agent:v7.0}"

echo "======Permissions for the terraform-deployer ServiceAccount======="


[ -s "$KC" ] || { echo "FAIL: $KC not found or empty"; exit 1; }
echo "File mode: $(stat -f '%Lp' "$KC") (should be 600)"
# Mac-side checks: swap host.docker.internal for the local API port
PORT="$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}' | sed 's#.*:##')"
LOCAL="https://127.0.0.1:${PORT}"
K="kubectl --kubeconfig $KC --server $LOCAL"
echo "Server in file: $(kubectl --kubeconfig "$KC" config view --minify -o jsonpath='{.clusters[0].cluster.server}')"
echo "Mac-side check uses: $LOCAL"

echo; echo "== Who am I =="
$K auth whoami 2>/dev/null || echo "(auth whoami not supported by this kubectl)"

echo; echo "== API reachable: list deployments in $NS =="
$K -n "$NS" get deploy && echo "OK" || echo "FAIL"

echo; echo "== Permissions in $NS =="
for v in "create deployments" "create services" "create configmaps" "delete deployments"; do
  printf '%-28s' "$v:"; $K -n "$NS" auth can-i $v
done
echo; echo "== Permission to create namespace in the cluster =="
printf '%-32s' "Create Namespaces:"; $K  auth can-i create namespaces 2>/dev/null

echo; echo "== Outside $NS =="
for v in "create services" "create configmaps" "create deployments -n default" "get secrets"; do
  printf '%-32s' "$v:"; $K -n "$NS" auth can-i $v
done

echo; echo "== From a container using the file as-is ($IMAGE) =="
docker run --rm --entrypoint kubectl \
  -v "$(cd "$(dirname "$KC")" && pwd)/$(basename "$KC"):/kube/config:ro" \
  -e KUBECONFIG=/kube/config "$IMAGE" -n "$NS" auth can-i create deployments \
  && echo "OK: reachable from a container" \
  || echo "FAIL: not reachable (check server host:port, tls-server-name, or that kubectl exists in the image)"
echo "======End of Permissions check for the terraform-deployer ServiceAccount======="
