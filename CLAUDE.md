# CLAUDE.md - DNA2Cell Marimo Development Guidelines

This file provides context and instructions for developing the DNA2Cell Marimo interactive anatomogram project.

## Project Overview

DNA2Cell Marimo is an interactive notebook for visualizing gene expression data on anatomical diagrams. It uses Marimo for the notebook interface, AnyWidget for wrapping D3.js visualizations, and provides a reactive interface for exploring gene expression patterns.

## Development Stack

### Core Technologies
- **Python 3.12**: Main programming language
- **uv**: Fast Python package manager (10-100x faster than pip)
- **Marimo**: Interactive notebook framework
- **AnyWidget**: Custom widget framework for Jupyter/Marimo
- **D3.js v7**: Data visualization library
- **Pandas/NumPy**: Data processing

### Package Management
We use `uv` for dependency management. Key commands:
```bash
# Create virtual environment
uv venv

# Activate environment
source .venv/bin/activate

# Install dependencies
uv add package_name

# Run commands in environment
uv run command_name
```

## Key Files and Components

### Core Implementation Files
- `notebooks/anatomogram_explorer.py`: Main Marimo notebook
- `marimo_components/anatomogram_widget.py`: AnyWidget with D3.js visualization
- `marimo_components/data_processor.py`: Data loading and validation utilities
- `marimo_components/export_utils.py`: Export functionality

### Assets
- `assets/svg/homo_sapiens.male.svg`: Male anatomogram SVG
- `assets/svg/homo_sapiens.female.svg`: Female anatomogram SVG
- `sample_data/`: Example expression data files

### Configuration
- `pyproject.toml`: Project configuration and dependencies
- `uv.lock`: Locked dependency versions

## Common Commands

```bash
# Start Marimo notebook
uv run marimo edit notebooks/anatomogram_explorer.py

# Run type checking
uv run mypy .

# Format code
uv run ruff format .

# Run tests
uv run pytest

# Install new dependency
uv add package_name

# Update dependencies
uv sync
```

## Code Style Guidelines

### Python
- Use type hints for all function signatures
- Follow PEP 8 style guide
- Use descriptive variable names
- Document complex logic with inline comments

### JavaScript (in AnyWidget)
- Use modern ES6+ syntax
- Use const/let instead of var
- Use arrow functions where appropriate
- Follow D3.js conventions for data binding

### Example Python Function
```python
def process_expression_data(
    data: dict[str, Any], 
    threshold: float = 0.0
) -> tuple[pd.DataFrame, dict[str, float]]:
    """Process expression data and return filtered results.
    
    Args:
        data: Raw expression data dictionary
        threshold: Minimum expression value threshold
        
    Returns:
        Tuple of (filtered_dataframe, summary_statistics)
    """
    # Implementation here
```

## Testing Guidelines

- Write unit tests for data processing functions
- Test edge cases (empty data, invalid formats)
- Use pytest fixtures for common test data
- Aim for >80% code coverage

## Workflow Guidelines

### Adding New Features
1. Create feature branch from main
2. Implement with tests
3. Update documentation
4. Run type checking and formatting
5. Submit PR with clear description

### Debugging Tips
- Use Marimo's built-in debugging tools
- Check browser console for JavaScript errors
- Use `console.log` in AnyWidget for D3.js debugging
- Validate data format early in pipeline

## AnyWidget Development

### Structure
```javascript
_esm = """
import * as d3 from "https://cdn.skypack.dev/d3@7";

function render({ model, el }) {
    // Create visualization
    // Listen for model changes
    // Update on state change
}

export default { render };
"""
```

### State Management
- Use traitlets for Python-JavaScript synchronization
- Keep state minimal and well-defined
- Handle edge cases (null data, empty selections)

## Performance Considerations

- Lazy load large datasets
- Use efficient D3 selections
- Minimize re-renders in AnyWidget
- Cache processed data when possible

## Common Issues and Solutions

### SVG Loading Issues
- Ensure SVG files are in correct path
- Check CORS if loading from external source
- Validate SVG structure for D3 compatibility

### Data Format Errors
- Always validate data on upload
- Provide clear error messages
- Support multiple input formats

### Performance Problems
- Profile with browser dev tools
- Optimize D3 selections
- Consider data sampling for large datasets

## Future Enhancements

- WebGL rendering for large anatomograms
- Real-time collaboration features
- Additional statistical analyses
- Integration with external databases

## Important Notes

- NEVER modify the original anatomogram visualization code
- Keep AnyWidget implementation separate from Marimo logic
- Test with various data sizes and formats
- Maintain backward compatibility with data formats

## Getting Help

- Check Marimo docs: https://marimo.io/docs
- AnyWidget docs: https://anywidget.dev/
- D3.js reference: https://d3js.org/
- Project issues: GitHub repository

## Marimo Development Learnings

### Cell Output and Display

**Key Principle**: Marimo cells display the last expression evaluated, NOT return values.

#### ❌ Common Mistake: Using Return Statements
```python
@app.cell
def _(mo):
    if condition:
        widget = mo.ui.slider()
        return widget  # SyntaxError: 'return' outside function
    else:
        return mo.md("No widget")
```

#### ✅ Correct Approach: Use Last Expression
```python
@app.cell
def _(mo):
    if condition:
        output = mo.ui.slider()
    else:
        output = mo.md("No widget")
    
    output  # Last expression is displayed
```

### Reactivity Patterns

#### Pattern 1: Simple Reactive Updates
When UI elements change, dependent cells automatically re-run:

```python
# Cell 1: Create selector
@app.cell
def _(mo):
    gene_selector = mo.ui.multiselect(
        options=['TP53', 'BRCA1', 'EGFR'],
        value=['TP53'],
        max_selections=1
    )
    gene_selector
    return (gene_selector,)

# Cell 2: Use selector value (re-runs when selection changes)
@app.cell
def _(gene_selector, data):
    selected_gene = gene_selector.value[0] if gene_selector.value else None
    if selected_gene:
        display_data = data[selected_gene]
        mo.md(f"Showing data for: {selected_gene}")
    else:
        mo.md("Select a gene")
```

#### Pattern 2: Widget Updates with AnyWidget
For custom widgets, pass reactive values directly to the widget constructor:

```python
@app.cell
def _(AnatomogramWidget, gene_selector, mo):
    if gene_selector.value:
        # Widget is recreated when gene_selector changes
        widget = AnatomogramWidget(
            selected_gene=gene_selector.value[0],  # Reactive value
            expression_data=data
        )
        output = mo.ui.anywidget(widget)
    else:
        output = mo.md("Select a gene")
    
    output
```

### Common Pitfalls and Solutions

#### 1. Conditional Display with Multiple Outputs
**Problem**: Trying to display different things based on conditions

**Solution**: Assign to a variable, then display:
```python
@app.cell
def _(condition, mo):
    # Determine what to display
    if condition:
        output = create_complex_widget()
    else:
        output = mo.md("Condition not met")
    
    # Display the output
    output
```

#### 2. Empty Returns in Cells
**Problem**: Using `return` without a value
```python
return  # SyntaxError in Marimo cells
```

**Solution**: Return needed values or omit return entirely:
```python
return (var1, var2)  # If other cells need these
# OR just display without return
widget_ui  # Display and end cell
```

#### 3. Widget Not Updating
**Problem**: Widget doesn't update when inputs change

**Solution**: Ensure the cell creating the widget depends on reactive elements:
```python
@app.cell
def _(selector, AnatomogramWidget, mo):  # selector in function signature!
    # Cell re-runs when selector changes
    widget = AnatomogramWidget(data=selector.value)
    mo.ui.anywidget(widget)
```

### Best Practices

1. **Explicit Dependencies**: Always include UI elements in cell function signatures
2. **Single Output**: Each cell should have one clear output (the last expression)
3. **Conditional Logic**: Use variable assignment for conditional displays
4. **State Management**: Let Marimo handle state through cell dependencies
5. **Debugging**: Use `print()` statements to trace execution in Marimo logs

### Example: Complete Reactive Pattern
```python
# Cell 1: UI Control
@app.cell
def _(mo):
    control = mo.ui.slider(start=0, stop=100, value=50)
    control
    return (control,)

# Cell 2: Dependent Visualization
@app.cell
def _(control, visualize_data):
    # This cell re-runs whenever control.value changes
    threshold = control.value
    
    if threshold > 25:
        output = visualize_data(threshold)
    else:
        output = mo.md(f"Threshold too low: {threshold}")
    
    output  # Display the result
```

### Troubleshooting Checklist

- [ ] Check for `return` statements in cells (remove them)
- [ ] Ensure reactive elements are in cell dependencies
- [ ] Use variable assignment for conditional outputs
- [ ] Verify last expression is what you want to display
- [ ] Check browser console for JavaScript errors (for widgets)
- [ ] Use `print()` to debug execution flow