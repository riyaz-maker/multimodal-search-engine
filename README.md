# Multimodal E-commerce Search Engine

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/React-18-blue.svg" alt="React Version">
  <img src="https://img.shields.io/badge/Framework-FastAPI-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Vector_DB-Pinecone-blue.svg" alt="Pinecone">
  <img src="https://img.shields.io/badge/Search-Elasticsearch-yellow.svg" alt="Elasticsearch">
  <img src="https://img.shields.io/badge/Orchestration-Docker-blue.svg" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

This provides a complete, end-to-end implementation of a multimodal search engine for e-commerce. It combines semantic vector search with the precision of traditional keyword search and images to deliver highly relevant results.

This repository is a blueprint for building user-facing AI system.

## Key Features

- **Intuitive Multimodal Search**: Allows users to search with text, an image, or a combination of both.
- **Advanced Hybrid Retrieval**: Intelligently fuses results from two distinct search backends:
    - **Dense (Vector) Search**: Uses Pinecone and a pretrained CLIP model (`clip-ViT-B-32`) to find semantically similar items based on visual and descriptive meaning.
    - **Sparse (Keyword) Search**: Uses Elasticsearch and the BM25 algorithm for precise matching on product titles, categories, and other metadata.
- **Result Fusion**: Implements Reciprocal Rank Fusion (RRF) to intelligently combine the ranked lists from both search backends, producing a single, highly relevant list of results.
- **Fully Containerized Environment**: The entire application stack (databases, backend, frontend, servers) is defined and orchestrated with Docker and Docker Compose.

## Architectural Diagram

The system follows a modern, service-oriented architecture where different components are specialized for their tasks. The FastAPI backend acts as the central orchestrator.

```mermaid
graph TD
    subgraph User Facing
        A[React Frontend]
    end

    subgraph Backend API
        B(FastAPI Server)
    end
    
    subgraph Data & Search Backends
        C{Pinecone Vector DB}
        D{Elasticsearch}
        E(PostgreSQL Catalog)
    end

    A -->|HTTP Search Request| B;
    B -->|1. Vector Query| C;
    B -->|1. Keyword Query| D;
    C -->|2. Semantic Results| B;
    D -->|2. Keyword Results| B;
    B -->|3. Fuse Results (RRF)| F{Final Ranked IDs};
    F -->|4. Fetch Details| E;
    E -->|5. Product Details| B;
    B -->|6. JSON Response| A;