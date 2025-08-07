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

    # Initialize the data processor
    processor = ExpressionDataProcessor()
    return AnatomogramWidget, Path, json, mo, pd, processor


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    # 🧬 Interactive Anatomogram Explorer

    This notebook allows you to:
    - Upload and visualize gene expression data on human anatomograms
    - Explore expression patterns across different tissues
    - Compare gene expression between male and female anatomograms
    - Perform statistical analysis on expression data
    - Export visualizations and processed data

    ## Getting Started
    1. Upload your expression data (JSON or CSV format)
    2. Select genes and visualization parameters
    3. Explore the interactive anatomogram
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""## 📁 Data Upload""")
    return


@app.cell(hide_code=True)
def _(mo):
    expression_file = mo.ui.file(
        filetypes=[".json", ".csv", ".tsv"],
        label="Upload Expression Data (JSON, CSV, or TSV format)"
    )

    uberon_file = mo.ui.file(
        filetypes=[".json"],
        label="Upload UBERON Mapping - Optional (JSON format)"
    )

    # Display file upload widgets
    mo.vstack([expression_file, uberon_file])
    return expression_file, uberon_file


@app.cell
def _(mo):
    use_sample_data = mo.ui.checkbox(label="Use sample data")

    mo.vstack([
        mo.md("Don't have data? Check the box above to use sample data."),
        use_sample_data
    ])
    return (use_sample_data,)


@app.cell
def _(
    Path,
    expression_file,
    json,
    mo,
    processor,
    uberon_file,
    use_sample_data,
):
    expression_data = None
    uberon_map = None
    available_genes = []
    tissue_list = set()
    data_loaded = False
    error_message = ""

    # Load UBERON mapping
    if uberon_file.value:
        try:
            uberon_content = uberon_file.value[0].content
            uberon_map = json.loads(uberon_content.decode('utf-8'))
        except Exception as e:
            error_message = f"Error loading UBERON mapping: {str(e)}"

    # Use default UBERON mapping if none provided
    if not uberon_map:
        # Try to load default mapping
        default_uberon_path = Path(__file__).parent.parent / "sample_data" / "uberon_id_map.json"
        if default_uberon_path.exists():
            try:
                with open(default_uberon_path, 'r') as f:
                    uberon_map = json.load(f)
            except:
                uberon_map = {}

    # Load expression data
    if use_sample_data.value:
        # Load sample data
        sample_data_path = Path(__file__).parent.parent / "sample_data" / "expression_data.json"
        if sample_data_path.exists():
            try:
                with open(sample_data_path, 'r') as f:
                    expression_data = json.load(f)
                data_loaded = True
            except Exception as e:
                error_message = f"Error loading sample data: {str(e)}"
        else:
            error_message = "Sample data file not found"
    elif expression_file.value:
        try:
            file_info = expression_file.value[0]
            expression_data = processor.load_file(
                file_info.content,
                file_info.name
            )
            data_loaded = True
        except Exception as e:
            error_message = f"Error loading file: {str(e)}"

    # Validate and process data
    if expression_data and data_loaded:
        is_valid, validation_message = processor.validate_format(expression_data)

        if is_valid:
            available_genes = processor.get_gene_list(expression_data)
            tissue_list = processor.get_tissue_list(expression_data)
            stats = processor.get_summary_statistics(expression_data)

            # Create a preview of the data
            preview_data = []
            for gene in available_genes[:10]:  # Show first 10 genes
                gene_tissues = expression_data['genes'][gene]
                # Get first 5 tissues for each gene
                for tissue, value in list(gene_tissues.items())[:5]:
                    tissue_name = uberon_map.get(tissue, tissue) if uberon_map else tissue
                    preview_data.append({
                        "Gene": gene,
                        "Tissue ID": tissue,
                        "Tissue Name": tissue_name,
                        "Expression": value
                    })
            
            preview_df = pd.DataFrame(preview_data)

            output = mo.vstack([
                mo.md(f"""
                ✅ **Data loaded successfully!**

                - **Genes:** {stats['num_genes']}
                - **Tissues:** {stats['num_tissues']}
                - **Mean expression:** {stats['mean_expression']:.3f}
                - **Expression range:** [{stats['min_expression']:.3f}, {stats['max_expression']:.3f}]
                - **Sample genes:** {', '.join(available_genes[:5])}{'...' if len(available_genes) > 5 else ''}
                """).callout(kind="success"),
                mo.md("### Data Preview (first 10 genes, 5 tissues each)"),
                mo.plain(preview_df)
            ])
        else:
            error_message = f"Data validation failed: {validation_message}"
            data_loaded = False

    if error_message:
        output = mo.md(f"❌ **Error:** {error_message}").callout(kind="danger")
    elif not data_loaded and not error_message:
        output = mo.md("👆 Please upload expression data or use sample data to begin").callout(kind="info")

    # Display the output
    if 'output' in locals():
        output

    return available_genes, data_loaded, expression_data, uberon_map


@app.cell
def _(mo):
    mo.md("""## 📋 Available Genes""")
    return


@app.cell
def _(available_genes, data_loaded, expression_data, mo, pd):
    if data_loaded and available_genes:
        # Create a table of all genes with their expression summary
        gene_summary = []
        for gene in available_genes:
            gene_data = expression_data['genes'][gene]
            values = list(gene_data.values())
            gene_summary.append({
                "Gene": gene,
                "Tissues": len(gene_data),
                "Min Expression": min(values) if values else 0,
                "Max Expression": max(values) if values else 0,
                "Mean Expression": sum(values)/len(values) if values else 0
            })
        
        gene_df = pd.DataFrame(gene_summary)
        
        mo.vstack([
            mo.md(f"**Total genes available: {len(available_genes)}**"),
            mo.ui.table(gene_df, show_column_actions=True, search=True)
        ])
    else:
        mo.md("*Gene list will appear after data is loaded*")
    return gene_df if 'gene_df' in locals() else None


@app.cell
def _(mo):
    mo.md("""## 🎛️ Visualization Controls""")
    return


@app.cell
def _(available_genes, data_loaded, mo):
    # Only show controls if data is loaded
    if data_loaded and available_genes:
        gene_selector = mo.ui.dropdown(
            options={gene: gene for gene in available_genes},
            value=available_genes[0],
            label="Select Gene"
        )

        sex_selector = mo.ui.radio(
            options={"male": "Male", "female": "Female"},
            value="male",
            label="Anatomogram View"
        )

        color_palette = mo.ui.dropdown(
            options={
                "viridis": "Viridis",
                "magma": "Magma", 
                "inferno": "Inferno",
                "plasma": "Plasma",
                "turbo": "Turbo",
                "cividis": "Cividis",
                "warm": "Warm",
                "cool": "Cool"
            },
            value="viridis",
            label="Color Palette"
        )

        scale_type = mo.ui.radio(
            options={"linear": "Linear", "log": "Logarithmic"},
            value="linear",
            label="Scale Type"
        )

        threshold_slider = mo.ui.slider(
            start=0,
            stop=1,
            step=0.01,
            value=0,
            label="Expression Threshold"
        )

        # Display controls in a grid
        mo.hstack([
            mo.vstack([gene_selector, sex_selector]),
            mo.vstack([color_palette, scale_type]),
            threshold_slider
        ])
    else:
        mo.md("*Controls will appear after data is loaded*")
        gene_selector = None
        sex_selector = None
        color_palette = None
        scale_type = None
        threshold_slider = None

    return (
        color_palette,
        gene_selector,
        scale_type,
        sex_selector,
        threshold_slider,
    )


@app.cell
def _(mo):
    mo.md("""## 🫁 Anatomogram Visualization""")
    return


@app.cell
def _(
    AnatomogramWidget,
    available_genes,
    color_palette,
    data_loaded,
    expression_data,
    gene_selector,
    mo,
    scale_type,
    sex_selector,
    threshold_slider,
    uberon_map,
):
    if data_loaded and available_genes and gene_selector and gene_selector.value:
        # Use GitHub-hosted SVG files
        svg_base_url = "https://raw.githubusercontent.com/ebi-gene-expression-group/anatomogram/master/src/svg"

        # Debug info
        debug_info = mo.md(f"""
        ### Debug Info:
        - Data loaded: {data_loaded}
        - Selected gene: {gene_selector.value}
        - Sex: {sex_selector.value if sex_selector else 'None'}
        - SVG URL: {svg_base_url}
        - Expression data keys: {list(expression_data.keys()) if expression_data else 'None'}
        - Number of tissues for selected gene: {len(expression_data['genes'].get(gene_selector.value, {})) if expression_data and 'genes' in expression_data else 0}
        """).callout(kind="info")

        # Create the anatomogram widget
        anatomogram = AnatomogramWidget(
            expression_data=expression_data,
            selected_gene=gene_selector.value,
            sex=sex_selector.value if sex_selector and sex_selector.value else "male",
            color_palette=color_palette.value if color_palette and color_palette.value else "viridis",
            scale_type=scale_type.value if scale_type and scale_type.value else "linear",
            uberon_map=uberon_map or {},
            threshold=threshold_slider.value if threshold_slider and threshold_slider.value is not None else 0.0,
            svg_url=svg_base_url  # GitHub URL
        )

        # Create the bound widget with reactive updates
        widget_ui = mo.ui.anywidget(
            anatomogram,
            selected_gene=gene_selector.value,
            sex=sex_selector.value if sex_selector else "male",
            color_palette=color_palette.value if color_palette else "viridis",
            scale_type=scale_type.value if scale_type else "linear",
            threshold=threshold_slider.value if threshold_slider else 0.0
        )

        # Display the widget
        return mo.vstack([
            debug_info,
            widget_ui,
            mo.md(f"*Viewing gene: **{gene_selector.value}** | Sex: **{sex_selector.value if sex_selector else 'N/A'}** | Threshold: **{threshold_slider.value if threshold_slider else 0:.2f}***")
        ])
    else:
        return mo.md("*Anatomogram will appear after data is loaded*")


@app.cell
def _(mo):
    mo.md("""## 📊 Expression Analysis""")
    return


@app.cell
def _(
    available_genes,
    color_palette,
    data_loaded,
    expression_data,
    gene_selector,
    mo,
    pd,
    threshold_slider,
    uberon_map,
):
    if data_loaded and available_genes and gene_selector and gene_selector.value:
        selected_gene = gene_selector.value
        gene_data = expression_data['genes'].get(selected_gene, {})

        # Filter by threshold
        threshold = threshold_slider.value
        filtered_data = {k: v for k, v in gene_data.items() if v >= threshold}

        if filtered_data:
            # Create expression summary
            df = pd.DataFrame([
                {
                    "Tissue": uberon_map.get(k, k) if uberon_map else k,
                    "UBERON ID": k,
                    "Expression": v
                }
                for k, v in filtered_data.items()
            ]).sort_values("Expression", ascending=False)

            # Summary statistics
            mo.md(f"""
            ### Gene: {selected_gene}
            - **Total tissues with expression ≥ {threshold}:** {len(filtered_data)}
            - **Mean expression:** {df['Expression'].mean():.3f}
            - **Std deviation:** {df['Expression'].std():.3f}
            - **Max expression:** {df['Expression'].max():.3f}
            - **Min expression:** {df['Expression'].min():.3f}
            """)

            # Top expressed tissues
            mo.md("#### Top 10 Expressed Tissues")
            mo.plain(df.head(10))

            # Create a bar chart of top tissues
            if len(df) > 0:
                try:
                    import altair as alt

                    # Take top 20 tissues for visualization
                    top_tissues = df.head(20)

                    chart = alt.Chart(top_tissues).mark_bar().encode(
                        x=alt.X('Expression:Q', title='Expression Level'),
                        y=alt.Y('Tissue:N', sort='-x', title='Tissue'),
                        color=alt.Color('Expression:Q', scale=alt.Scale(scheme=color_palette.value)),
                        tooltip=['Tissue', 'UBERON ID', 'Expression']
                    ).properties(
                        width=600,
                        height=min(400, len(top_tissues) * 20),
                        title=f'Top {len(top_tissues)} Tissues - {selected_gene}'
                    )

                    mo.ui.altair_chart(chart)
                except ImportError:
                    mo.md("*Install altair to see expression charts*")
        else:
            mo.md(f"*No tissues with expression ≥ {threshold} for gene {selected_gene}*")

    return


@app.cell
def _(mo):
    mo.md("""## 💾 Export Options""")
    return


@app.cell
def _(
    available_genes,
    data_loaded,
    expression_data,
    gene_selector,
    json,
    mo,
    pd,
    threshold_slider,
):
    # Initialize variables
    export_filtered_data = None
    export_current_gene = None
    export_filtered_button = None
    export_gene_button = None
    
    if data_loaded and gene_selector and gene_selector.value:
        # Export filtered data
        def export_filtered_data():
            if not gene_selector.value:
                return None

            filtered = {
                "genes": {},
                "metadata": {
                    "threshold": threshold_slider.value,
                    "selected_gene": gene_selector.value,
                    "total_genes": len(available_genes),
                    "export_date": pd.Timestamp.now().isoformat()
                }
            }

            # Apply threshold filter
            for gene, tissues in expression_data['genes'].items():
                filtered_tissues = {k: v for k, v in tissues.items() if v >= threshold_slider.value}
                if filtered_tissues:
                    filtered["genes"][gene] = filtered_tissues

            return json.dumps(filtered, indent=2)

        # Export current gene data
        def export_current_gene():
            if not gene_selector.value:
                return None

            gene_export = {
                "gene": gene_selector.value,
                "expression_data": expression_data['genes'].get(gene_selector.value, {}),
                "metadata": {
                    "total_tissues": len(expression_data['genes'].get(gene_selector.value, {})),
                    "threshold": threshold_slider.value,
                    "export_date": pd.Timestamp.now().isoformat()
                }
            }

            return json.dumps(gene_export, indent=2)

        # Create download buttons
        export_filtered_button = mo.ui.button(label="Export Filtered Data")
        export_gene_button = mo.ui.button(label="Export Current Gene")

        # Handle downloads on button click
        if export_filtered_button.value:
            mo.download(
                data=export_filtered_data(),
                filename=f"filtered_expression_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

        if export_gene_button.value:
            mo.download(
                data=export_current_gene(),
                filename=f"{gene_selector.value}_expression_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

        mo.hstack([export_filtered_button, export_gene_button])
    else:
        mo.md("*Export options will be available after data is loaded*")
    
    return


if __name__ == "__main__":
    app.run()
