import streamlit as st
from pathlib import Path

IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"

IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".webp"}


def image_path(*parts: str) -> Path:
    return IMAGES_DIR.joinpath(*parts)


def list_images(folder: str) -> list[Path]:
    directory = IMAGES_DIR / folder

    if not directory.is_dir():
        return []

    return sorted(
        p for p in directory.iterdir()
        if p.suffix.lower() in IMAGE_TYPES
    )


def show_image(*parts: str, caption: str = "") -> None:
    path = image_path(*parts)

    if path.exists():
        st.image(
            str(path),
            caption=caption,
            use_container_width=True
        )
    else:
        st.info(
            f"Add {'/'.join(parts)} to AppCode/images/ to display it."
        )