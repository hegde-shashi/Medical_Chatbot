# 🏥 Medical Chatbot — RAG-Powered AI Health Assistant

A **Retrieval-Augmented Generation (RAG)** based medical chatbot that answers health-related questions using a curated medical knowledge base. Built with **LangChain**, **Google Gemini**, **Pinecone**, and **Flask**, and fully deployed on **AWS (EC2 + ECR)** via a **GitHub Actions CI/CD pipeline**.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Features](#-features)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Indexing the Medical Knowledge Base](#indexing-the-medical-knowledge-base)
  - [Running the App Locally](#running-the-app-locally)
- [Running with Docker](#-running-with-docker)
- [AWS Deployment](#-aws-deployment)
  - [Step 1 – Create IAM User](#step-1--create-iam-user)
  - [Step 2 – Create Amazon ECR Repository](#step-2--create-amazon-ecr-repository)
  - [Step 3 – Launch EC2 Instance](#step-3--launch-ec2-instance)
  - [Step 4 – Configure GitHub Actions Secrets](#step-4--configure-github-actions-secrets)
  - [Step 5 – Set Up GitHub Actions Self-Hosted Runner on EC2](#step-5--set-up-github-actions-self-hosted-runner-on-ec2)
  - [Step 6 – CI/CD Pipeline (GitHub Actions)](#step-6--cicd-pipeline-github-actions)
- [CI/CD Workflow](#-cicd-workflow)
- [Environment Variables Reference](#-environment-variables-reference)
- [Contributing](#-contributing)
- [Author](#-author)
- [License](#-license)

---

## 🧠 Overview

This project is an intelligent medical chatbot that leverages the power of **Retrieval-Augmented Generation (RAG)**:

1. A medical PDF book is chunked and embedded using **HuggingFace sentence-transformers**.
2. The vector embeddings are stored in a **Pinecone** vector database.
3. When a user asks a question, the app retrieves the most relevant document chunks and passes them as context to **Google Gemini 2.5 Flash**.
4. The LLM synthesizes a concise, accurate answer grounded in the medical knowledge base.

If a question falls outside the medical book's scope but is still medically valid, the chatbot cites general medical knowledge and flags the source distinction transparently.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Google Gemini 2.5 Flash (`langchain-google-genai`) |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` (HuggingFace) |
| **Vector DB** | Pinecone (Serverless, AWS `us-east-1`) |
| **Orchestration** | LangChain (RAG chain) |
| **Backend** | Flask (Python) |
| **Frontend** | HTML, CSS, Vanilla JS |
| **Containerization** | Docker |
| **Container Registry** | Amazon ECR |
| **Cloud Compute** | Amazon EC2 |
| **CI/CD** | GitHub Actions |

---

## 📁 Project Structure

```
Medical_Chatbot/
├── .github/
│   └── workflows/
│       └── cicd.yaml          # GitHub Actions CI/CD pipeline
├── data/
│   └── Medical_book.pdf       # Source medical knowledge base
├── research/
│   └── trials.ipynb           # Experimentation & prototyping notebook
├── src/
│   ├── __init__.py
│   ├── helper.py              # PDF loading, text splitting, embedding utils
│   └── prompt.py              # System prompt for the LLM
├── templates/
│   └── chat.html              # Chat UI (served by Flask)
├── app.py                     # Flask app — main entry point
├── store_index.py             # One-time script: embed & push to Pinecone
├── dockerfile                 # Docker build instructions
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup
├── template.sh                # Project scaffolding script
└── .env                       # Environment variables (not committed)
```

---

## 🏗️ Architecture

```
User (Browser)
     │
     ▼
Flask Web App (app.py)
     │
     ▼
LangChain RAG Chain
     │
     ├──► Pinecone Vector DB  ◄──── (Indexed from Medical PDF via store_index.py)
     │         │
     │    Top-K Relevant Chunks
     │
     └──► Google Gemini 2.5 Flash (LLM)
               │
               ▼
          Final Answer → User
```

The data pipeline (`store_index.py`) is a one-time setup:
```
Medical_book.pdf
     │
  PyPDFLoader
     │
  Text Chunking (chunk_size=500, overlap=20)
     │
  HuggingFace Embeddings (all-MiniLM-L6-v2, dim=384)
     │
  Pinecone Index ("medical-chatbot", cosine similarity)
```

---

## ✨ Features

- 🔍 **RAG-based answering** — Grounded in a real medical knowledge base
- 🤖 **Gemini 2.5 Flash** — Fast, accurate LLM responses
- 📄 **PDF ingestion pipeline** — Easily swap or update the knowledge base
- 🌐 **Clean Chat UI** — Responsive, animated chat interface
- 🐳 **Dockerized** — Runs consistently anywhere
- ☁️ **AWS Deployed** — EC2 + ECR with full CI/CD automation
- 🔄 **Auto-deploy on push** — Every push to `main` triggers build → push → deploy

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Docker (for containerized runs)
- A [Pinecone](https://www.pinecone.io/) account (free tier works)
- A [Google AI Studio](https://aistudio.google.com/) API key (for Gemini)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/hegde-shashi/Medical_Chatbot.git
cd Medical_Chatbot

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
PINECONE_API_KEY=your_pinecone_api_key_here
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### Indexing the Medical Knowledge Base

> ⚠️ Run this **once** to embed the PDF and populate Pinecone.

```bash
python store_index.py
```

This will:
1. Load `data/Medical_book.pdf`
2. Split it into 500-token chunks
3. Embed with `all-MiniLM-L6-v2`
4. Create a `medical-chatbot` Pinecone index (if it doesn't exist)
5. Upsert all vectors into Pinecone

### Running the App Locally

```bash
python app.py
```

Navigate to `http://localhost:3000` in your browser.

---

## 🐳 Running with Docker

```bash
# Build the Docker image
docker build -t medical-chatbot .

# Run the container
docker run -d \
  -e PINECONE_API_KEY=your_pinecone_api_key \
  -e GEMINI_API_KEY=your_gemini_api_key \
  -p 3000:3000 \
  medical-chatbot
```

App will be available at `http://localhost:3000`.

---

## ☁️ AWS Deployment

The application is deployed on AWS using **Amazon ECR** (container registry) and **Amazon EC2** (compute), with the full deployment pipeline automated via **GitHub Actions**.

---

### Step 1 – Create IAM User

1. Go to **AWS Console → IAM → Users → Create User**
2. Set a username (e.g., `medical-chatbot-deployer`)
3. Attach the following policies:
   - `AmazonEC2ContainerRegistryFullAccess`
   - `AmazonEC2FullAccess`
4. Go to **Security Credentials → Create Access Key** (choose CLI use case)
5. Save the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

---

### Step 2 – Create Amazon ECR Repository

1. Go to **AWS Console → ECR → Create Repository**
2. Set visibility to **Private**
3. Name it (e.g., `medical-chatbot`)
4. Save the **repository URI** — you'll use it as `ECR_REPO` in GitHub Secrets

---

### Step 3 – Launch EC2 Instance

1. Go to **AWS Console → EC2 → Launch Instance**
2. Select **Ubuntu 22.04 LTS** (or similar)
3. Choose instance type: `t2.medium` or higher (recommended for model inference)
4. Configure Security Group — open **port 3000** (and port 22 for SSH)
5. Launch and SSH into the instance
6. Install Docker on the EC2 instance:

```bash
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

---

### Step 4 – Configure GitHub Actions Secrets

Go to your **GitHub repo → Settings → Secrets and Variables → Actions** and add:

| Secret Name | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key ID |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret access key |
| `AWS_DEFAULT_REGION` | AWS region (e.g., `us-east-1`) |
| `ECR_REPO` | ECR repository name (e.g., `medical-chatbot`) |
| `PINECONE_API_KEY` | Your Pinecone API key |
| `GEMINI_API_KEY` | Your Google Gemini API key |

---

### Step 5 – Set Up GitHub Actions Self-Hosted Runner on EC2

1. Go to **GitHub repo → Settings → Actions → Runners → New self-hosted runner**
2. Select **Linux** and follow the installation commands on your EC2 instance
3. Start the runner:

```bash
./run.sh
```

> 💡 Keep the runner running in the background with `nohup ./run.sh &` or configure it as a service.

---

### Step 6 – CI/CD Pipeline (GitHub Actions)

Every push to the `main` branch automatically triggers:

1. **CI (Continuous Integration)** — Runs on GitHub-hosted `ubuntu-latest`:
   - Checks out the code
   - Authenticates with AWS
   - Logs in to Amazon ECR
   - Builds the Docker image and pushes it to ECR

2. **CD (Continuous Deployment)** — Runs on the **self-hosted EC2 runner**:
   - Checks out the code
   - Authenticates with AWS
   - Logs in to Amazon ECR
   - Pulls and runs the latest Docker image on the EC2 instance, exposing port 3000

The app is then accessible at: `http://<EC2_PUBLIC_IP>:3000`

---

## 🔄 CI/CD Workflow

```yaml
# .github/workflows/cicd.yaml (summary)

on:
  push:
    branches: [main]

jobs:
  Continuous-Integration:       # GitHub-hosted runner
    - Checkout code
    - Configure AWS credentials
    - Login to Amazon ECR
    - docker build & push to ECR

  Continuous-Deployment:        # Self-hosted runner (EC2)
    - Checkout code
    - Configure AWS credentials
    - Login to Amazon ECR
    - docker run (with env vars injected from GitHub Secrets)
```

---

## 🔑 Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `PINECONE_API_KEY` | ✅ | API key for Pinecone vector database |
| `GEMINI_API_KEY` | ✅ | Google Gemini API key (set as `GOOGLE_API_KEY` in env) |

---


## 👨‍💻 Author

**Shashidhar Hegde**
📧 [hegdeshashidhar123@gmail.com](mailto:hegdeshashidhar123@gmail.com)
🔗 [GitHub](https://github.com/hegde-shashi)

---

## 📜 License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.