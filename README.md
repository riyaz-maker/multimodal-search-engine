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
