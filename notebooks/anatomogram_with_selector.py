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

    return AnatomogramWidget, mo


@app.cell
def _(mo):
    mo.md(
        """
    # 🧬 Anatomogram Explorer with Gene Selector

    Select different genes to visualize their expression patterns on the anatomogram.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    # Hardcoded sample expression data with multiple genes
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
            },
            "BRCA1": {
                "UBERON_0002107": 0.45,
                "UBERON_0000955": 0.38,
                "UBERON_0002106": 0.52,
                "UBERON_0001264": 0.41,
                "UBERON_0000992": 0.89,
                "UBERON_0002048": 0.34,
                "UBERON_0002113": 0.48,
                "UBERON_0002108": 0.31,
                "UBERON_0001155": 0.29,
                "UBERON_0001255": 0.56,
                "UBERON_0002367": 0.37,
                "UBERON_0000995": 0.42,
                "UBERON_0002110": 0.61,
                "UBERON_0000945": 0.33,
                "UBERON_0001043": 0.28,
                "UBERON_0002046": 0.75,
                "UBERON_0002369": 0.81,
                "UBERON_0001630": 0.22,
                "UBERON_0002097": 0.36,
                "UBERON_0001013": 0.19,
                "UBERON_0000178": 0.43,
                "UBERON_0001987": 0.92,
                "UBERON_0002412": 0.27,
                "UBERON_0003889": 0.95,
                "UBERON_0001474": 0.15,
                "UBERON_0000007": 0.49,
                "UBERON_0002298": 0.32,
                "UBERON_0001637": 0.38,
                "UBERON_0000956": 0.41,
                "UBERON_0001897": 0.36,
                "UBERON_0001870": 0.39,
                "UBERON_0001876": 0.44,
                "UBERON_0001898": 0.47,
                "UBERON_0000974": 0.35,
                "UBERON_0000977": 0.51,
                "UBERON_0000948": 0.46,
                "UBERON_0000310": 0.88,
                "UBERON_0000029": 0.54,
                "UBERON_0002371": 0.62,
                "UBERON_0001134": 0.29,
                "UBERON_0001981": 0.42,
                "UBERON_0001871": 0.37,
                "UBERON_0000451": 0.31,
                "UBERON_0006618": 0.48,
                "UBERON_0000947": 0.52,
                "UBERON_0001621": 0.44,
                "UBERON_0007650": 0.39
            },
            "EGFR": {
                "UBERON_0002107": 0.31,
                "UBERON_0000955": 0.95,
                "UBERON_0002106": 0.22,
                "UBERON_0001264": 0.18,
                "UBERON_0000992": 0.27,
                "UBERON_0002048": 0.88,
                "UBERON_0002113": 0.42,
                "UBERON_0002108": 0.76,
                "UBERON_0001155": 0.81,
                "UBERON_0001255": 0.35,
                "UBERON_0002367": 0.29,
                "UBERON_0000995": 0.51,
                "UBERON_0002110": 0.46,
                "UBERON_0000945": 0.73,
                "UBERON_0001043": 0.67,
                "UBERON_0002046": 0.39,
                "UBERON_0002369": 0.44,
                "UBERON_0001630": 0.58,
                "UBERON_0002097": 0.92,
                "UBERON_0001013": 0.86,
                "UBERON_0000178": 0.24,
                "UBERON_0001987": 0.33,
                "UBERON_0002412": 0.41,
                "UBERON_0003889": 0.28,
                "UBERON_0001474": 0.52,
                "UBERON_0000007": 0.36,
                "UBERON_0002298": 0.89,
                "UBERON_0001637": 0.71,
                "UBERON_0000956": 0.93,
                "UBERON_0001897": 0.85,
                "UBERON_0001870": 0.91,
                "UBERON_0001876": 0.87,
                "UBERON_0001898": 0.79,
                "UBERON_0000974": 0.64,
                "UBERON_0000977": 0.48,
                "UBERON_0000948": 0.37,
                "UBERON_0000310": 0.55,
                "UBERON_0000029": 0.62,
                "UBERON_0002371": 0.31,
                "UBERON_0001134": 0.69,
                "UBERON_0001981": 0.75,
                "UBERON_0001871": 0.84,
                "UBERON_0000451": 0.96,
                "UBERON_0006618": 0.43,
                "UBERON_0000947": 0.59,
                "UBERON_0001621": 0.47,
                "UBERON_0007650": 0.65
            },
            "MYC": {
                "UBERON_0002107": 0.91,
                "UBERON_0000955": 0.67,
                "UBERON_0002106": 0.84,
                "UBERON_0001264": 0.72,
                "UBERON_0000992": 0.53,
                "UBERON_0002048": 0.79,
                "UBERON_0002113": 0.86,
                "UBERON_0002108": 0.58,
                "UBERON_0001155": 0.64,
                "UBERON_0001255": 0.45,
                "UBERON_0002367": 0.71,
                "UBERON_0000995": 0.62,
                "UBERON_0002110": 0.38,
                "UBERON_0000945": 0.55,
                "UBERON_0001043": 0.49,
                "UBERON_0002046": 0.83,
                "UBERON_0002369": 0.76,
                "UBERON_0001630": 0.41,
                "UBERON_0002097": 0.69,
                "UBERON_0001013": 0.32,
                "UBERON_0000178": 0.88,
                "UBERON_0001987": 0.51,
                "UBERON_0002412": 0.73,
                "UBERON_0003889": 0.46,
                "UBERON_0001474": 0.37,
                "UBERON_0000007": 0.94,
                "UBERON_0002298": 0.78,
                "UBERON_0001637": 0.56,
                "UBERON_0000956": 0.82,
                "UBERON_0001897": 0.75,
                "UBERON_0001870": 0.81,
                "UBERON_0001876": 0.77,
                "UBERON_0001898": 0.89,
                "UBERON_0000974": 0.61,
                "UBERON_0000977": 0.68,
                "UBERON_0000948": 0.92,
                "UBERON_0000310": 0.43,
                "UBERON_0000029": 0.74,
                "UBERON_0002371": 0.85,
                "UBERON_0001134": 0.52,
                "UBERON_0001981": 0.66,
                "UBERON_0001871": 0.48,
                "UBERON_0000451": 0.87,
                "UBERON_0006618": 0.63,
                "UBERON_0000947": 0.7,
                "UBERON_0001621": 0.95,
                "UBERON_0007650": 0.59
            },
            "PTEN": {
                "UBERON_0002107": 0.55,
                "UBERON_0000955": 0.78,
                "UBERON_0002106": 0.42,
                "UBERON_0001264": 0.65,
                "UBERON_0000992": 0.71,
                "UBERON_0002048": 0.49,
                "UBERON_0002113": 0.63,
                "UBERON_0002108": 0.37,
                "UBERON_0001155": 0.44,
                "UBERON_0001255": 0.58,
                "UBERON_0002367": 0.82,
                "UBERON_0000995": 0.29,
                "UBERON_0002110": 0.53,
                "UBERON_0000945": 0.47,
                "UBERON_0001043": 0.61,
                "UBERON_0002046": 0.35,
                "UBERON_0002369": 0.68,
                "UBERON_0001630": 0.75,
                "UBERON_0002097": 0.31,
                "UBERON_0001013": 0.46,
                "UBERON_0000178": 0.59,
                "UBERON_0001987": 0.73,
                "UBERON_0002412": 0.38,
                "UBERON_0003889": 0.66,
                "UBERON_0001474": 0.41,
                "UBERON_0000007": 0.84,
                "UBERON_0002298": 0.72,
                "UBERON_0001637": 0.54,
                "UBERON_0000956": 0.76,
                "UBERON_0001897": 0.69,
                "UBERON_0001870": 0.85,
                "UBERON_0001876": 0.91,
                "UBERON_0001898": 0.88,
                "UBERON_0000974": 0.43,
                "UBERON_0000977": 0.57,
                "UBERON_0000948": 0.51,
                "UBERON_0000310": 0.64,
                "UBERON_0000029": 0.48,
                "UBERON_0002371": 0.79,
                "UBERON_0001134": 0.62,
                "UBERON_0001981": 0.56,
                "UBERON_0001871": 0.74,
                "UBERON_0000451": 0.83,
                "UBERON_0006618": 0.45,
                "UBERON_0000947": 0.67,
                "UBERON_0001621": 0.52,
                "UBERON_0007650": 0.77
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

    # Get list of available genes
    available_genes = list(expression_data['genes'].keys())

    mo.md(f"""
    ### Data loaded:
    - **Available genes:** {', '.join(available_genes)}
    - **Total genes:** {len(available_genes)}
    - **Tissues per gene:** {len(expression_data['genes'][available_genes[0]])}
    """)

    return available_genes, expression_data, uberon_map


@app.cell
def _(mo):
    mo.md("""## 🎛️ Gene Selector""")
    return


@app.cell
def _(available_genes, mo):
    # Create searchable gene selector using multiselect with max_selections=1
    gene_selector = mo.ui.multiselect(
        options=available_genes,
        value=[available_genes[0]],
        label="🔍 Search and select a gene",
        max_selections=1
    )

    gene_selector
    return (gene_selector,)


@app.cell
def _(expression_data, gene_selector, mo):
    if gene_selector.value and len(gene_selector.value) > 0:
        selected_gene = gene_selector.value[0]  # Get first (and only) selected gene
        gene_data = expression_data['genes'][selected_gene]
        values = list(gene_data.values())

        stats_md = mo.md(f"""
        ### Selected Gene: **{selected_gene}**
        - Expression range: {min(values):.2f} - {max(values):.2f}
        - Mean expression: {sum(values)/len(values):.2f}
        - Tissues with expression > 0.5: {sum(1 for v in values if v > 0.5)}
        """)
    else:
        selected_gene = None
        gene_data = None
        values = None
        stats_md = mo.md("*Select a gene to see statistics*")
    
    stats_md
    return gene_data, selected_gene, stats_md, values


@app.cell
def _(mo):
    mo.md("""## 🫁 Anatomogram Visualization""")
    return


@app.cell
def _(AnatomogramWidget, expression_data, gene_selector, mo, uberon_map):
    if gene_selector.value and len(gene_selector.value) > 0:
        # Use GitHub-hosted SVG files
        svg_base_url = "https://raw.githubusercontent.com/ebi-gene-expression-group/anatomogram/master/src/svg"

        # Create the anatomogram widget with reactive binding
        anatomogram = AnatomogramWidget(
            expression_data=expression_data,
            selected_gene=gene_selector.value[0],  # Get first (and only) selected gene
            sex="male",
            color_palette="viridis",
            scale_type="linear",
            uberon_map=uberon_map,
            threshold=0.0,
            svg_url=svg_base_url
        )

        # Create and explicitly return the widget UI for display
        return mo.ui.anywidget(anatomogram)
    else:
        # Return the markdown message if no gene is selected
        return mo.md("*Select a gene to view the anatomogram*")


if __name__ == "__main__":
    app.run()
