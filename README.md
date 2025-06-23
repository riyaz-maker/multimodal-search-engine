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
    subgraph "User Interface"
        A["React Frontend"]
    end

    subgraph "Backend Logic"
        B["FastAPI Server"]
        F["Fusion Logic (RRF)"]
    end

    subgraph "Data Stores"
        C["Pinecone"]
        D["Elasticsearch"]
        E["PostgreSQL"]
    end

    A -- "1. Search Request" --> B;
    B -- "2. Vector Query" --> C;
    B -- "2. Keyword Query" --> D;
    C -- "3. Semantic IDs" --> F;
    D -- "3. Keyword IDs" --> F;
    F -- "4. Ranked IDs" --> B;
    B -- "5. Fetch Details" --> E;
    E -- "6. Product Data" --> B;
    B -- "7. Final JSON Response" --> A;