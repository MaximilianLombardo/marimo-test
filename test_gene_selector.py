#!/usr/bin/env python3
"""Test script to verify gene selector and anatomogram work together."""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from marimo_components.anatomogram_widget import AnatomogramWidget

# Test data
expression_data = {
    "genes": {
        "TP53": {
            "UBERON_0002107": 0.72,
            "UBERON_0000955": 0.82,
            "UBERON_0002048": 0.61,
        },
        "BRCA1": {
            "UBERON_0002107": 0.45,
            "UBERON_0000955": 0.38,
            "UBERON_0002048": 0.34,
        }
    }
}

uberon_map = {
    "UBERON_0002107": "liver",
    "UBERON_0000955": "brain",
    "UBERON_0002048": "lung",
}

# Test widget creation
widget = AnatomogramWidget(
    expression_data=expression_data,
    selected_gene="TP53",
    sex="male",
    color_palette="viridis",
    scale_type="linear",
    uberon_map=uberon_map,
    threshold=0.0,
    svg_url="https://raw.githubusercontent.com/ebi-gene-expression-group/anatomogram/master/src/svg"
)

print(f"Widget created successfully!")
print(f"Selected gene: {widget.selected_gene}")
print(f"Available genes: {widget.get_available_genes()}")

# Test gene update
widget.update_gene("BRCA1")
print(f"Updated gene: {widget.selected_gene}")

print("\nTest passed!")