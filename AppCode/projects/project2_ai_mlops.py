import streamlit as st
from utils.image_utils import show_image, image_path, list_images

def render():

    st.header("FasAPI backend")
    st.subheader("⚡ FastAPI Backend Architecture")

    show_image(
            "architecture",
            "FastApi.png",
            caption="FasApi backend Architecture",
        )

    st.info(
        "Security principle: Authentication establishes who the user is; "
        "authorization determines which documents the user can retrieve."
    )
    # ---------------------------------------------------------
    # KUBERNETES AND GITOPS
    # ---------------------------------------------------------

    st.subheader("☸️ Kubernetes Deployment & GitOps")

    
    show_image(
            "architecture",
            "k8s-flow.png",
            caption="Kubernetes Deployment Workflow Architecture",
        )

    st.markdown(
        """
        **Deployment workflow**

        1. GitHub Actions builds and publishes versioned Docker images.
        2. The workflow updates image tags in the GitOps repository.
        3. Argo CD detects changes in the GitOps repository.
        4. Argo CD synchronizes the Kubernetes manifests.
        5. Argo Rollouts manages the configured progressive deployment.
        6. Kubernetes runs the frontend and backend workloads.
        """
    )

    st.info(
        "Namespace separation: Streamlit frontend and FastAPI backend "
        "run in `two-tier-rbac`. Qdrant runs in `enterprise-chatbot`. "
        "The backend accesses Qdrant using its Kubernetes service DNS."
    )

    st.divider()

    # ---------------------------------------------------------
    # TECHNOLOGY STACK
    # ---------------------------------------------------------

    st.subheader("🧰 Technology Stack")

    stack_col1, stack_col2 = st.columns(2)

    with stack_col1:
        st.markdown(
            """
            **Application & AI**

            - Python
            - Streamlit
            - FastAPI
            - LangChain
            - Groq LLM
            - Hugging Face Embeddings
            - Qdrant
            - Docling

            **Authentication & Security**

            - bcrypt
            - JWT
            - Role-Based Access Control
            - Department-level authorization
            - Kubernetes Secrets
            """
        )

    with stack_col2:
        st.markdown(
            """
            **CI/CD & Containerization**

            - GitHub
            - GitHub Actions
            - Pytest
            - Docker
            - Docker Hub
            - Git

            **Cloud-Native & GitOps**

            - Kubernetes
            - Docker Desktop
            - Traefik Ingress
            - Kustomize
            - Argo CD
            - Argo Rollouts
            """
        )

    st.divider()

    # ---------------------------------------------------------
    # ENGINEERING VALUE
    # ---------------------------------------------------------

    st.subheader("💡 Engineering Value")

    st.markdown(
        """
        This project demonstrates the integration of AI application
        development with enterprise security and modern cloud-native
        engineering practices.

        It brings together:

        - Two-tier application architecture.
        - Secure authentication and authorization.
        - Department and role-based document retrieval.
        - Retrieval-Augmented Generation (RAG).
        - Vector database integration.
        - Automated testing and containerization.
        - GitHub Actions CI/CD.
        - GitOps-based Kubernetes delivery.
        - Progressive deployment with Argo Rollouts.

        The solution demonstrates how enterprise AI applications can
        combine knowledge retrieval, security controls and automated
        infrastructure delivery.
        """
    )

    st.success(
        "Designed and Developed by Shaikh S Huda | "
        "Platform Engineering • DevOps • DevSecOps • AI Engineering"
    )

    st.markdown(
        """
        **Enterprise RBAC Chatbot | AI Engineering | GitHub Actions |
        Docker | Kubernetes | Argo CD | GitOps**
        """
    )
