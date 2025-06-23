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

## Getting Started

This project is fully containerized. All you need is Git and Docker with Docker Compose installed on your machine.

### 1. Prerequisites

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/products/docker-desktop/) (which includes Docker Compose)

### 2. Clone the Repository

```bash
git clone [link](https://github.com/riyaz-maker/multimodal-search-engine)
cd multimodal-search-engine
```

### 3. Configure Your Environment
The application uses a .env file to manage secrets and configuration.

### 4. First-Time Setup (Data Processing & Indexing)
These commands only need to be run once to prepare the data and populate your databases.

```bash
docker-compose build
```

### 5. Run the data preparation and indexing pipeline step-by-step:
(This entire process may take 20-40 minutes depending on your hardware)

```bash
# Step 1: Prepare the H&M data
docker-compose run --rm scripts python -m scripts.prepare_hm_data

# Step 2: Ingest metadata into PostgreSQL
docker-compose run --rm scripts python -m scripts.ingest_data

# Step 3: Create the vector index in Pinecone
docker-compose run --rm scripts python -m scripts.setup_vector_db

# Step 4: Generate embeddings and populate Pinecone & Elasticsearch
docker-compose run --rm scripts python -m scripts.batch_index
```

### 6. Run the Full Application
Once the one-time setup is complete, you can run the entire application stack with a single command.
```bash
docker-compose up
```
Frontend UI will be available at: http://localhost:5173
Backend API docs will be available at: http://localhost:8000/docs
To stop all services, press Ctrl + C in the terminal where Docker Compose is running.

## Technology Stack
Backend: Python, FastAPI
Frontend: React (with Vite)
ML Model: clip-ViT-B-32 via sentence-transformers
Vector Database: Pinecone
Keyword Search: Elasticsearch
Primary Database: PostgreSQL
Orchestration: Docker & Docker Compose

# Screenshots
![E324A702-255F-41C8-A579-22CD14B65B4E_1_105_c](https://github.com/user-attachments/assets/1e2a1d58-f194-43a7-a929-7013d7b02a91)
![F7870CB9-1C50-4BCC-9EDA-3C2600EAA514_1_105_c](https://github.com/user-attachments/assets/d1825ab2-da2d-40d2-9c24-1fab135e182f)
![5F382292-612B-4D7C-8FD8-5E92FF5DA642_1_105_c](https://github.com/user-attachments/assets/472f78de-ac46-4aa6-a763-b9a61a120ecf)
