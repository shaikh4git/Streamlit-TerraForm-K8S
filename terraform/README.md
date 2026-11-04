## How to set jenkins container to let terraform deploy streamlit applciation via service account on Docker Desktop Kubernetes

A namespace-scoped ServiceAccount cannot normally create namespaces, because namespaces are cluster-scoped resources.


kubectl create namespace streamlit-terraform

namespace/streamlit-terraform created
shaikh@Shaikhs-MacBook-Pro-2 Streamlit-Repo % kubectl create serviceaccount terraform-deployer \
  -n streamlit-terraform
serviceaccount/terraform-deployer created


Two options:
- Option A (recommended): Create the namespace once using kubectl, remove the namespace resource from Terraform, and use namespace-scoped RBAC for the Terraform deployer.
- Option B: Grant Terraform additional cluster-scoped namespace permissions if Terraform must provision namespaces.


- Namespace: streamlit-terraform
- ServiceAccount: terraform-deployer
we can proceed with configuring Kubernetes RBAC, generating the kubeconfig, and connecting it to your Jenkins Docker agent.

We'll do this in five steps:
1. Create a Kubernetes Role defining what Terraform can manage. :: terraform-role.yaml:
2. Create a RoleBinding granting those permissions to terraform-deployer. :: terraform-rolebinding.yaml
3. Generate a ServiceAccount authentication token and kubeconfig. :: # kubectl create token terraform-deployer \
  -n streamlit-terraform \
  --duration=24h
4. Store that kubeconfig securely in Jenkins Credentials.
5. Test access from Jenkins before executing terraform apply.


The Role allows Terraform to manage Deployments and Services only inside streamlit-terraform.

Notice that we're not granting permissions to create namespaces, because you've already created yours.

Role-binding yaml establishes the authorization relationship:
ServiceAccount. ==> terraform-deployer

Authentication identity
RoleBinding ==> terraform-deployer-binding

Role ==> terraform-deployer-role

Kubernetes API server enforces these permissions:

Verify the permissions
Run:
kubectl auth can-i create deployments \
  -n streamlit-terraform \
  --as=system:serviceaccount:streamlit-terraform:terraform-deployer


And:
kubectl auth can-i update services \
  -n streamlit-terraform \
  --as=system:serviceaccount:streamlit-terraform:terraform-deployer


Both should return:
yes


Also test that it cannot create namespaces:
kubectl auth can-i create namespaces \
  --as=system:serviceaccount:streamlit-terraform:terraform-deployer

Expected:
no


A. Identify your Docker Desktop Kubernetes API server
Run:
kubectl config view --minify \
  -o jsonpath='{.clusters[0].cluster.server}{"\n"}'


You might see:
https://127.0.0.1:6443



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



This creates the credential file:
~/.kube/jenkins-terraform/config


The generated kubeconfig embeds your cluster's CA certificate and the ServiceAccount token.

This example assumes your existing kubeconfig has embedded CA data and uses macOS's base64 -D. If that field is empty, the current cluster configuration may reference a certificate file instead.
D. Test it locally
KUBECONFIG="$HOME/.kube/jenkins-terraform/config" \
  kubectl get deployments -n streamlit-terraform


If you have no Deployments yet, this is perfectly normal:
No resources found in streamlit-terraform namespace.


That is still a successful authentication and authorization test.

Now test that the ServiceAccount cannot access unrelated resources:
KUBECONFIG="$HOME/.kube/jenkins-terraform/config" \
  kubectl get secrets -n streamlit-terraform


Assuming no other RBAC permissions were granted, Kubernetes should return Forbidden.
Step 4 — Handle Docker Desktop networking
Before uploading the kubeconfig to Jenkins, test how a Docker container reaches the Kubernetes API.

For example:
docker run --rm curlimages/curl \
  -k -I https://host.docker.internal:6443


This is only a network connectivity diagnostic, not an authentication test. Here, -k temporarily skips TLS verification, so don't use it in your final Jenkins deployment configuration.

A Kubernetes API response such as HTTP 401 or 403 means the server is reachable. A connection-refused or timeout error means the endpoint is not working.

For Jenkins, use an address that its agent containers can reach and that passes certificate verification. If host.docker.internal is reachable but not covered by your API certificate, you must use an appropriate DNS name or certificate configuration; don't permanently disable TLS verification.

Once you have confirmed a working endpoint, update the generated kubeconfig's server URL if necessary:
kubectl config \
  --kubeconfig="$HOME/.kube/jenkins-terraform/config" \
  set-cluster docker-desktop \
  --server="https://YOUR-VERIFIED-API-ENDPOINT:6443"


Replace YOUR-VERIFIED-API-ENDPOINT with the tested address.
Step 5 — Upload the kubeconfig to Jenkins
Open:

Jenkins → Manage Jenkins → Credentials → System → Global credentials → Add Credentials

Configure:
Field	Value
Kind	Secret file
File	~/.kube/jenkins-terraform/config
ID	kubeconfig-dockerdesktop
Description	Kubernetes Terraform ServiceAccount
Scope	Global

In the upload dialog, browse to the actual file on your MacBook. The ~ path above is shorthand for your home directory.

Click Create.

Now Jenkins stores the kubeconfig securely and makes it available to pipelines referencing kubeconfig-dockerdesktop.
Step 6 — Test the credential from your Jenkins agent
Before executing Terraform, add this temporary verification stage to your Jenkinsfile:

stage('Verify Kubernetes Access') {
    steps {
        withCredentials([
            file(
                credentialsId: 'kubeconfig-dockerdesktop',
                variable: 'KUBE_CONFIG_FILE'
            )
        ]) {
            sh '''
                set -eu

                export KUBECONFIG="$KUBE_CONFIG_FILE"
                export KUBE_CONFIG_PATH="$KUBE_CONFIG_FILE"

                echo "===== Kubernetes API Connectivity ====="
                kubectl cluster-info

                echo "===== Current Identity ====="
                kubectl auth whoami

                echo "===== Deployment Permission ====="
                kubectl auth can-i create deployments \
                  -n streamlit-terraform

                echo "===== Service Permission ====="
                kubectl auth can-i create services \
                  -n streamlit-terraform

                echo "===== Available Deployments ====="
                kubectl get deployments \
                  -n streamlit-terraform
            '''
        }
    }
}



The expected Kubernetes identity is:
system:serviceaccount:streamlit-terraform:terraform-deployer


If kubectl auth whoami is unsupported by your installed client, the permission checks and kubectl get still help verify access.

If Jenkins reports connection refused, x509 certificate errors, Unauthorized, or Forbidden, troubleshoot the network, certificate, token, or RBAC respectively.
Step 7 — Update your Terraform configuration
Since you've already created streamlit-terraform, remove the kubernetes_namespace_v1 resource from your earlier Terraform configuration.

Instead, reference the existing namespace directly:
resource "kubernetes_deployment_v1" "streamlit" {
  metadata {
    name      = "streamlit-deploy"
    namespace = "streamlit-terraform"
  }

  # Existing deployment configuration...
}


Do the same for the Service.

Your provider.tf can remain:
provider "kubernetes" {
  # Reads KUBE_CONFIG_PATH from Jenkins
}


The Kubernetes Terraform provider supports KUBE_CONFIG_PATH, allowing your Jenkins Secret file credential to supply the authentication configuration. 
Terraform Registry

Important considerations before production use
Token expiration: The token generated with --duration=24h is intended for initial testing. It will expire, and Jenkins builds will stop authenticating unless the token is renewed and the credential updated. For ongoing CI/CD, use an automated short-lived token delivery mechanism or another supported rotating authentication method. Avoid permanent ServiceAccount tokens where possible.

Persistent Terraform state: Because your Jenkins Docker agent is temporary and gets removed after pipelines, you need persistent Terraform state storage. Your existing AWS S3 backend is a suitable option, with a dedicated state key for this Streamlit deployment.

Security: Keep the kubeconfig out of GitHub and Docker images. Restrict Jenkins credential access to authorized jobs.

Final architecture
Jenkins Pipeline

Terraform plan and apply


Jenkins Secret File Credential

kubeconfig-dockerdesktop


ServiceAccount

terraform-deployer


Kubernetes RBAC

Role + RoleBinding


Kubernetes API Server

HTTPS + Authentication + Authorization


Streamlit Deployment and Service

Namespace: streamlit-terraform