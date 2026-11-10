
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
            "title": "DevOps, DevSecOps & Cloud Engineering",
            "details": [
                "Jenkins CI/CD pipeline implementations",
                "Docker and Kubernetes deployments",
                "Terraform Infrastructure as Code",
                "Argo CD GitOps and Argo Rollouts",
                "DevSecOps security integration",
                "Prometheus and Grafana monitoring",
                "Machine learning model building",
                "Hands-on machine learning and data analytics projects",
                "Generative AI and RAG chatbot prototypes using Python, "
                "LangChain, Llama, Hugging Face Transformers, ChromaDB, and FastAPI",
                "Automated CI/CD for ML model packaging and deployment "
                "using Jenkins, Docker, Kubernetes, and GitHub Actions",
            ],
            "technologies": (
                "AWS, Azure, Terraform, Jenkins, Docker, Kubernetes, "
                "Argo CD, Python, LangChain, Llama, Hugging Face "
                "Transformers, ChromaDB, FastAPI"
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

    st.title("📁 AI/MLOPS/Data Engineering/DevOps Projects")
    st.caption(
        "Enterprise solutions designed and developed by Shaikh S Huda"
    )

    # ======================================
    # PROJECT 1: ENTERPRISE RBAC CHATBOT
    # ======================================

    st.markdown(
        """
        <div class="hero">
            <span class="tag">AI • DEVSECOPS • GITOPS • KUBERNETES</span>
            <h1>Project 1: Enterprise RBAC Chatbot 🤖</h1>
            <p>
                Secure AI-powered enterprise knowledge assistant
                with department-specific document access and
                Role-Based Access Control.
            </p>
            <p>
                Designed to reduce internal communication delays,
                eliminate departmental information barriers and
                provide secure access to company knowledge.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ======================================
    # PROJECT OBJECTIVE
    # ======================================

    st.subheader("🎯 Project Objective")

    st.write(
        """
        Enterprise organizations maintain sensitive information
        across multiple departments, including Finance, HR,
        Marketing and Executive Management.

        This project implements an AI-powered internal chatbot
        that allows employees to retrieve relevant company
        information while enforcing department-specific access
        restrictions.

        The chatbot uses authentication and authorization
        controls to ensure that users can only retrieve
        information permitted by their assigned roles.
        """
    )

    # ======================================
    # PROJECT HIGHLIGHTS
    # ======================================

    st.subheader("⚙️ Key Capabilities")

    col1, col2, col3 = st.columns(3)

    with col1:
        card(
            "🔐 Secure Authentication",
            "User authentication using bcrypt password hashes "
            "and centrally managed Kubernetes Secrets."
        )

    with col2:
        card(
            "🛡️ Role-Based Access Control",
            "Department-specific document retrieval based on "
            "authenticated user identity, department and roles."
        )

    with col3:
        card(
            "🤖 AI-Powered Knowledge Assistant",
            "Natural language question answering using "
            "Groq LLM integration and LangChain."
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        card(
            "📂 Department Isolation",
            "Controlled access to Finance, HR, Marketing "
            "and Executive information."
        )

    with col5:
        card(
            "🔄 Automated CI/CD",
            "GitHub Actions for testing, Docker image building, "
            "image publishing and GitOps repository updates."
        )

    with col6:
        card(
            "☸️ Kubernetes GitOps",
            "Docker Desktop Kubernetes deployment using "
            "Argo CD and Argo Rollouts."
        )

    st.divider()

    # ======================================
    # ARCHITECTURE
    # ======================================

    st.subheader("🏗️ Solution Architecture")

    st.write(
        "End-to-end architecture covering authentication, "
        "AI-based document retrieval, security and deployment."
    )
    show_image(
        "architecture", "rbac-chatbot-architecture.png",
        caption="Enterprise RBAC Chatbot — Secure, Role-Based AI Architecture",
    )

    st.code(
        """
                    EMPLOYEE
                       |
                       v
                STREAMLIT CHATBOT
                       |
                       v
                USER AUTHENTICATION
                       |
                  bcrypt Verify
                       |
                       v
               AUTHENTICATED IDENTITY
                       |
             Department + Assigned Roles
                       |
                       v
                RBAC AUTHORIZATION
                       |
              Access Control Enforcement
                       |
                       v
              DEPARTMENT DOCUMENTS
                       |
          +------------+------------+
          |            |            |
          v            v            v
       FINANCE         HR        MARKETING
          |            |            |
          +------------+------------+
                       |
                       v
                AUTHORIZED CONTEXT
                       |
                       v
                LANGCHAIN / GROQ
                       |
                       v
                 AI RESPONSE
                       |
                       v
                  EMPLOYEE


        =========================================
                   CI/CD AND GITOPS
        =========================================

        Application GitHub Repository
                       |
                       v
                GITHUB ACTIONS
                       |
                +------+------+
                |             |
                v             v
             RBAC TESTS    DOCKER BUILD
                              |
                              v
                         DOCKER HUB
                              |
                              v
                       IMAGE TAG UPDATE
                              |
                              v
                      GITOPS REPOSITORY
                              |
                              v
                           ARGO CD
                              |
                              v
                       ARGO ROLLOUTS
                              |
                              v
                    DOCKER DESKTOP K8S
        """,
        language="text",
    )

    st.info(
        "Security principle: Authentication establishes who the "
        "user is; authorization determines which documents the "
        "user is allowed to retrieve."
    )

    st.divider()

    # ======================================
    # AUTHENTICATION AND RBAC
    # ======================================

    st.subheader("🔐 Authentication & Authorization")

    st.markdown(
        """
        **Authentication implementation**

        - User credentials maintained in `Users/users.json`.
        - Passwords stored as bcrypt hashes.
        - User configuration injected through the
          `CHATBOT_USERS_JSON` environment variable.
        - Kubernetes Secret: `chatbot-secrets`.
        - API credentials managed through Kubernetes Secrets.

        **Authorization implementation**

        - User identity is established after successful login.
        - Department and roles are returned by the authentication
          module.
        - Document retrieval must enforce the user's permitted
          department and role.
        - Unauthorized document retrieval is denied.
        """
    )

    st.code(
        """
        Kubernetes Secret: chatbot-secrets

        CHATBOT_USERS_JSON
        GROQ_API_KEY
        LANGCHAIN_API_KEY
        """,
        language="text",
    )

    st.divider()

    # ======================================
    # RBAC TEST SCENARIOS
    # ======================================

    st.subheader("🧪 RBAC Validation Scenarios")

    rbac_tests = pd.DataFrame(
        [
            [
                "Finance",
                "What is the Finance budget policy?",
                "Finance information retrieved",
                "Authorized"
            ],
            [
                "Marketing",
                "What is the Finance budget policy?",
                "No Finance document retrieved",
                "Restricted"
            ],
            [
                "HR",
                "What is the payroll policy?",
                "HR information retrieved",
                "Authorized"
            ],
            [
                "Marketing",
                "What is the payroll policy?",
                "No HR document retrieved",
                "Restricted"
            ],
            [
                "C-level",
                "What is the Finance budget policy?",
                "Finance information retrieved",
                "Authorized"
            ],
        ],
        columns=[
            "Logged-in User",
            "Question",
            "Expected Result",
            "Access"
        ]
    )

    st.dataframe(
        rbac_tests,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "These are the defined RBAC validation scenarios, "
        "not live test execution results."
    )

    st.divider()

    # ======================================
    # CI/CD PIPELINE
    # ======================================

    st.subheader("🔄 GitHub Actions CI/CD Pipeline")

    ci_stages = [
        "GitHub Checkout",
        "Python Environment Setup",
        "Dependency Installation",
        "RBAC Unit Tests",
        "Docker Build",
        "Docker Hub Authentication",
        "Docker Image Push",
        "GitOps Repository Checkout",
        "Kustomize Image Tag Update",
        "GitOps Commit and Push",
    ]

    for start in range(0, len(ci_stages), 2):

        cols = st.columns(2)

        for col, stage in zip(
            cols,
            ci_stages[start:start + 2]
        ):
            with col:
                st.markdown(
                    f"""
                    <div class="pipeline">
                        ⚙️ {stage}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.write("")

    st.markdown(
        """
        **Docker image versioning**

        Application images are tagged using the first seven
        characters of the Git commit hash.

        Example:
        """
    )

    st.code(
        """
        enterprise-rbac-chatbot:7a9f4c2
        """,
        language="text",
    )

    st.write(
        """
        The generated image tag is propagated through the
        GitHub Actions workflow and written into the GitOps
        repository's Kustomize configuration.
        """
    )

    st.divider()

    # ======================================
    # GITOPS AND KUBERNETES
    # ======================================

    st.subheader("☸️ Kubernetes Deployment & GitOps")

    deployment_components = pd.DataFrame(
        [
            [
                "Docker",
                "Container image packaging"
            ],
            [
                "Docker Hub",
                "Container image registry"
            ],
            [
                "Docker Desktop Kubernetes",
                "Local Kubernetes environment"
            ],
            [
                "Kubernetes Secrets",
                "Application credentials and user configuration"
            ],
            [
                "Argo CD",
                "GitOps-based continuous delivery"
            ],
            [
                "Argo Rollouts",
                "Progressive application rollout management"
            ],
            [
                "Kustomize",
                "Kubernetes manifest image version management"
            ],
        ],
        columns=["Technology", "Implementation"]
    )

    st.dataframe(
        deployment_components,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        """
        **Deployment workflow**

        1. GitHub Actions builds and pushes a versioned Docker image.
        2. The workflow updates `newTag` in the GitOps repository.
        3. Argo CD detects the GitOps repository change.
        4. Argo CD synchronizes the updated Kubernetes manifests.
        5. Argo Rollouts manages the configured progressive
           deployment strategy.
        """
    )

    st.divider()

    # ======================================
    # TECHNOLOGY STACK
    # ======================================

    st.subheader("🧰 Technology Stack")

    tech_left, tech_right = st.columns(2)

    with tech_left:

        st.markdown(
            """
            **Application & AI**

            - Python
            - Streamlit
            - LangChain
            - Groq LLM
            - bcrypt
            - JSON-based user configuration

            **Security**

            - Role-Based Access Control
            - Password hashing
            - Kubernetes Secrets
            - Department-level document authorization
            """
        )

    with tech_right:

        st.markdown(
            """
            **CI/CD & Containerization**

            - GitHub Actions
            - Docker
            - Docker Hub
            - Git

            **Cloud Native & GitOps**

            - Kubernetes
            - Docker Desktop
            - Argo CD
            - Argo Rollouts
            - Kustomize
            """
        )

    st.divider()

    # ======================================
    # PROJECT VALUE
    # ======================================

    st.subheader("💡 Engineering Value")

    st.write(
        """
        This project demonstrates the integration of AI
        application development with enterprise security
        requirements and modern cloud-native delivery practices.

        It brings together application authentication,
        authorization, containerization, automated testing,
        CI/CD, GitOps and progressive Kubernetes deployments
        within a single engineering solution.
        """
    )

    st.success(
        "Designed and developed by Shaikh S Huda — "
        "Platform Engineering | DevOps | DevSecOps | AI"
    )

    st.caption(
        "Enterprise RBAC Chatbot | AI Engineering | "
        "GitHub Actions | Kubernetes | GitOps"
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

st.markdown(
    f"""
    <div class="footer">
        🚀 {AUTHOR} | Engineering Command Center | {VERSION}
        <p>
            DevOps • DevSecOps • Kubernetes • Terraform • AI & MLOps
        </p>
        <p>Designed and Developed by {AUTHOR}</p>
    </div>
    """,
    unsafe_allow_html=True,
)
