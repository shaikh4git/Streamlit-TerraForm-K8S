import streamlit as st
from utils.image_utils import show_image, image_path, list_images

def render():

    st.header("Project 1:Enterprise AI Knowledge Intelligence & Secure DevSecOps Platform")
    
    st.markdown(
            """
            **Secure AI-powered enterprise knowledge assistant with
            department-specific document access and Role-Based Access Control.**
    
            Designed to simplify internal knowledge discovery and provide
            secure access to organizational information while enforcing
            user-specific permissions.
    
            This two-tier application combines a Streamlit frontend,
            FastAPI backend, secure authentication, RBAC authorization,
            Qdrant vector search and Groq-powered AI responses.
            """
        )
    
    # ---------------------------------------------------------
    # PROJECT OBJECTIVE
    # ---------------------------------------------------------

    st.subheader("🎯 Project Objective")

    st.markdown(
        """
        Enterprise organizations maintain information across multiple
        departments and user groups. Not every employee or user should
        have access to every document.

        This project implements an AI-powered knowledge assistant that:

        - Authenticates users securely.
        - Identifies the user's department and assigned roles.
        - Enforces Role-Based Access Control.
        - Retrieves only authorized document content.
        - Generates contextual answers using LangChain and Groq.
        - Automates application delivery through GitHub Actions and GitOps.
        """
    )

    st.subheader("🏗️ System Architecture")
    show_image("architecture","rbac-chatbot-architecture.png")

    

    # ---------------------------------------------------------
    # KEY CAPABILITIES
    # ---------------------------------------------------------

    st.subheader("⚙️ Key Capabilities")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            **🔐 Secure Authentication**

            - bcrypt password verification
            - JWT-based authentication
            - Kubernetes Secrets
            - Centralized user configuration

            **🛡️ Role-Based Access Control**

            - Department-specific authorization
            - User and role-based permissions
            - Metadata-based document filtering
            - Unauthorized retrieval prevention

            **🤖 AI Knowledge Assistant**

            - Natural language question answering
            - LangChain RAG orchestration
            - Groq LLM integration
            """
        )

    with col2:
        st.markdown(
            """
            **📂 Document Intelligence**

            - Document ingestion and processing
            - Docling document processing
            - LangChain text splitting
            - Hugging Face embeddings
            - Qdrant vector search

            **🔄 Automated CI/CD**

            - GitHub Actions
            - RBAC unit testing
            - Docker image building
            - Docker Hub publishing
            - GitOps repository updates

            **☸️ Kubernetes GitOps**

            - Docker Desktop Kubernetes
            - Kustomize
            - Argo CD synchronization
            - Argo Rollouts
            """
        )

    st.divider()


    # ---------------------------------------------------------
    # DOCUMENT INGESTION
    # ---------------------------------------------------------

    st.subheader("📚 Document Ingestion & Vectorization")
    st.markdown(
        """
        **Document processing workflow**

        - Documents are processed using Docling.
        - LangChain splits documents into manageable chunks.
        - RBAC metadata is attached to document chunks.
        - Hugging Face embeddings convert chunks into vectors.
        - Qdrant stores vectors and associated metadata.
        - The backend applies authorization filters during retrieval.
        """
    )

    show_image(
            "architecture",
            "Ingestion.png",
            caption="Document Ingestion Architecture",
        )


    st.divider()

    # ---------------------------------------------------------
    # AUTHENTICATION AND AUTHORIZATION
    # ---------------------------------------------------------

    st.subheader("🔐 Authentication & Authorization")

    with st.expander("Authentication Implementation", expanded=True):

        st.markdown(
            """
            - User credentials maintained in `Users/users.json`.
            - Passwords stored as bcrypt hashes.
            - User configuration injected through the
              `CHATBOT_USERS_JSON` environment variable.
            - Kubernetes Secret: `chatbot-secrets`.
            - API credentials managed through Kubernetes Secrets.
            - JWT used to establish authenticated identity for API requests.
            """
        )

    with st.expander("RBAC Authorization Implementation", expanded=True):

        st.markdown(
            """
            - User identity is established after successful authentication.
            - Department and assigned roles are obtained from the
              authentication module.
            - Backend authorization checks the user's permissions.
            - Document retrieval applies the permitted department,
              owner and role metadata filters.
            - Unauthorized document retrieval is denied.
            - Only authorized document context is passed to the
              LangChain/Groq pipeline.
            """
        )

    with st.expander("Kubernetes Secret Configuration"):

        st.code(
            """
Kubernetes Secret: chatbot-secrets

CHATBOT_USERS_JSON
GROQ_API_KEY
LANGCHAIN_API_KEY
            """,
            language="text",
        )

        st.caption(
            "Secret values are injected at runtime and are not stored "
            "in application source code."
        )

# -------------------------------------------------------
# FastApi backend
# -------------------------------------------------------
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
    # RBAC VALIDATION
    # ---------------------------------------------------------

    st.subheader("🧪 RBAC Validation Scenarios")

    st.markdown(
        """
        These are the defined RBAC validation scenarios,
        not live test execution results.
        """
    )

    rbac_scenarios = [
        ("Valid credentials", "Successful authentication"),
        ("Invalid password", "Authentication rejected"),
        ("Valid JWT", "Authenticated API access"),
        ("Invalid or missing JWT", "API access rejected"),
        ("Authorized department document", "Document retrieval permitted"),
        ("Unauthorized department document", "Document retrieval denied"),
        ("Authorized role", "Role-based access permitted"),
        ("Unauthorized role", "Role-based access denied"),
    ]

    for scenario, expected in rbac_scenarios:
        st.markdown(f"- **{scenario}:** {expected}")

    st.divider()

    # ---------------------------------------------------------
    # GITHUB ACTIONS CI/CD
    # ---------------------------------------------------------

    st.subheader("🔄 GitHub Actions CI/CD Pipeline")

    show_image(
            "architecture",
            "GithubAction.png",
            caption="Github Action pipeline Architecture",
        )

    st.markdown("**Pipeline stages**")

    pipeline_stages = [
        "GitHub repository checkout",
        "Python environment setup",
        "Dependency installation",
        "Backend and RBAC unit tests",
        "Code and configuration validation",
        "Frontend Docker image build",
        "Backend Docker image build",
        "Docker Hub authentication",
        "Docker image publishing",
        "GitOps repository checkout",
        "Kustomize image tag update",
        "GitOps commit and push",
        "Argo CD synchronization",
        "Argo Rollouts deployment",
    ]

    for stage in pipeline_stages:
        st.markdown(f"⚙️ {stage}")

    # ---------------------------------------------------------
    # IMAGE VERSIONING
    # ---------------------------------------------------------

    st.subheader("🏷️ Docker Image Versioning")

    st.markdown(
        """
        Application images use the first seven characters of the
        Git commit hash as the version tag.
        """
    )

    st.code(
        """
Example:

enterprise-rbac-frontend:7a9f4c2
enterprise-rbac-backend:7a9f4c2
        """,
        language="text",
    )

    st.markdown(
        """
        The generated image tags are propagated through the CI/CD
        workflow and written into the GitOps repository's
        Kustomize configuration.
        """
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
