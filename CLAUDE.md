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