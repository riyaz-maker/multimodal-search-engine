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

This provides a complete, end-to-end implementation of a multimodal search engine for e-commerce. It addresses the fundamental "vocabulary gap" where users know what they want visually but struggle to describe it with text. By using a hybrid retrieval system, it combines the  semantic vector search with the of traditional keyword search to deliver highly relevant results.

This repository is a blueprint for building AI system.

## Key Features

* **Multimodal Search**: Allows users to search with text, an image, or a combination of both.

* **Hybrid Retrieval**: Intelligently fuses results from a dense vector search (Pinecone + CLIP) for semantic meaning and a sparse keyword search (Elasticsearch).

* **Result Fusion**: Implements Reciprocal Rank Fusion (RRF) to intelligently combine the ranked lists from both search backends, producing a single, highly relevant list of results.

* **Fully Containerized Environment**: The entire application stack (databases, backend, frontend, servers) is defined and orchestrated with Docker and Docker Compose for a one-command setup.

* **Modern, Scalable Architecture**: Built with a FastAPI backend API that serves a React frontend, following a clean, disaggregated system architecture.

## Architectural Diagram

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

## Getting Started

This project is fully containerized. All you need is Git and Docker with Docker Compose installed on your machine.

### 1. Prerequisites

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/products/docker-desktop/) (which includes Docker Compose)

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd multimodal-search-engine