
import json
import math
from pathlib import Path
import random
from datetime import datetime, timezone
import pandas as pd
import streamlit as st

# ============================================================
# SHAiKH S HUDA | DEVOPS, DEVSECOPS & AI ENGINEERING PLATFORM
# Created by: Shaikh S Huda
# Portfolio: Shaikh S Huda
# DevOps Dashboard: Shaikh S Huda
# Kubernetes Engineering: Shaikh S Huda
# AI & MLOps Lab: Shaikh S Huda
# ============================================================

# These functions help manage the images/ directory and display images in the Streamlit app until st.set_page_config is called.
IMAGES_DIR = Path(__file__).parent / "images"
IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".webp"}


def image_path(*parts: str) -> Path:
    """Return a path inside images/, e.g. image_path("architecture", "diagram.png")."""
    return IMAGES_DIR.joinpath(*parts)


def list_images(folder: str) -> list[Path]:
    """All images in an images/<folder>/ directory, sorted by name."""
    directory = IMAGES_DIR / folder
    if not directory.is_dir():
        return []
    return sorted(p for p in directory.iterdir() if p.suffix.lower() in IMAGE_TYPES)


def show_image(*parts: str, caption: str = "") -> None:
    """Display one image from images/, or a friendly note if it's missing."""
    path = image_path(*parts)
    if path.exists():
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.info(f"Add {'/'.join(parts)} to AppCode/images/ to display it.")

st.set_page_config(
    page_title="Shaikh S Huda | Engineering Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

AUTHOR = "Shaikh S Huda"
APP_NAME = "Engineering Command Center"
VERSION = "v2.0"
IMAGE_REPO = "shaikhdocker/sshuda-streamlit-app"

# ------------------------------------------------------------
# Session state
# ------------------------------------------------------------

defaults = {
    "deployments": 24,
    "successful_builds": 21,
    "failed_builds": 3,
    "replicas": 4,
    "current_version": "v2.0",
    "deployment_history": [],
    "pipeline_runs": [],
    "prediction_runs": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ------------------------------------------------------------
# Styling — Shaikh S Huda Premium Dashboard
# ------------------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background:
          radial-gradient(ellipse at 85% 5%,
          rgba(18, 90, 140, 0.17), transparent 35%),
          #0b1120;
        color: #f1f5f9;
    }

    .hero {
        padding: 38px 32px;
        background: linear-gradient(
            115deg, #112f50, #17385c, #102038
        );
        border: 1px solid #315579;
        border-radius: 22px;
        margin-bottom: 24px;
    }

    .hero h1 {
        font-size: 42px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .hero p {
        font-size: 17px;
        color: #c7d9ef;
    }

    .tag {
        display: inline-block;
        background: #155e75;
        color: #cffafe;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .info-card {
        background: #14243b;
        border: 1px solid #294365;
        border-radius: 14px;
        padding: 20px;
        margin: 12px 0;
        min-height: 120px;
    }

    .info-card h3 {
        color: #7dd3fc;
        margin: 0 0 8px 0;
    }

    .info-card p {
        color: #cbd5e1;
        margin: 0;
    }

    .pipeline {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #285077;
        background: #132b45;
        text-align: center;
        font-weight: 700;
    }

    .footer {
        text-align: center;
        padding: 24px;
        color: #94a3b8;
        border-top: 1px solid #334155;
        margin-top: 40px;
    }

    [data-testid="stMetric"] {
        background: #13233a;
        border: 1px solid #294365;
        border-radius: 14px;
        padding: 16px;
    }

    h1, h2, h3 {
        letter-spacing: -0.4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def card(title, description):
    st.markdown(
        f"""
        <div class="info-card">
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def add_deployment(strategy, version, replicas):
    record = {
        "time": datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        ),
        "engineer": AUTHOR,
        "strategy": strategy,
        "version": version,
        "replicas": replicas,
        "status": "Simulated Success",
    }

    st.session_state.deployment_history.insert(0, record)
    st.session_state.current_version = version
    st.session_state.replicas = replicas
    st.session_state.deployments += 1
    return record


def monitoring_data(points=30):
    random_generator = random.Random(42)

    return pd.DataFrame(
        {
            "CPU Usage (%)": [
                round(
                    35 + 10 * math.sin(i / 3)
                    + random_generator.uniform(-5, 5),
                    2,
                )
                for i in range(points)
            ],
            "Memory Usage (%)": [
                round(
                    49 + 7 * math.cos(i / 5)
                    + random_generator.uniform(-3, 3),
                    2,
                )
                for i in range(points)
            ],
        }
    )


def run_pipeline():
    stages = [
        "GitHub Checkout",
        "Python Unit Tests",
        "Gitleaks Secret Scanning",
        "SonarQube Quality Gate",
        "Trivy Filesystem Scan",
        "Docker Build",
        "Trivy Image Scan",
        "Docker Push",
        "Ansible Staging",
        "Terraform Plan",
        "Terraform Apply",
        "Kubernetes Rollout",
    ]

    result = {
        "engineer": AUTHOR,
        "time": datetime.now(timezone.utc).isoformat(),
        "status": "Simulated Success",
        "stages": stages,
    }

    st.session_state.pipeline_runs.insert(0, result)
    st.session_state.successful_builds += 1
    return stages


# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------

with st.sidebar:
    st.title("🚀 Shaikh S Huda")
    st.caption("Engineering Command Center")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "📊 DevOps Dashboard",
            "🔄 CI/CD Pipeline",
            "☸️ Kubernetes Lab",
            "🚦 Deployment Strategies",
            "📈 Monitoring",
            "🤖 AI & MLOps Lab",
            "📁 Projects",
            "🎓 Graduation Photos",
            "🏢 Companies & Clients",
            "👨‍💻 About Shaikh S Huda",
            "📥 Reports",
        ],
    )

    st.divider()

    st.success("● Demo Platform Online")
    st.caption(f"Version: {VERSION}")
    st.caption(f"Maintained by {AUTHOR}")
    st.caption("Docker • Jenkins • Kubernetes • Terraform")

    st.info(
        "Interactive demonstration environment. "
        "Metrics and deployment actions are simulated."
    )


# ------------------------------------------------------------
# HOME
# ------------------------------------------------------------

if page == "🏠 Home":
    st.markdown(
        f"""
        <div class="hero">
            <span class="tag">DEVOPS • DEVSECOPS • CLOUD • AI</span>
            <h1>Shaikh S Huda 🚀</h1>
            <p>Platform Engineering, DevSecOps & Intelligent Automation</p>
            <p>
                Welcome to the Engineering Command Center,
                designed and developed by Shaikh S Huda.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    a, b, c, d = st.columns(4)

    a.metric("Pipeline Builds", st.session_state.successful_builds)
    b.metric("Deployments", st.session_state.deployments)
    c.metric("Kubernetes Replicas", st.session_state.replicas)
    d.metric("Platform Version", st.session_state.current_version)

    st.subheader("Explore the Engineering Platform")

    col1, col2, col3 = st.columns(3)

    with col1:
        card(
            "🔧 DevOps & DevSecOps",
            "CI/CD automation using Jenkins, GitHub, "
            "SonarQube, Gitleaks, Trivy and Docker.",
        )

    with col2:
        card(
            "☸️ Kubernetes & GitOps",
            "Container orchestration, Helm, Terraform, "
            "Argo CD and Argo Rollouts.",
        )

    with col3:
        card(
            "🤖 AI & MLOps",
            "Python, data engineering, predictive analytics, "
            "Databricks and machine learning.",
        )

    st.subheader("Technology Stack")

    st.write(
        "Python | Streamlit | Jenkins | Docker | Kubernetes | "
        "Terraform | Ansible | GitHub Actions | Argo CD | "
        "Argo Rollouts | Prometheus | Grafana | SonarQube | "
        "Gitleaks | Trivy | Azure Databricks | AI/ML | AWS | Azure | Linux | Git"
    )

    st.info(
        "Created by Shaikh S Huda — "
        "Demonstrating modern platform engineering practices."
    )


# ------------------------------------------------------------
# DEVOPS DASHBOARD
# ------------------------------------------------------------

elif page == "📊 DevOps Dashboard":
    st.title("📊 Shaikh S Huda — DevOps Dashboard")
    st.caption("Interactive simulated platform metrics")

    total = (
        st.session_state.successful_builds
        + st.session_state.failed_builds
    )

    success_rate = (
        100 * st.session_state.successful_builds / total
        if total else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Successful Builds", st.session_state.successful_builds)
    c2.metric("Failed Builds", st.session_state.failed_builds)
    c3.metric("Build Success Rate", f"{success_rate:.1f}%")
    c4.metric("Active Replicas", st.session_state.replicas)

    st.subheader("Simulated Infrastructure Utilization")
    st.line_chart(monitoring_data())

    st.subheader("Platform Components")

    components = pd.DataFrame(
        [
            ["Jenkins", "CI/CD", "Demo Ready"],
            ["Docker", "Containers", "Demo Ready"],
            ["Kubernetes", "Orchestration", "Demo Ready"],
            ["Terraform", "Infrastructure as Code", "Demo Ready"],
            ["Ansible", "Configuration Automation", "Demo Ready"],
            ["Argo CD", "GitOps", "Demo Ready"],
            ["Prometheus", "Monitoring", "Demo Ready"],
            ["Grafana", "Visualization", "Demo Ready"],
        ],
        columns=["Component", "Function", "Demo Status"],
    )

    st.dataframe(
        components,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Dashboard data is simulated and does not query live "
        "Jenkins, Prometheus or Kubernetes APIs."
    )


# ------------------------------------------------------------
# CI/CD PIPELINE
# ------------------------------------------------------------

elif page == "🔄 CI/CD Pipeline":
    st.title("🔄 Shaikh S Huda — CI/CD Automation")
    st.write(
        "Explore the CI/CD stages used in a modern "
        "DevSecOps engineering workflow."
    )

    pipeline_stages = [
        "GitHub",
        "Unit Tests",
        "Gitleaks",
        "SonarQube",
        "Trivy",
        "Docker",
        "Ansible",
        "Terraform",
        "Kubernetes",
    ]

    for start in range(0, len(pipeline_stages), 3):
        cols = st.columns(3)
        for col, stage in zip(
            cols, pipeline_stages[start:start + 3]
        ):
            with col:
                st.markdown(
                    f'<div class="pipeline">✅ {stage}</div>',
                    unsafe_allow_html=True,
                )

    st.divider()

    if st.button(
        "▶ Run Simulated CI/CD Pipeline",
        type="primary",
        use_container_width=True,
    ):
        stages = run_pipeline()

        for stage in stages:
            st.success(f"✔ {stage} — Simulated Success")

        st.balloons()
        st.success(
            f"Pipeline demonstration completed by {AUTHOR}!"
        )

    st.subheader("Pipeline Execution History")

    if st.session_state.pipeline_runs:
        st.dataframe(
            pd.DataFrame(st.session_state.pipeline_runs)[
                ["time", "engineer", "status"]
            ],
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("Run the simulated pipeline to generate history.")


# ------------------------------------------------------------
# KUBERNETES
# ------------------------------------------------------------

elif page == "☸️ Kubernetes Lab":
    st.title("☸️ Shaikh S Huda — Kubernetes Lab")
    st.caption("Interactive deployment and scaling simulator")

    namespace = st.selectbox(
        "Select Namespace",
        [
            "streamlit-terraform",
            "streamlit-canary",
            "streamlit-bluegreen",
            "streamlit-argocd",
        ],
    )

    replicas = st.slider(
        "Desired Kubernetes Replicas",
        min_value=1,
        max_value=20,
        value=st.session_state.replicas,
    )

    image_version = st.text_input(
        "Docker Image Tag",
        value=st.session_state.current_version,
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🚀 Simulate Kubernetes Deployment",
            type="primary",
        ):
            add_deployment(
                "RollingUpdate",
                image_version,
                replicas,
            )
            st.success(
                f"Simulated deployment by {AUTHOR} "
                f"to namespace {namespace} completed."
            )

    with col2:
        if st.button("🔄 Reset Simulated Replicas"):
            st.session_state.replicas = 2
            st.rerun()

    st.subheader("Simulated Kubernetes Pods")

    pods = pd.DataFrame(
        [
            {
                "Pod": f"streamlit-deploy-demo-{i + 1:02d}",
                "Status": "Running",
                "Ready": "1/1",
                "Image": image_version,
                "Namespace": namespace,
            }
            for i in range(replicas)
        ]
    )

    st.dataframe(
        pods,
        use_container_width=True,
        hide_index=True,
    )

    st.info(
        "Scaling here changes only the dashboard simulation, "
        "not your real Kubernetes Deployment."
    )


# ------------------------------------------------------------
# DEPLOYMENT STRATEGIES
# ------------------------------------------------------------

elif page == "🚦 Deployment Strategies":
    st.title("🚦 Shaikh S Huda — Deployment Strategies")

    strategy = st.selectbox(
        "Choose Kubernetes Deployment Strategy",
        [
            "Rolling Update",
            "Canary Deployment",
            "Blue-Green Deployment",
        ],
    )

    st.subheader(strategy)

    if strategy == "Rolling Update":
        st.write(
            "Replace old application Pods gradually while "
            "maintaining the configured availability."
        )

        surge = st.slider("Max Surge (Pods)", 0, 5, 1)
        unavailable = st.slider("Max Unavailable (Pods)", 0, 5, 0)

        st.write(f"Max Surge: **{surge}**")
        st.write(f"Max Unavailable: **{unavailable}**")

        if surge == 0 and unavailable == 0:
            st.warning(
                "At least one of Max Surge or "
                "Max Unavailable must permit progress."
            )

    elif strategy == "Canary Deployment":
        st.write(
            "Gradually send traffic to a new application version "
            "while the stable version continues serving users."
        )

        canary = st.slider(
            "Canary Traffic Percentage",
            min_value=0,
            max_value=100,
            value=20,
            step=5,
        )

        traffic = pd.DataFrame(
            {
                "Version": ["Stable", "Canary"],
                "Traffic": [100 - canary, canary],
            }
        ).set_index("Version")

        st.bar_chart(traffic)

        st.write(f"Stable Traffic: **{100 - canary}%**")
        st.write(f"Canary Traffic: **{canary}%**")

        st.caption(
            "This models desired traffic distribution, "
            "not actual Kubernetes request routing."
        )

    else:
        st.write(
            "Blue-Green Deployment maintains two environments "
            "and switches traffic from the current version "
            "to the replacement version."
        )

        active = st.radio(
            "Simulated Active Environment",
            ["Blue", "Green"],
            horizontal=True,
        )

        c1, c2 = st.columns(2)

        with c1:
            if active == "Blue":
                st.success("🔵 Blue — Active")
            else:
                st.info("🔵 Blue — Standby")

        with c2:
            if active == "Green":
                st.success("🟢 Green — Active")
            else:
                st.info("🟢 Green — Standby")

    st.caption(
        f"Deployment strategy learning environment by {AUTHOR}"
    )


# ------------------------------------------------------------
# MONITORING
# ------------------------------------------------------------

elif page == "📈 Monitoring":
    st.title("📈 Shaikh S Huda — Observability Center")
    st.caption("Prometheus and Grafana-style simulated metrics")

    points = st.slider(
        "Monitoring Samples",
        min_value=10,
        max_value=120,
        value=40,
    )

    data = monitoring_data(points)

    cpu = data["CPU Usage (%)"].iloc[-1]
    memory = data["Memory Usage (%)"].iloc[-1]

    m1, m2, m3 = st.columns(3)

    m1.metric("CPU Usage", f"{cpu:.1f}%")
    m2.metric("Memory Usage", f"{memory:.1f}%")
    m3.metric("Simulated Availability", "99.9%")

    st.subheader("CPU and Memory Utilization")
    st.line_chart(data)

    st.subheader("Resource Monitoring")

    st.progress(
        min(max(int(cpu), 0), 100),
        text="CPU Utilization",
    )

    st.progress(
        min(max(int(memory), 0), 100),
        text="Memory Utilization",
    )

    st.subheader("Alert Simulation")

    threshold = st.slider(
        "CPU Alert Threshold (%)",
        min_value=10,
        max_value=100,
        value=80,
    )

    if cpu >= threshold:
        st.error("Simulated Prometheus Alert: High CPU Usage")
    else:
        st.success("CPU usage is below the simulated alert threshold.")

    st.caption(
        "These are synthetic metrics; no live Prometheus "
        "endpoint is queried."
    )


# ------------------------------------------------------------
# AI & MLOPS
# ------------------------------------------------------------

elif page == "🤖 AI & MLOps Lab":
    st.title("🤖 Shaikh S Huda — AI & MLOps Lab")

    st.write(
        "Explore a simplified predictive analytics experiment "
        "built with Python and Streamlit."
    )

    st.subheader("User Activation Prediction Simulator")

    activity = st.slider(
        "User Activity Score",
        min_value=0,
        max_value=100,
        value=65,
    )

    engagement = st.slider(
        "User Engagement Score",
        min_value=0,
        max_value=100,
        value=70,
    )

    retention = st.slider(
        "Historical Retention Score",
        min_value=0,
        max_value=100,
        value=55,
    )

    # Demonstration scoring formula, not a trained ML model.
    prediction = (
        activity * 0.35
        + engagement * 0.40
        + retention * 0.25
    )

    st.metric(
        "Simulated Activation Score",
        f"{prediction:.1f}/100",
    )

    if prediction >= 75:
        st.success("High activation score")
    elif prediction >= 50:
        st.warning("Moderate activation score")
    else:
        st.error("Low activation score")

    if st.button("🧠 Run AI Experiment"):
        st.session_state.prediction_runs += 1

        st.success(
            f"Experiment #{st.session_state.prediction_runs} "
            f"completed by {AUTHOR}."
        )

    st.divider()

    st.subheader("MLOps Architecture")

    st.code(
        """
Data Ingestion
      |
Data Validation
      |
Feature Engineering
      |
Model Training
      |
Model Evaluation
      |
Model Registry
      |
CI/CD Pipeline
      |
Kubernetes Deployment
      |
Monitoring & Retraining
        """,
        language="text",
    )

    st.info(
        "The activation score is a weighted demonstration. "
        "It is not a trained predictive model."
    )


# ------------------------------------------------------------
# GRADUATION PHOTOS
# ------------------------------------------------------------

elif page == "🎓 Graduation Photos":
    st.title("🎓 MS Data Science Graduation Day")
    st.subheader("Saint Peter's University")
    st.caption("17 May 2024 | New Jersey, USA")

    st.markdown("""
    ### A Memorable Academic Milestone

    Completing my Master's degree in Data Science at Saint Peter's
    University was an important milestone in my academic and
    professional journey.

    My studies strengthened my knowledge of Python programming,
    data science and analytics, machine learning, data engineering,
    cloud technologies, and applied AI.
    """)

    # Store graduation-2024.png and optional additional graduation
    # images in AppCode/images/. The gallery auto-discovers them.

    photo_files = list_images("graduation")
    if photo_files:
        st.subheader("Graduation Photo Gallery")
        for start in range(0, len(photo_files), 2):
            columns = st.columns(2)
            for column, photo in zip(columns, photo_files[start:start + 2]):
                with column:
                    st.image(
                        str(photo),
                        caption=f"Saint Peter's University — {photo.stem.replace('-', ' ').title()}",
                        use_container_width=True,
                    )

# ------------------------------------------------------------
# COMPANIES AND CLIENT ENGAGEMENTS
# ------------------------------------------------------------

elif page == "🏢 Companies & Clients":
    st.title("🏢 Companies & Client Engagements")
    st.write(
        "Professional experience in infrastructure, DevOps, DevSecOps, "
        "cloud engineering, data science, and technical training."
    )

    experiences = [
        {
            "company": "Freelancer",
            "period": "October 2024 – Present",
            "title": "Platform Engineering, DevOps & AI Engineering | Cloud-Native Architecture, DevSecOps, MLOps & RAG",
            "details": [
                "Jenkins and GitHub Actions CI/CD pipeline implementations",
                "Docker and Kubernetes deployments",
                "Terraform Infrastructure as Code",
                "Argo CD GitOps and Argo Rollouts",
                "DevSecOps security integration",
                "Prometheus and Grafana monitoring",
                "AI Engineering: Two-Tier RBAC Chatbot with Streamlit frontend, FastAPI backend, JWT authentication and role-based document access",
                "LLM & RAG Engineering: Groq LLM (openai/gpt-oss-20b), Qdrant vector database, Hugging Face embeddings, LangChain, metadata-based authorization and guardrails.",
                "Machine learning model building",
                "Hands-on machine learning and data analytics projects",
                "Generative AI and RAG chatbot prototypes using Python, "
                "LangChain, Llama, Hugging Face Transformers, ChromaDB,Qdrant and FastAPI",
                "Automated CI/CD for ML model packaging and deployment ",
            ],
            "technologies": (
                "AWS, Azure, Terraform, Jenkins, Docker, Kubernetes, "
                "Argo CD, Python, LangChain, Llama, Hugging Face "
                "Transformers, ChromaDB, Qdrant, FastAPI"
            ),
        },

        {
            "company": "Freelancer — Kuala Lumpur, Malaysia",
            "Client": "Robomy Sdn Bhd",
            "period": "September 2024 – October 2024",
            "title": "Technical Trainer",
            "details": [
                "Delivered technical training workshops",
                "Python and Django development",
                "DevOps fundamentals and Linux",
                "Machine learning and KNIME",
            ],
            "technologies": "Python, Django, Linux, DevOps, KNIME",
        },

        {
            "company": "Dell EMC — United States",
            "Client": "PowerPath",
            "period": "November 2022 – May 2024",
            "title": "Co-op / Internship — Pricnipal Software Engineer & Data Science",
            "details": [
                "Customer experience and PowerPath escalations",
                "Python-based data processing",
                "Data engineering and ETL workflows",
                "Azure Databricks and analytics",
                "Machine learning and AI-related initiatives",
            ],
            "technologies": "Python, Azure, Databricks, ETL, ML",
        },
        {
            "company": "Dell EMC — India",
            "Client": "Dell EMC, India",
            "period": "May 2017 – October 2022",
            "title": "Principal Software Engineer",
            "details": [
                "Enterprise storage and infrastructure support",
                "Technical troubleshooting and escalations",
                "Customer experience and technical problem resolution",
                "Linux and enterprise infrastructure technologies",
            ],
            "technologies": "Linux, Enterprise Storage, PowerPath",
        },
        {
            "company": "Wipro Limited — Finland",
            "Client": "Stora Enso, Imatra, Finland",
            "period": "April 2014 – May 2017 · 3 yrs 2 mos",
            "title": "Senior Solution Consultant",
            "details": [
                "Led a critical data center migration from Tieto to Wipro, "
                "provisioning 300+ Linux servers across Finland with zero major service disruption.",
                "Designed and executed enterprise data migration strategies.",
                "Built a 6-node VMware ESXi private cloud infrastructure, "
                "deploying SUSE Linux virtual machines.",
                "Served as onsite SUSE Linux and Red Hat Enterprise Linux (RHEL) Subject Matter Expert.",
                "Led offshore technical teams and managed end-to-end Linux infrastructure support.",
                "Architected Linux and VMware ESXi clusters.",
                "Performed Physical-to-Virtual (P2V) migrations.",
                "Optimized Linux kernels for infrastructure performance.",
                "Led root cause analysis, major incident management, "
                "troubleshooting, and service restoration.",
            ],
            "technologies": (
                "SUSE Linux, RHEL, VMware ESXi, vCenter, "
                "Linux Clustering, Data Center Migration, "
                "P2V Migration, Shell Scripting, "
                "Kernel Tuning, Incident Management"
            ),
        },
        {
            "company": "Wipro Limited — Reading, United Kingdom",
            "Client": "Thames Water Utilities, United Kingdom",
            "period": "June 2011 – March 2014 · 2 yrs 10 mos",
            "title": "Infrastructure Specialist",
            "details": [
                "Designed and administered enterprise Linux infrastructure "
                "supporting 500+ Linux servers.",
                "Performed Linux kernel fine-tuning for SAP applications "
                "and IBM DB2 database workloads.",
                "Configured VMware vCenter and deployed virtual machines "
                "across VMware ESX clusters.",
                "Managed IBM AIX virtualization environments.",
                "Prepared and configured infrastructure platforms "
                "for Oracle and IBM DB2 database deployments.",
                "Delivered end-to-end Linux architecture, administration, "
                "troubleshooting, and performance optimization.",
                "Conducted customer meetings, technical discussions, "
                "requirements gathering, and infrastructure planning.",
            ],
            "technologies": (
                "Linux, SUSE Linux, RHEL, IBM AIX, "
                "VMware ESX, VMware vCenter, SAP, "
                "IBM DB2, Oracle, Kernel Tuning, "
                "Virtualization, Infrastructure Architecture"
            ),
        },
        {
            "company": "Wipro Limited — Bengaluru, India",
            "Client": "Thames Water Utilities, United Kingdom",
            "period": "July 2008 – May 2011 · 2 yrs 11 mos",
            "title": "System Administrator",
            "details": [
                "Provided multi-operating-system administration "
                "and enterprise infrastructure support.",
                "Automated routine system administration tasks "
                "using Bash shell scripting.",
                "Monitored infrastructure health, availability, "
                "performance, and operational alerts.", 
                "Managed enterprise backup and restore operations.",
                "Delivered on-call infrastructure support, "
                "incident troubleshooting, and issue resolution.",
                "Supported business-critical enterprise systems "
                "to maintain operational reliability.",
            ],
            "technologies": (
                "Linux, Unix, Bash Shell Scripting, "
                "System Administration, Infrastructure Monitoring, "
                "Backup and Recovery, Incident Management, "
                "Enterprise Infrastructure Support"
            ),
        },
        {
            "company": "Tutor Vista — Bangalore, India",
            "Client": "Tutor Vista, India",
             "period": "December 2007 – July 2008",
             "title": "Offshore Faculty",
             "details": [
                 "Tutoring Physics and Mathematics online Globally mostly the students from the USA and Canada ",
             ],
             "technologies": "Google Chat for TutorVista",
         },

    ]

    for experience in experiences:
        with st.container(border=True):
            st.subheader(experience["company"])
            st.write(f"**Period:** {experience['period']}")
            st.write(f"**Title:** {experience['title']}")
            st.markdown("\n".join(f"- {detail}" for detail in experience["details"]))
            st.caption(f"Technologies: {experience['technologies']}")

    st.caption(
        "Add named client engagements only when you have permission "
        "to disclose them publicly."
    )


# ------------------------------------------------------------
# PROJECTS
# ------------------------------------------------------------

elif page == "📁 Projects":

    st.title("📁 AI / MLOps / Data Engineering / DevOps Projects")
    st.markdown(
        "Enterprise solutions designed and developed by **Shaikh S Huda**"
    )

    st.markdown(
        """
        **AI • DEVSECOPS • GITOPS • KUBERNETES • PLATFORM ENGINEERING**
        """
    )

    st.divider()

    # =========================================================
    # PROJECT 1: ENTERPRISE RBAC CHATBOT
    # =========================================================

    st.header("Project 1: Enterprise RBAC Chatbot 🤖")

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
    # APPLICATION ARCHITECTURE
    # ---------------------------------------------------------

    st.subheader("🏗️ Solution Architecture")
    st.write(
            "End-to-end architecture covering authentication, "
            "AI-based document retrieval, security and deployment."
        )
    show_image(
            "architecture", "rbac-chatbot-architecture.png",
            caption="Enterprise RBAC Chatbot — Secure, Role-Based AI Architecture",
        )

    st.markdown(
        """
        **Two-Tier Application Architecture – Streamlit Frontend
        + FastAPI Backend**
        """
    )

    application_architecture = r"""
                         USER
                           |
                           v
                    TRAEFIK INGRESS
                           |
                           v
                  STREAMLIT FRONTEND
                     (CHATBOT UI)
                           |
                    REST API REQUEST
                           |
                           v
                    FASTAPI BACKEND
                           |
              +------------+------------+
              |                         |
              v                         v
       USER AUTHENTICATION        JWT VALIDATION
              |                         |
        bcrypt Verify                   |
              |                         |
              +------------+------------+
                           |
                           v
                AUTHENTICATED IDENTITY
                           |
              Department + Assigned Roles
                           |
                           v
                  RBAC AUTHORIZATION
                           |
                 ACCESS CONTROL CHECK
                           |
                           v
                 DOCUMENT RETRIEVAL
                           |
                           v
               QDRANT VECTOR DATABASE
                           |
                  METADATA FILTERING
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
          PRINCIPAL      TEACHER       STUDENT
             |             |             |
             +-------------+-------------+
                           |
                  AUTHORIZED DOCUMENTS
                           |
                           v
                 AUTHORIZED CONTEXT
                           |
                           v
                LANGCHAIN RAG PIPELINE
                           |
                           v
                      GROQ LLM
                           |
                           v
                    AI RESPONSE
                           |
                           v
                   FASTAPI BACKEND
                           |
                           v
                  STREAMLIT FRONTEND
                           |
                           v
                         USER
"""

    st.code(application_architecture, language="text")

    st.info(
        "Security principle: Authentication establishes who the user is; "
        "authorization determines which documents the user can retrieve."
    )

    # ---------------------------------------------------------
    # DOCUMENT INGESTION
    # ---------------------------------------------------------

    st.subheader("📚 Document Ingestion & Vectorization")

    document_architecture = r"""
                DEPARTMENT DOCUMENTS
                           |
                           v
                 DOCUMENT INGESTION
                           |
                           v
                       DOCLING
                           |
                           v
                 DOCUMENT PROCESSING
                           |
                           v
                 LANGCHAIN CHUNKING
                           |
                           v
                 RBAC METADATA TAGGING
                           |
              Owner / Department / Roles
                           |
                           v
                HUGGING FACE EMBEDDINGS
                           |
                           v
                 QDRANT VECTOR DATABASE
                           |
                           v
                   READY FOR RETRIEVAL
                           |
                           v
                 FASTAPI RETRIEVAL SERVICE
                           |
                           v
                 RBAC METADATA FILTERING
                           |
                           v
                 AUTHORIZED DOCUMENT CHUNKS
"""

    st.code(document_architecture, language="text")

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

    cicd_architecture = r"""
       =========================================
               CI/CD AND GITOPS PIPELINE
       =========================================

                  DEVELOPER
                      |
                      v
           APPLICATION GITHUB REPOSITORY
                      |
                      v
              GIT PUSH / PULL REQUEST
                      |
                      v
                GITHUB ACTIONS
                      |
             +--------+---------+
             |                  |
             v                  v
         BACKEND TESTS     CODE VALIDATION
             |
             v
          RBAC TESTS
             |
             v
       +-----+-------------------+
       |                         |
       v                         v
 FRONTEND DOCKER BUILD     BACKEND DOCKER BUILD
       |                         |
       v                         v
 FRONTEND IMAGE            BACKEND IMAGE
       |                         |
       +------------+------------+
                    |
                    v
                 DOCKER HUB
                    |
          +---------+---------+
          |                   |
          v                   v
    FRONTEND IMAGE       BACKEND IMAGE
      TAG UPDATE            TAG UPDATE
          |                   |
          +---------+---------+
                    |
                    v
             GITOPS REPOSITORY
                    |
                    v
             KUSTOMIZE MANIFESTS
                    |
                    v
                  ARGO CD
                    |
             GITOPS SYNCHRONIZATION
                    |
                    v
              ARGO ROLLOUTS
                    |
                    v
         DOCKER DESKTOP KUBERNETES
                    |
          +---------+---------+
          |                   |
          v                   v
    FRONTEND DEPLOYMENT  BACKEND DEPLOYMENT
          |                   |
          v                   v
     FRONTEND SERVICE     BACKEND SERVICE
          |                   |
          +---------+---------+
                    |
                    v
               TRAEFIK INGRESS
                    |
                    v
              RUNNING CHATBOT
"""
    # Side-by-side Architecture and CI/CD Pipeline
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        show_image(
            "architecture",
            "GithubAction.png",
            caption="Enterprise RBAC Chatbot — Secure, Role-Based AI Architecture",
        )

    with col2:
        st.code(cicd_architecture, language="text")

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

    kubernetes_architecture = r"""
       =========================================
               KUBERNETES INFRASTRUCTURE
       =========================================

             DOCKER DESKTOP KUBERNETES
                         |
             +-----------+-----------+
             |                       |
             v                       v
       NAMESPACE:              NAMESPACE:
       TWO-TIER-RBAC           ENTERPRISE-CHATBOT
             |                       |
       +-----+------+                |
       |            |                |
       v            v                v
   STREAMLIT      FASTAPI          QDRANT
   FRONTEND       BACKEND          VECTOR DB
       |            |                |
       v            v                v
   DEPLOYMENT    DEPLOYMENT       DEPLOYMENT
       |            |                |
       v            v                v
    SERVICE       SERVICE          SERVICE
       |            |
       +-----+------+
             |
             v
       BACKEND CONNECTS TO
             |
             v
   qdrant.enterprise-chatbot.svc.cluster.local:6333
"""

    st.code(kubernetes_architecture, language="text")

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

# ------------------------------------------------------------
# ABOUT
# ------------------------------------------------------------



elif page == "👨‍💻 About Shaikh S Huda":

    # ======================================
    # HEADER - PROFILE DETAILS AND PHOTO
    # ======================================

    profile_left, profile_right = st.columns([3, 1], gap="large")

    with profile_left:
        st.title("👨‍💻 Shaikh S Huda")

        st.subheader(
            "Platform Engineering | DevOps | DevSecOps | AI"
        )

        st.markdown(
            """
            Welcome to the professional engineering portfolio
            of **Shaikh S Huda**.

            This platform demonstrates practical knowledge of
            continuous integration, continuous delivery,
            container orchestration, infrastructure automation,
            security scanning and machine learning workflows.
            """
        )

    with profile_right:
        image_path = (
            Path(__file__).resolve().parent
            / "images"
            / "graduation"
            / "shaikh-profile.jpg"
        )

        st.image(
            str(image_path),
            caption="Shaikh S Huda",
            width="stretch"
        )


    st.divider()

    # ======================================
    # ENGINEERING EXPERTISE
    # ======================================

    left, right = st.columns(2)

    with left:
        card(
            "Cloud & Infrastructure Engineering",
            "Linux, Docker, Kubernetes, Terraform, "
            "Ansible, AWS and Azure.",
        )

        card(
            "DevOps & GitOps Automation",
            "Jenkins, GitHub Actions, Argo CD, "
            "Argo Rollouts and CI/CD pipelines.",
        )

    with right:
        card(
            "DevSecOps Engineering",
            "Gitleaks, Trivy, SonarQube, "
            "OWASP Dependency-Check and security gates.",
        )

        card(
            "Data Engineering & MLOps",
            "Python, Databricks, machine learning, "
            "automation and predictive analytics.",
        )

    st.subheader("Engineering Philosophy")

    st.success(
        "Build securely. Automate intelligently. "
        "Deploy reliably. Monitor continuously."
    )

    st.markdown(
        f"**Designed and developed by {AUTHOR}.**"
    )

# ------------------------------------------------------------
# REPORTS
# ------------------------------------------------------------

elif page == "📥 Reports":
    st.title("📥 Shaikh S Huda — Deployment Reports")

    st.subheader("Current Simulated Platform State")

    report = {
        "application": APP_NAME,
        "engineer": AUTHOR,
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "namespace": "streamlit-terraform",
        "docker_image_repository": IMAGE_REPO,
        "current_demo_version": st.session_state.current_version,
        "simulated_replicas": st.session_state.replicas,
        "simulated_deployments": st.session_state.deployments,
        "successful_demo_builds": st.session_state.successful_builds,
        "deployment_history": st.session_state.deployment_history,
        "pipeline_runs": st.session_state.pipeline_runs,
        "data_source": "Streamlit demonstration session",
    }

    st.json(report)

    st.download_button(
        label="⬇ Download Shaikh S Huda Deployment Report",
        data=json.dumps(report, indent=2),
        file_name="shaikh_s_huda_deployment_report.json",
        mime="application/json",
        type="primary",
    )

    st.subheader("Deployment History")

    if st.session_state.deployment_history:
        st.dataframe(
            pd.DataFrame(st.session_state.deployment_history),
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info(
            "No simulated deployments have been recorded yet."
        )

    st.caption(
        "Reports describe simulated data from this "
        "Streamlit session, not live Kubernetes infrastructure."
    )


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------


st.html(
    f"""
    <style>
        .footer {{
            text-align: center;
            padding: 20px 15px;
            margin-top: 30px;
            border-top: 1px solid rgba(128, 128, 128, 0.3);
            font-size: 14px;
            color: #aab8ce;
        }}

        .footer p {{
            margin: 12px 0;
        }}

        .footer a {{
            color: #8bbcff;
            text-decoration: none;
            font-weight: 600;
        }}

        .footer a:hover {{
            text-decoration: underline;
        }}
    </style>

    <div class="footer">
        <div>
            🚀 {AUTHOR} | Engineering Command Center | {VERSION}
        </div>

        <p>
            DevOps • DevSecOps • Docker • Kubernetes • Terraform •
            Python • AI & MLOps • AWS • Azure
        </p>

        <p>
            🔗 <a href="https://www.linkedin.com/in/shaikh-huda-shams-617aa530/"
            target="_blank">LinkedIn Profile</a>
        </p>

        <p>
            💻 <a href="https://github.com/shaikh4git/"
            target="_blank">GitHub Repositories</a>
        </p>

        <p>Designed and Developed by {AUTHOR}</p>
    </div>
    """
)

