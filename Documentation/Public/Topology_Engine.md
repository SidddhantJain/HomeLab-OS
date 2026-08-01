# Network Topology Engine Specification

## Overview
Generates a structured graph format representing network node relationships:
```json
{
  "nodes": [
    {"id": "internet", "type": "gateway"},
    {"id": "router", "type": "router"},
    {"id": "homelab", "type": "server"}
  ],
  "edges": [
    {"source": "internet", "target": "router"},
    {"source": "router", "target": "homelab"}
  ]
}
```
Used by `Topology.jsx` to render node visualizations.
