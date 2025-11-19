import sys
from streamlit.web import cli as stcli
from pathlib import Path

def main():
    """
    Launcher for the Streamlit UI.
    """
    ui_path = Path(__file__).parent / "ui.py"
    # We need to mock sys.argv to make streamlit think it was called as 'streamlit run ...'
    sys.argv = ["streamlit", "run", str(ui_path)]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()

