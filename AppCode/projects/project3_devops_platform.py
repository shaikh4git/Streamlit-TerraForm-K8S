import streamlit as st
from utils.image_utils import show_image, image_path, list_images

def render():

    st.subheader("📚 Document Ingestion & Vectorization")

    show_image(
            "architecture",
            "Ingestion.png",
            caption="Document Ingestion Architecture",
        )
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
