"""AnyWidget implementation for anatomogram visualization."""

import anywidget
import traitlets
from pathlib import Path


class AnatomogramWidget(anywidget.AnyWidget):
    """Interactive anatomogram visualization widget using D3.js."""
    _version = "0.1.1"  # Increment to force reload
    
    # CSS styling for the widget
    _css = """
    .anatomogram-widget-container {
        width: 100%;
        height: 100%;
        position: relative;
        background-color: white;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .anatomogram-container {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: auto;
    }
    
    .anatomogram-container svg {
        width: 100%;
        height: auto;
        max-width: 600px;
        max-height: 90vh;
    }
    
    .anatomogram-container svg path,
    .anatomogram-container svg circle,
    .anatomogram-container svg rect,
    .anatomogram-container svg polygon,
    .anatomogram-container svg ellipse {
        fill: #E0E0E0;
        stroke: white;
        stroke-width: 0.5;
        transition: opacity 0.2s;
        cursor: pointer;
    }
    
    .anatomogram-container svg path:hover,
    .anatomogram-container svg circle:hover,
    .anatomogram-container svg rect:hover,
    .anatomogram-container svg polygon:hover,
    .anatomogram-container svg ellipse:hover {
        opacity: 0.8;
        stroke: #333;
        stroke-width: 1;
    }
    
    .anatomogram-tooltip {
        position: absolute;
        display: none;
        background-color: rgba(0, 0, 0, 0.9);
        color: white;
        padding: 10px 15px;
        border-radius: 4px;
        font-size: 14px;
        pointer-events: none;
        z-index: 1000;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
    }
    
    .anatomogram-tooltip::after {
        content: '';
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: rgba(0, 0, 0, 0.9) transparent transparent transparent;
    }
    
    .tissue-name {
        font-weight: 600;
        margin-bottom: 4px;
    }
    
    .expression-value {
        font-size: 12px;
        color: #ccc;
    }
    
    .loading-message {
        text-align: center;
        padding: 40px;
        font-size: 18px;
        color: #666;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
    }
    
    .error-message {
        text-align: center;
        padding: 40px;
        font-size: 16px;
        color: #d32f2f;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
    }
    """
    
    # JavaScript implementation with D3
    _esm = """
    import * as d3 from "https://cdn.skypack.dev/d3@7";
    
    export default {
        render({ model, el }) {
            console.log('AnatomogramWidget render called');
            console.log('Model:', model);
            console.log('Element:', el);
            
            // Create main container
            const mainContainer = document.createElement('div');
            mainContainer.className = 'anatomogram-widget-container';
            el.appendChild(mainContainer);
            
            const container = d3.select(mainContainer)
                .append("div")
                .attr("class", "anatomogram-container");
            
            let currentSvg = null;
            let tooltip = null;
            
            // Initialize tooltip
            function initTooltip() {
                tooltip = d3.select(mainContainer)
                    .append("div")
                    .attr("class", "anatomogram-tooltip")
                    .style("display", "none");
            }
            
            // Show loading message
            function showLoading(message = 'Loading anatomogram...') {
                container.html(`<div class="loading-message">${message}</div>`);
            }
            
            // Show error message
            function showError(message) {
                container.html(`<div class="error-message">Error: ${message}</div>`);
            }
            
            // Load SVG based on sex
            async function loadAnatomogram() {
                const sex = model.get("sex");
                const svgUrl = model.get("svg_url");
                
                if (!svgUrl) {
                    showError("SVG URL not provided");
                    return;
                }
                
                // Construct the full SVG path based on sex
                const svgPath = sex === 'female' 
                    ? `${svgUrl}/homo_sapiens.female.svg`
                    : `${svgUrl}/homo_sapiens.male.svg`;
                
                showLoading(`Loading SVG from: ${svgPath}`);
                console.log('Loading SVG from:', svgPath);
                
                try {
                    const svgDoc = await d3.xml(svgPath);
                    console.log('SVG loaded successfully:', svgDoc);
                    
                    if (!svgDoc || !svgDoc.documentElement) {
                        showError("Invalid SVG document");
                        return;
                    }
                    
                    container.html('');
                    const svgElement = svgDoc.documentElement;
                    container.node().appendChild(svgElement);
                    currentSvg = d3.select(svgElement);
                    
                    // Set SVG size
                    currentSvg
                        .attr("width", "100%")
                        .attr("height", "100%")
                        .attr("viewBox", currentSvg.attr("viewBox") || "0 0 800 1000")
                        .attr("preserveAspectRatio", "xMidYMid meet");
                    
                    // Attach event handlers and update colors
                    attachEventHandlers();
                    updateColors();
                    
                } catch (error) {
                    console.error("Error loading SVG:", error);
                    showError(`Failed to load anatomogram: ${error.message}`);
                }
            }
            
            // Color scale creation
            function createColorScale(palette, scaleType, minVal, maxVal) {
                const colorSchemes = {
                    'viridis': d3.interpolateViridis,
                    'magma': d3.interpolateMagma,
                    'inferno': d3.interpolateInferno,
                    'plasma': d3.interpolatePlasma,
                    'turbo': d3.interpolateTurbo,
                    'cividis': d3.interpolateCividis,
                    'warm': d3.interpolateWarm,
                    'cool': d3.interpolateCool
                };
                
                const interpolator = colorSchemes[palette] || d3.interpolateViridis;
                
                if (scaleType === 'log') {
                    // For log scale, we need positive values
                    const logMin = minVal > 0 ? minVal : 0.001;
                    const logScale = d3.scaleLog()
                        .domain([logMin, maxVal])
                        .range([0, 1])
                        .clamp(true);
                    
                    return (value) => {
                        if (value <= 0) return interpolator(0);
                        return interpolator(logScale(value));
                    };
                } else {
                    // Linear scale
                    const linearScale = d3.scaleLinear()
                        .domain([minVal, maxVal])
                        .range([0, 1])
                        .clamp(true);
                    
                    return (value) => interpolator(linearScale(value));
                }
            }
            
            // Update tissue colors based on expression data
            function updateColors() {
                if (!currentSvg) return;
                
                const gene = model.get("selected_gene");
                const expressionData = model.get("expression_data");
                const palette = model.get("color_palette");
                const scaleType = model.get("scale_type");
                const threshold = model.get("threshold") || 0;
                
                if (!gene || !expressionData || !expressionData.genes || !expressionData.genes[gene]) {
                    // Reset all to default gray if no valid data
                    currentSvg.selectAll('*[id^="UBERON"]').each(function() {
                        const element = d3.select(this);
                        colorElement(element, '#E0E0E0');
                    });
                    return;
                }
                
                const geneData = expressionData.genes[gene];
                const values = Object.values(geneData).filter(v => typeof v === 'number' && v > 0);
                
                if (values.length === 0) {
                    // No valid values, color everything gray
                    currentSvg.selectAll('*[id^="UBERON"]').each(function() {
                        const element = d3.select(this);
                        colorElement(element, '#E0E0E0');
                    });
                    return;
                }
                
                const minVal = d3.min(values) || 0;
                const maxVal = d3.max(values) || 1;
                
                const colorScale = createColorScale(palette, scaleType, minVal, maxVal);
                
                // Update all tissue elements
                currentSvg.selectAll('*[id^="UBERON"]').each(function() {
                    const element = d3.select(this);
                    const tissueId = element.attr('id');
                    const value = geneData[tissueId];
                    
                    if (value !== undefined && value >= threshold) {
                        const color = colorScale(value);
                        colorElement(element, color);
                        element.attr('data-expression', value);
                    } else {
                        colorElement(element, '#E0E0E0');
                        element.attr('data-expression', null);
                    }
                });
            }
            
            // Helper function to color an element (handles groups and paths)
            function colorElement(element, color) {
                const node = element.node();
                if (node.tagName.toLowerCase() === 'g') {
                    // For groups, color all child shapes
                    element.selectAll('path, rect, circle, polygon, ellipse').style('fill', color);
                } else {
                    // Direct shape element
                    element.style('fill', color);
                }
            }
            
            // Attach event handlers for tooltips
            function attachEventHandlers() {
                if (!currentSvg || !tooltip) return;
                
                currentSvg.selectAll('*[id^="UBERON"]')
                    .on('mouseover', function(event) {
                        const element = d3.select(this);
                        const tissueId = element.attr('id');
                        const expressionValue = element.attr('data-expression');
                        
                        if (!tissueId) return;
                        
                        const gene = model.get("selected_gene");
                        const uberonMap = model.get("uberon_map");
                        
                        const tissueName = uberonMap && uberonMap[tissueId] ? uberonMap[tissueId] : tissueId;
                        
                        let tooltipContent = `<div class="tissue-name">${tissueName}</div>`;
                        
                        if (expressionValue && expressionValue !== 'null') {
                            const value = parseFloat(expressionValue);
                            tooltipContent += `<div class="expression-value">Expression: ${value.toFixed(3)}</div>`;
                            if (gene) {
                                tooltipContent += `<div class="expression-value">Gene: ${gene}</div>`;
                            }
                        } else {
                            tooltipContent += `<div class="expression-value">No expression data</div>`;
                        }
                        
                        tooltip
                            .style("display", "block")
                            .html(tooltipContent);
                    })
                    .on('mousemove', function(event) {
                        const [x, y] = d3.pointer(event, mainContainer);
                        tooltip
                            .style("left", (x + 10) + "px")
                            .style("top", (y - 10) + "px");
                    })
                    .on('mouseout', function() {
                        tooltip.style("display", "none");
                    });
            }
            
            // Initialize
            initTooltip();
            
            // Initial load
            if (model.get("svg_url")) {
                loadAnatomogram();
            }
            
            // Listen for property changes
            model.on("change:selected_gene", updateColors);
            model.on("change:sex", loadAnatomogram);
            model.on("change:color_palette", updateColors);
            model.on("change:scale_type", updateColors);
            model.on("change:threshold", updateColors);
            model.on("change:expression_data", () => {
                if (currentSvg) {
                    updateColors();
                } else {
                    loadAnatomogram();
                }
            });
            model.on("change:svg_url", loadAnatomogram);
        }
    };
    """
    
    # Synchronized properties
    expression_data = traitlets.Dict({}).tag(sync=True)
    selected_gene = traitlets.Unicode("").tag(sync=True)
    sex = traitlets.Unicode("male").tag(sync=True)
    color_palette = traitlets.Unicode("viridis").tag(sync=True)
    scale_type = traitlets.Unicode("linear").tag(sync=True)
    uberon_map = traitlets.Dict({}).tag(sync=True)
    threshold = traitlets.Float(0.0).tag(sync=True)
    svg_url = traitlets.Unicode("").tag(sync=True)  # Base URL for SVG files
    
    def __init__(self, **kwargs):
        """Initialize the widget with optional parameters."""
        super().__init__(**kwargs)
    
    def update_gene(self, gene: str):
        """Update the selected gene programmatically."""
        if self.expression_data and 'genes' in self.expression_data:
            if gene in self.expression_data['genes']:
                self.selected_gene = gene
            else:
                raise ValueError(f"Gene '{gene}' not found in expression data")
    
    def get_available_genes(self):
        """Get list of available genes from the expression data."""
        if self.expression_data and 'genes' in self.expression_data:
            return sorted(self.expression_data['genes'].keys())
        return []