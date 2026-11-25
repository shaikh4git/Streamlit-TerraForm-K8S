import streamlit as st
from utils.image_utils import show_image, image_path, list_images

def render():

    st.title(
        "🚀 Project 2: Enterprise DevSecOps & "
        "Terraform-Based Kubernetes Deployment Platform"
    )

    st.markdown("""
    **End-to-end CI/CD | DevSecOps | Infrastructure as Code |
    Kubernetes Deployment Automation**

    Designed and implemented an automated deployment platform
    for a containerized Streamlit application using Jenkins,
    Ansible, Docker, Terraform and Kubernetes.
    """)

    st.divider()

    # --------------------------------------------------
    # PROJECT OVERVIEW
    # --------------------------------------------------

    st.header("📌 1. Project Overview")

    st.markdown("""
    The objective of this project is to implement an end-to-end
    software delivery workflow that automates application
    validation, security scanning, container image creation,
    staging deployment and Kubernetes infrastructure management.

    Jenkins orchestrates the complete CI/CD workflow.

    Ansible deploys the application to Docker Desktop staging.

    Terraform provisions and manages Kubernetes resources,
    including the application Deployment and Service.

    The pipeline also verifies the actual running image,
    Kubernetes rollout status and application resources.
    """)

    st.markdown("### Key Engineering Objectives")

    objectives = [
        "Automate application build and deployment using Jenkins.",
        "Integrate DevSecOps security scanning into CI/CD.",
        "Validate application functionality through unit testing.",
        "Enforce code quality through SonarQube Quality Gate.",
        "Build and version Docker images using Docker Buildx.",
        "Automate staging deployment using Ansible.",
        "Manage Kubernetes infrastructure using Terraform.",
        "Generate dedicated Kubernetes ServiceAccount credentials.",
        "Import existing Kubernetes resources into Terraform state.",
        "Verify the deployed application and running container image."
    ]

    for objective in objectives:
        st.markdown(f"- {objective}")

    st.divider()

    # --------------------------------------------------
    # HIGH LEVEL ARCHITECTURE
    # --------------------------------------------------

    st.header("🏗️ 2. End-to-End System Architecture")

    show_image(
            "architecture",
            "DevSecOps.png",
            caption="FasApi backend Architecture",
        )
    st.caption(
        "Jenkins orchestrates the workflow. Ansible handles staging. "
        "Terraform manages Kubernetes resources and application deployment."
    )

    # --------------------------------------------------
    # REPOSITORY ARCHITECTURE
    # --------------------------------------------------

    st.header("📂 3. Source Code & Repository Architecture")

    tab1, tab2 = st.tabs([
        "Application & CI/CD Repository",
        "Kubernetes Infrastructure"
    ])

    with tab1:

        st.markdown("### Streamlit-Repo")

        st.code("""
Streamlit-Repo/
├── ansible/
│   ├── staging_blugren.yaml
│   ├── staging_canary.yaml
│   └── staging_std.yaml
├── app.py
├── Dockerfile
├── JenkinsBluegreen
├── JenkinsCanary
├── JenkinsSTD
├── requirements.txt
└── tests/
    └── test_app.py
""", language="text")

        st.markdown("""
        **Responsibilities**

        - Streamlit application source code.
        - Docker image creation.
        - Jenkins CI/CD pipeline definitions.
        - Ansible staging deployment playbooks.
        - Pytest application test cases.
        """)

    with tab2:

        st.markdown("### Terraform & Kubernetes")

        st.code("""
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── providers.tf
└── terraform.tfvars

k8s/
├── deployment.yaml
├── service.yaml
└── configmap.yaml

scripts/
└── generate-sa-kubeconfig.sh
""", language="text")

        st.markdown("""
        **Responsibilities**

        - Kubernetes provider configuration.
        - Deployment and Service resource management.
        - Terraform state management.
        - ServiceAccount authentication.
        - Existing-resource import.
        - Infrastructure outputs and deployment verification.

        Adjust the illustrative tree above to match the actual
        directories in your repository.
        """)

    st.divider()

    # --------------------------------------------------
    # JENKINS PIPELINE
    # --------------------------------------------------

    st.header("⚙️ 4. Jenkins CI/CD & DevSecOps Pipeline")

    st.markdown("""
    Jenkins is the central automation engine responsible for
    coordinating source checkout, security validation, testing,
    image creation, staging and Terraform deployment.
    """)

    pipeline_stages = [
        (
            "01. Workspace Cleanup",
            "Jenkins cleanWs() removes previous build artifacts "
            "to provide a clean execution environment."
        ),
        (
            "02. GitHub Checkout",
            "Checks out the source code and retrieves the Git commit "
            "and branch information. Generates a unique Docker image "
            "tag using the Jenkins build number and Git commit hash."
        ),
        (
            "03. Gitleaks Secret Scanning",
            "Scans Git repository history for accidentally committed "
            "credentials, API keys, tokens and other sensitive values."
        ),
        (
            "04. Pytest Unit Testing",
            "Executes automated unit tests against the Streamlit "
            "application to validate application functionality."
        ),
        (
            "05. SonarQube Code Analysis",
            "Performs static code analysis to identify code-quality "
            "issues, maintainability concerns and potential vulnerabilities."
        ),
        (
            "06. SonarQube Quality Gate",
            "Evaluates the SonarQube analysis against configured quality "
            "criteria. The pipeline proceeds only when the gate passes."
        ),
        (
            "07. Trivy Filesystem Scan",
            "Scans application files, dependencies and configuration "
            "for known vulnerabilities and security issues."
        ),
        (
            "08. Docker Buildx",
            "Builds the Streamlit Docker image using Docker Buildx and "
            "assigns a unique versioned tag."
        ),
        (
            "09. Trivy Image Scan",
            "Scans the generated container image for operating-system "
            "package and application dependency vulnerabilities."
        ),
        (
            "10. Docker Hub",
            "Publishes the validated container image to the configured "
            "Docker Hub repository."
        ),
        (
            "11. Ansible Staging Deployment",
            "Deploys the newly built image to Docker Desktop staging "
            "and validates the staging application."
        ),
        (
            "12. Terraform Kubernetes Deployment",
            "Authenticates to Kubernetes, imports existing resources "
            "when necessary, generates a Terraform plan and applies "
            "the infrastructure changes."
        ),
        (
            "13. Deployment Verification",
            "Checks Terraform outputs, Kubernetes rollout status, "
            "Deployment, Service, Pods and the actual running image."
        )
    ]

    for stage, description in pipeline_stages:
        with st.expander(stage):
            st.write(description)

    st.divider()

    # --------------------------------------------------
    # SECURITY
    # --------------------------------------------------

    st.header("🔐 5. DevSecOps Security Integration")

    security_data = [
        {
            "Tool": "Gitleaks",
            "Purpose": "Secret and credential detection",
            "Stage": "Source code"
        },
        {
            "Tool": "Pytest",
            "Purpose": "Automated application testing",
            "Stage": "Testing"
        },
        {
            "Tool": "SonarQube",
            "Purpose": "Static code quality and security analysis",
            "Stage": "Code analysis"
        },
        {
            "Tool": "Quality Gate",
            "Purpose": "Enforce configured quality criteria",
            "Stage": "Quality enforcement"
        },
        {
            "Tool": "Trivy FS",
            "Purpose": "Filesystem and dependency vulnerability scanning",
            "Stage": "Pre-build security"
        },
        {
            "Tool": "Trivy Image",
            "Purpose": "Container image vulnerability scanning",
            "Stage": "Container security"
        }
    ]

    st.table(security_data)

    st.markdown("""
    **Security objective:** Introduce security checks throughout
    the software delivery lifecycle instead of relying only on
    post-deployment vulnerability assessments.
    """)

    st.divider()

    # --------------------------------------------------
    # DOCKER AND ANSIBLE
    # --------------------------------------------------

    st.header("🐳 6. Docker Build & Ansible Staging")

    st.markdown("""
    After building the application image, Jenkins invokes Ansible
    to deploy the image into the Docker Desktop staging environment.
    """)

    st.code("""
ansible-playbook \\
    -i localhost, \\
    AppCode/ansible/staging_canary.yaml \\
    -e "image_repo=$IMAGE_REPO" \\
    -e "image_tag=$IMAGE_TAG"
""", language="bash")

    st.markdown("""
    **Ansible responsibilities**

    - Connect to the Docker Desktop staging environment.
    - Deploy the selected application image.
    - Configure the staging container.
    - Perform application health checks.
    - Validate the staging deployment before Terraform deployment.
    """)

    st.divider()

    # --------------------------------------------------
    # TERRAFORM
    # --------------------------------------------------

    st.header("🏗️ 7. Terraform Infrastructure as Code")

    st.markdown("""
    Terraform is responsible for managing Kubernetes infrastructure
    and deploying the Streamlit application into the Kubernetes cluster.

    Unlike a GitOps controller-based architecture, this implementation
    uses Jenkins to execute Terraform directly.
    """)

    terraform_stages = [
        (
            "A. Bootstrap Authentication",
            "Uses a securely stored bootstrap kubeconfig to authenticate "
            "to the Kubernetes API."
        ),
        (
            "B. ServiceAccount Kubeconfig",
            "Executes generate-sa-kubeconfig.sh to create a dedicated "
            "ServiceAccount kubeconfig for Terraform."
        ),
        (
            "C. Terraform Init and Validate",
            "Initializes Terraform providers and validates the "
            "infrastructure configuration."
        ),
        (
            "D. Existing Resource Import",
            "Checks Terraform state and Kubernetes resources. Imports "
            "existing Deployment and Service resources when they exist "
            "but are not yet managed by Terraform."
        ),
        (
            "E. Terraform Plan",
            "Generates a saved execution plan using the selected "
            "namespace and dynamically generated image tag."
        ),
        (
            "F. Terraform Apply",
            "Applies the saved plan to create or update Kubernetes "
            "resources."
        ),
        (
            "G. Deployment Verification",
            "Checks Terraform outputs, rollout status, running image, "
            "Kubernetes Service and application Pods."
        )
    ]

    for title, description in terraform_stages:
        with st.expander(title):
            st.write(description)

    st.markdown("### Kubernetes Deployment Details")

    st.code("""
Namespace:  streamlit-terraform

Deployment: streamlit-deploy

Service:    streamlit-service

Image:      shaikhdocker/sshuda-streamlit-app:<BUILD>-<COMMIT>
""", language="text")

    st.divider()

    # --------------------------------------------------
    # DEPLOYMENT STRATEGIES
    # --------------------------------------------------

    st.header("🔄 8. Deployment Strategies")

    st.markdown("""
    The project contains separate Jenkins pipelines and Ansible
    staging playbooks for three deployment approaches.
    """)

    strategy1, strategy2, strategy3 = st.tabs([
        "Standard",
        "Canary",
        "Blue-Green"
    ])

    with strategy1:

        st.subheader("Standard Rolling Deployment")

        st.markdown("""
        Uses the standard Kubernetes Deployment rollout mechanism
        to replace application Pods progressively.

        **Pipeline:** JenkinsSTD

        **Staging playbook:** staging_std.yaml

        **Objective:** Update the application while maintaining
        service availability during the rolling replacement.
        """)

    with strategy2:

        st.subheader("Canary Deployment")

        st.markdown("""
        Uses the canary deployment workflow to introduce a new
        application version alongside the existing version.

        **Pipeline:** JenkinsCanary

        **Staging playbook:** staging_canary.yaml

        **Objective:** Validate a new release progressively before
        wider adoption.

        Note: Describe traffic splitting or percentage-based
        rollout only if implemented in this pipeline.
        """)

    with strategy3:

        st.subheader("Blue-Green Deployment")

        st.markdown("""
        Uses separate blue and green application environments.

        **Pipeline:** JenkinsBluegreen

        **Staging playbook:** staging_blugren.yaml

        **Objective:** Validate the new environment before switching
        application traffic to it.

        Note: Explain the actual traffic-switching mechanism
        implemented in your deployment workflow.
        """)

    st.divider()

    # --------------------------------------------------
    # FINAL VERIFICATION
    # --------------------------------------------------

    st.header("✅ 9. Deployment Verification")

    st.markdown("""
    After Terraform Apply, Jenkins verifies the deployed application
    instead of treating a successful Terraform command as the only
    indication of deployment success.
    """)

    st.code("""
terraform output

kubectl rollout status \\
    deployment/streamlit-deploy \\
    -n streamlit-terraform \\
    --timeout=120s

kubectl get deployments,services,pods \\
    -n streamlit-terraform

kubectl get deployment streamlit-deploy \\
    -n streamlit-terraform \\
    -o jsonpath='{.spec.template.spec.containers[0].image}'
""", language="bash")

    st.markdown("""
    **Verification includes:**

    - Terraform output values.
    - Kubernetes Deployment rollout.
    - Actual deployed container image.
    - Kubernetes Service availability.
    - Running application Pods.
    """)

    st.divider()

    # --------------------------------------------------
    # TECHNOLOGY STACK
    # --------------------------------------------------

    st.header("🧰 10. Technology Stack")

    tech_columns = st.columns(3)

    technologies = [
        ("CI/CD", "Jenkins, GitHub"),
        ("Security", "Gitleaks, SonarQube, Trivy"),
        ("Testing", "Pytest"),
        ("Containers", "Docker, Docker Buildx"),
        ("Staging", "Ansible, Docker Desktop"),
        ("IaC", "Terraform"),
        ("Orchestration", "Kubernetes"),
        ("Application", "Python, Streamlit"),
        ("Registry", "Docker Hub")
    ]

    for index, (category, tools) in enumerate(technologies):
        with tech_columns[index % 3]:
            st.markdown(f"**{category}**")
            st.caption(tools)

    st.divider()

    # --------------------------------------------------
    # PROJECT OUTCOME
    # --------------------------------------------------

    st.header("🎯 11. Engineering Outcomes")

    st.markdown("""
    - Established an automated CI/CD workflow from source checkout
      through Kubernetes deployment.
    - Integrated secret detection, code analysis, quality enforcement
      and vulnerability scanning.
    - Automated Docker Desktop staging deployment through Ansible.
    - Implemented Terraform-based Kubernetes resource management.
    - Added conditional import logic for existing Kubernetes resources.
    - Implemented dedicated ServiceAccount authentication.
    - Automated post-deployment verification of Kubernetes resources
      and container image versions.

    **Architecture principle:**

    Jenkins orchestrates the delivery pipeline, Ansible automates
    staging, and Terraform manages Kubernetes infrastructure
    and application deployment.
    """)

    st.success(
        "End-to-end DevSecOps and Terraform-based Kubernetes "
        "deployment workflow."
    )
