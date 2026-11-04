from streamlit.testing.v1 import AppTest
from pathlib import Path

def test_streamlit_app():
    app_path = Path(__file__).resolve().parent.parent / "app.py"
    
    at = AppTest.from_file(app_path)
    at.run(timeout=10)

    assert not at.exception