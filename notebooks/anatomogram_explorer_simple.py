import marimo

__generated_with = "0.14.16"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import json
    from pathlib import Path
    import sys

    # Add parent directory to path for imports
    sys.path.append(str(Path(__file__).parent.parent))

    from marimo_components.anatomogram_widget import AnatomogramWidget
    from marimo_components.data_processor import ExpressionDataProcessor

    return AnatomogramWidget, mo


@app.cell
def _(mo):
    mo.md(
        """
    # 🧬 Simple Anatomogram Explorer

    This is a simplified version to test the anatomogram visualization.
    """
    )
    return


@app.cell
def _(mo):
    # Hardcoded sample expression data
    expression_data = {
        "genes": {
            "TP53": {
                "UBERON_0002107": 0.72,
                "UBERON_0000955": 0.82,
                "UBERON_0002106": 0.68,
                "UBERON_0001264": 0.58,
                "UBERON_0000992": 0.42,
                "UBERON_0002048": 0.61,
                "UBERON_0002113": 0.7,
                "UBERON_0002108": 0.45,
                "UBERON_0001155": 0.52,
                "UBERON_0001255": 0.38,
                "UBERON_0002367": 0.65,
                "UBERON_0000995": 0.48,
                "UBERON_0002110": 0.35,
                "UBERON_0000945": 0.4,
                "UBERON_0001043": 0.55,
                "UBERON_0002046": 0.62,
                "UBERON_0002369": 0.68,
                "UBERON_0001630": 0.3,
                "UBERON_0002097": 0.45,
                "UBERON_0001013": 0.25,
                "UBERON_0000178": 0.85,
                "UBERON_0001987": 0.42,
                "UBERON_0002412": 0.5,
                "UBERON_0003889": 0.38,
                "UBERON_0001474": 0.2,
                "UBERON_0000007": 0.78,
                "UBERON_0002298": 0.65,
                "UBERON_0001637": 0.48,
                "UBERON_0000956": 0.88,
                "UBERON_0001897": 0.9,
                "UBERON_0001870": 0.75,
                "UBERON_0001876": 0.82,
                "UBERON_0001898": 0.85,
                "UBERON_0000974": 0.52,
                "UBERON_0000977": 0.73,
                "UBERON_0000948": 0.76,
                "UBERON_0000310": 0.71,
                "UBERON_0000029": 0.38,
                "UBERON_0002371": 0.51,
                "UBERON_0001134": 0.57,
                "UBERON_0001981": 0.67,
                "UBERON_0001871": 0.4,
                "UBERON_0000451": 0.64,
                "UBERON_0006618": 0.5,
                "UBERON_0000947": 0.6,
                "UBERON_0001621": 0.77,
                "UBERON_0007650": 0.58
            }
        }
    }

    # Simple UBERON mapping
    uberon_map = {
        "UBERON_0002107": "liver",
        "UBERON_0000955": "brain",
        "UBERON_0002106": "spleen",
        "UBERON_0001264": "pancreas",
        "UBERON_0000992": "ovary",
        "UBERON_0002048": "lung",
        "UBERON_0002113": "kidney",
        "UBERON_0002108": "small intestine",
        "UBERON_0001155": "colon",
        "UBERON_0001255": "urinary bladder",
        "UBERON_0002367": "prostate gland",
        "UBERON_0000995": "pericardium",
        "UBERON_0002110": "gall bladder",
        "UBERON_0000945": "stomach",
        "UBERON_0001043": "esophagus",
        "UBERON_0002046": "thyroid gland",
        "UBERON_0002369": "adrenal gland",
        "UBERON_0001630": "muscle",
        "UBERON_0002097": "skin",
        "UBERON_0001013": "adipose tissue",
        "UBERON_0000178": "blood",
        "UBERON_0001987": "placenta",
        "UBERON_0002412": "vertebra",
        "UBERON_0003889": "fallopian tube",
        "UBERON_0001474": "bone tissue",
        "UBERON_0000007": "pituitary gland",
        "UBERON_0002298": "brainstem",
        "UBERON_0001637": "artery",
        "UBERON_0000956": "cerebral cortex",
        "UBERON_0001897": "dorsal root ganglion",
        "UBERON_0001870": "frontal cortex",
        "UBERON_0001876": "amygdala",
        "UBERON_0001898": "hypothalamus",
        "UBERON_0000974": "neck",
        "UBERON_0000977": "pleura",
        "UBERON_0000948": "heart",
        "UBERON_0000310": "breast",
        "UBERON_0000029": "lymph node",
        "UBERON_0002371": "bone marrow",
        "UBERON_0001134": "skeletal muscle tissue",
        "UBERON_0001981": "blood vessel",
        "UBERON_0001871": "temporal lobe",
        "UBERON_0000451": "prefrontal cortex",
        "UBERON_0006618": "atrium auricular region",
        "UBERON_0000947": "aorta",
        "UBERON_0001621": "coronary artery",
        "UBERON_0007650": "esophagogastric junction"
    }

    mo.md(f"""
    ### Data loaded:
    - Gene: TP53
    - Tissues: {len(expression_data['genes']['TP53'])}
    - Expression range: {min(expression_data['genes']['TP53'].values()):.2f} - {max(expression_data['genes']['TP53'].values()):.2f}
    """)

    return expression_data, uberon_map


@app.cell
def _(mo):
    mo.md("""## 🫁 Anatomogram Visualization""")
    return


@app.cell
def _(AnatomogramWidget, expression_data, mo, uberon_map):
    # Use GitHub-hosted SVG files
    svg_base_url = "https://raw.githubusercontent.com/ebi-gene-expression-group/anatomogram/master/src/svg"

    # Create the anatomogram widget
    anatomogram = AnatomogramWidget(
        expression_data=expression_data,
        selected_gene="TP53",
        sex="male",
        color_palette="viridis",
        scale_type="linear",
        uberon_map=uberon_map,
        threshold=0.0,
        svg_url=svg_base_url
    )

    # Display debug info
    mo.md(f"""
    ### Debug Info:
    - SVG URL: {svg_base_url}
    - Selected gene: TP53
    - Number of tissues: {len(expression_data['genes']['TP53'])}
    """)

    # Create the widget
    widget_ui = mo.ui.anywidget(anatomogram)

    # Display it
    widget_ui
    return


if __name__ == "__main__":
    app.run()
