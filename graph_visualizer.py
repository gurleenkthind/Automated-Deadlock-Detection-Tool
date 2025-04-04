from pyvis.network import Network
import networkx as nx
import webbrowser
import os
import tempfile
from datetime import datetime

def visualize_graph(graph, deadlocked_nodes=None):
    """
    Displays interactive dependency graph with deadlock detection and enhanced visuals.
    
    Args:
        graph (nx.DiGraph): NetworkX directed graph of processes and resources
        deadlocked_nodes (set, optional): Set of nodes involved in deadlock
    """
    # Create a PyVis network with improved styling
    net = Network(
        height="800px", 
        width="100%", 
        bgcolor="#2E3440", 
        font_color="white",
        directed=True,
        heading=f"Resource Allocation Graph Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    # Set network options for better visualization
    net.set_options("""
    {
        "nodes": {
            "borderWidth": 2,
            "borderWidthSelected": 4,
            "font": { "size": 16, "strokeWidth": 2, "strokeColor": "rgba(0,0,0,0.5)" },
            "shadow": true
        },
        "edges": {
            "color": { "inherit": false },
            "width": 2,
            "shadow": true,
            "smooth": { "type": "curvedCW", "roundness": 0.2 }
        },
        "physics": {
            "barnesHut": { "gravitationalConstant": -5000, "springLength": 150 },
            "stabilization": { "iterations": 50 }
        },
        "interaction": {
            "hover": true,
            "navigationButtons": true,
            "keyboard": true
        }
    }
    """)
    
    # Add nodes with styled appearance
    for node in graph.nodes():
        # Set node attributes based on type and deadlock status
        if deadlocked_nodes and node in deadlocked_nodes:
            color = "#BF616A"  # Red for deadlocked nodes
            border_color = "#D08770"
            size = 30
            title = f"{node} (DEADLOCKED)"
        elif node.startswith("P"):
            color = "#5E81AC"  # Blue for processes
            border_color = "#81A1C1"
            size = 25
            title = f"Process {node}"
        else:
            color = "#A3BE8C"  # Green for resources
            border_color = "#B8C88A"
            size = 25
            title = f"Resource {node}"
            
        # Add the node with properties
        net.add_node(
            node, 
            label=node,
            color=color,
            border_color=border_color,
            size=size,
            title=title,
            shape="dot" if node.startswith("P") else "square"
        )
    
    # Add edges with styling
    for source, target in graph.edges():
        # Determine edge type and style accordingly
        if source.startswith("P") and target.startswith("R"):
            # Request edge (Process → Resource)
            color = "#EBCB8B"  # Yellow
            title = f"Request: {source} → {target}"
            arrows = "to"
        else:
            # Allocation edge (Resource → Process)
            color = "#88C0D0"  # Cyan
            title = f"Allocation: {source} → {target}"
            arrows = "to"
            
        # Add the edge with properties
        net.add_edge(
            source, 
            target, 
            color=color,
            title=title,
            width=2,
            arrows=arrows
        )
    
    # Create timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = os.path.join(tempfile.gettempdir(), f"resource_graph_{timestamp}.html")
    
    # Add legend and info to HTML
    net.add_legend({
        "Process": "#5E81AC",
        "Resource": "#A3BE8C",
        "Deadlocked": "#BF616A",
        "Request": "#EBCB8B",
        "Allocation": "#88C0D0"
    })
    
    # Save the graph to HTML and open in browser
    net.save_graph(output_file)
    
    # Add custom JS to HTML for additional features
    with open(output_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Add custom CSS for better appearance
    custom_css = """
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #2E3440;
            color: #ECEFF4;
        }
        #mynetwork {
            border: 1px solid #4C566A;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }
        .header {
            padding: 10px 20px;
            background-color: #3B4252;
            border-bottom: 1px solid #4C566A;
            margin-bottom: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .legend {
            background-color: #3B4252;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            margin-right: 15px;
        }
        .legend-color {
            width: 20px;
            height: 20px;
            margin-right: 8px;
            border-radius: 4px;
        }
        h1, h2 {
            color: #88C0D0;
        }
        .info-box {
            background-color: #3B4252;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
    </style>
    """
    
    # Replace closing head tag with our custom CSS
    content = content.replace('</head>', f'{custom_css}</head>')
    
    # Write the modified content back to the file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)
    
    # Open the HTML file in browser
    webbrowser.open('file://' + os.path.abspath(output_file))
    
    return output_file
