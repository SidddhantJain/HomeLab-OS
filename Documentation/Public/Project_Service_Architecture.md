# Project Intelligence Service Architecture

## Purpose
Inspects developer code repositories, queries git remote tracking configs, and identifies framework details.

## Components
1. **GitIntegrator**: Runs git head queries to check active branch and remote URLs.
2. **MetadataAnalyzer**: Reads root files to detect languages (Python, Javascript, HTML) and runtime dependencies.
3. **ProjectManager**: Saves project metadata properties to database.
