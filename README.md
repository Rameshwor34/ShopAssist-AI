\# 🛍️ ShopAssist AI



\*\*AI-Powered E-Commerce Customer Support Assistant\*\*



ShopAssist AI is a production-oriented customer support assistant designed for e-commerce applications. It combines \*\*LLM-based intent routing, specialized agents, tool calling, Retrieval-Augmented Generation (RAG), structured JSON responses, caching, deterministic fallbacks, and containerized deployment\*\* into a single application.



The system is designed to answer common e-commerce customer-support questions such as:



\* Where is my order?

\* What is the status of my order?

\* What is the estimated delivery date?

\* Can I return my order?

\* Is my order eligible for return?

\* What is the return policy?

\* Where is my refund?

\* Can I cancel my order?

\* Why did my payment fail?

\* Is a product compatible with my device?

\* Is a product currently available?



The application provides a \*\*Streamlit web interface\*\* backed by a \*\*FastAPI service\*\*, with Gemini used as the primary LLM provider and a deterministic fallback mechanism for graceful degradation.



\---



\# 📋 Table of Contents



1\. \[Project Overview](#-project-overview)

2\. \[Problem Statement](#-problem-statement)

3\. \[Objectives](#-objectives)

4\. \[Key Features](#-key-features)

5\. \[System Architecture](#-system-architecture)

6\. \[Architecture Components](#-architecture-components)

7\. \[Application Request Flow](#-application-request-flow)

8\. \[Task 1 — Build an AI Assistant](#-task-1--build-an-ai-assistant)

9\. \[Task 2 — Productionize the AI Assistant](#-task-2--productionize-the-ai-assistant)

10\. \[LLM Integration](#-llm-integration)

11\. \[Prompt Engineering](#-prompt-engineering)

12\. \[Structured Output](#-structured-output)

13\. \[Intent Routing](#-intent-routing)

14\. \[Specialized Agents](#-specialized-agents)

15\. \[Tool Calling](#-tool-calling)

16\. \[RAG Pipeline](#-rag-pipeline)

17\. \[Local LLM Deployment](#-local-llm-deployment)

18\. \[Caching](#-caching)

19\. \[Reliability and Graceful Degradation](#-reliability-and-graceful-degradation)

20\. \[Mock Transactional Data](#-mock-transactional-data)

21\. \[Web Interface](#-web-interface)

22\. \[Docker Containerization](#-docker-containerization)

23\. \[Docker Compose](#-docker-compose)

24\. \[Configuration](#-configuration)

25\. \[Project Structure](#-project-structure)

26\. \[Running the Application](#-running-the-application)

27\. \[Testing the Backend](#-testing-the-backend)

28\. \[Example Requests](#-example-requests)

29\. \[Production Engineering Considerations](#-production-engineering-considerations)

30\. \[Assignment Requirements Coverage](#-assignment-requirements-coverage)

31\. \[Limitations and Future Improvements](#-limitations-and-future-improvements)

32\. \[Conclusion](#-conclusion)

33\. \[Created By](#-created-by)



\---



\# 📌 Project Overview



ShopAssist AI implements an AI-powered customer-support architecture for an e-commerce environment.



Instead of sending every customer message directly to an LLM, the application first determines the customer's intent and then routes the request through the appropriate processing path.



The overall processing pipeline is:



```text

Customer

&#x20;  │

&#x20;  ▼

Streamlit Web UI

&#x20;  │

&#x20;  ▼

FastAPI Backend

&#x20;  │

&#x20;  ▼

Chat Service

&#x20;  │

&#x20;  ▼

Intent Router

&#x20;  │

&#x20;  ├── Order Support

&#x20;  ├── Shipping

&#x20;  ├── Returns

&#x20;  ├── Refunds

&#x20;  ├── Cancellations

&#x20;  ├── Payments

&#x20;  ├── Account Support

&#x20;  ├── Product Information

&#x20;  └── General Support

&#x20;  │

&#x20;  ▼

Specialized Agent

&#x20;  │

&#x20;  ├── Tool Calling

&#x20;  │

&#x20;  ├── RAG Retrieval

&#x20;  │

&#x20;  └── LLM Generation

&#x20;  │

&#x20;  ▼

Structured Response

&#x20;  │

&#x20;  ▼

Streamlit UI

```



The architecture supports both cloud-based LLM inference through \*\*Gemini\*\* and optional local inference through \*\*vLLM\*\*.



\---



\# 🧩 Problem Statement



\## Task 1 — Build an AI Assistant



The first task requires development of a robust AI assistant using modern LLM APIs and RAG architectures.



The assistant must demonstrate:



\* Integration with a major LLM provider

\* Prompt engineering

\* Structured output

\* Tool calling

\* RAG

\* Embeddings and vector retrieval

\* Local open-source model deployment

\* Docker containerization



\## Task 2 — Productionize the AI Assistant



The second task focuses on transforming the assistant into a more production-oriented AI system.



The productionization requirements include:



\* A web UI

\* Backend/API integration

\* Reliability mechanisms

\* Fallback behavior

\* Error handling

\* Caching

\* Containerization

\* Docker Compose

\* Deployment instructions

\* Production-oriented architecture



ShopAssist AI addresses these requirements through a modular backend architecture and a Dockerized application stack.



\---



\# 🎯 Objectives



The main objectives of this project are:



1\. Build an AI-powered e-commerce support assistant.

2\. Integrate a modern LLM provider.

3\. Implement prompt engineering.

4\. Implement structured JSON responses.

5\. Build an intent classification and routing layer.

6\. Route requests to specialized support agents.

7\. Integrate transactional tools.

8\. Implement RAG-based knowledge retrieval.

9\. Support local LLM inference through vLLM.

10\. Provide graceful degradation when the primary LLM is unavailable.

11\. Add response caching.

12\. Provide a browser-based Streamlit interface.

13\. Containerize the application.

14\. Provide a reproducible Docker Compose deployment.

15\. Design the system around production-oriented AI engineering principles.



\---



\# ✨ Key Features



\## 🤖 LLM Integration



Gemini is used as the primary cloud LLM provider.



The application supports configuration of:



\* LLM provider

\* Gemini model

\* Temperature

\* Top-p



The current configuration uses:



```text

LLM\_PROVIDER=gemini

GEMINI\_MODEL=gemini-3.6-flash

```



\---



\## 🧠 Intelligent Intent Routing



Customer messages are classified into one of nine supported intents:



```text

order\_support

shipping

returns

refunds

cancellations

payments

account\_support

product\_information

general\_support

```



The router first attempts LLM-based classification.



If Gemini is unavailable, rate-limited, or produces malformed output, the system switches to deterministic keyword-based routing.



\---



\## 👨‍💼 Specialized Agents



After identifying the intent, ShopAssist selects the appropriate specialized agent instructions.



This allows the same underlying LLM to behave differently depending on the customer's request.



For example:



```text

Customer Request

&#x20;     │

&#x20;     ▼

Intent Router

&#x20;     │

&#x20;     ├── returns

&#x20;     │       ▼

&#x20;     │   Returns Agent

&#x20;     │

&#x20;     ├── shipping

&#x20;     │       ▼

&#x20;     │   Shipping Agent

&#x20;     │

&#x20;     ├── order\_support

&#x20;     │       ▼

&#x20;     │   Order Support Agent

&#x20;     │

&#x20;     └── product\_information

&#x20;             ▼

&#x20;         Product Agent

```



\---



\# 🏗️ System Architecture



\## Architecture Diagram



┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                         🏗️ ShopAssist AI — System Architecture                               │
│                                                                                              │
│                                      👤 USER                                                 │
│                                        │                                                     │
│                                        ▼                                                     │
│                              ┌───────────────────┐                                           │
│                              │  🖥️ Streamlit UI  │                                           │
│                              │   frontend/app.py │                                           │
│                              │                   │                                           │
│                              │  • Chat interface │                                           │
│                              │  • User messages  │                                           │
│                              │  • AI responses   │                                           │
│                              └─────────┬─────────┘                                           │
│                                        │ HTTP POST /chat                                     │
│                                        ▼                                                     │
│                         ┌──────────────────────────────┐                                     │
│                         │       ⚡ FastAPI Backend      │                                     │
│                         │          backend/main.py      │                                     │
│                         │                              │                                     │
│                         │  • API endpoints             │                                     │
│                         │  • Request validation        │                                     │
│                         │  • Response handling         │                                     │
│                         └──────────────┬───────────────┘                                     │
│                                        │                                                     │
│                                        ▼                                                     │
│                         ┌──────────────────────────────┐                                     │
│                         │       🧭 Intent Router        │                                     │
│                         │     backend/routing/router.py│                                     │
│                         │                              │                                     │
│                         │      Hybrid Routing          │                                     │
│                         │                              │                                     │
│                         │   ┌──────────────────────┐   │                                     │
│                         │   │ Gemini Classification│   │                                     │
│                         │   └──────────┬───────────┘   │                                     │
│                         │              │               │                                     │
│                         │              ▼               │                                     │
│                         │   ┌──────────────────────┐   │                                     │
│                         │   │ Deterministic        │   │                                     │
│                         │   │ Keyword Fallback    │   │                                     │
│                         │   └──────────────────────┘   │                                     │
│                         └──────────────┬───────────────┘                                     │
│                                        │                                                     │
│              ┌─────────────────────────┼─────────────────────────┐                           │
│              │                         │                         │                           │
│              ▼                         ▼                         ▼                           │
│     ┌─────────────────┐      ┌──────────────────┐      ┌──────────────────┐                 │
│     │ 🎯 Specialized  │      │ 🔧 Tool Registry  │      │ 📚 RAG Pipeline  │                 │
│     │     Agents      │      │                  │      │                  │                 │
│     │                 │      │ • Order Status   │      │ • Ingestion      │                 │
│     │ • Order Agent   │      │ • Product Info   │      │ • Chunking       │                 │
│     │ • Shipping      │      │ • Return Check   │      │ • Embeddings     │                 │
│     │ • Returns       │      │                  │      │ • Vector Search  │                 │
│     │ • Refunds       │      │                  │      │ • Retrieval      │                 │
│     │ • Cancellation  │      └────────┬─────────┘      └────────┬─────────┘                 │
│     │ • Payments      │               │                         │                           │
│     │ • Account       │               ▼                         ▼                           │
│     │ • Product Info  │      ┌─────────────────┐       ┌──────────────────┐                 │
│     │ • General       │      │ 🗄️ Mock         │       │ 📖 Knowledge Base │                 │
│     │   Support       │      │ Transactional   │       │                  │                 │
│     └────────┬────────┘      │ Data           │       │ Policies / FAQs  │                 │
│              │               │                │       │ Product / Support│                 │
│              │               │ orders.json    │       │ Documents        │                 │
│              │               │ products.json  │       └────────┬─────────┘                 │
│              │               └─────────────────┘                │                           │
│              │                                                  │                           │
│              └──────────────────────────┬───────────────────────┘                           │
│                                         │                                                   │
│                                         ▼                                                   │
│                              ┌──────────────────────┐                                        │
│                              │   🧠 Prompt Builder   │                                        │
│                              │                      │                                        │
│                              │ • System prompt      │                                        │
│                              │ • Agent instructions │                                        │
│                              │ • User message       │                                        │
│                              │ • Retrieved context  │                                        │
│                              │ • Tool results       │                                        │
│                              │ • temperature        │                                        │
│                              │ • top_p              │                                        │
│                              └──────────┬───────────┘                                        │
│                                         │                                                   │
│                          ┌──────────────┴──────────────┐                                    │
│                          │                             │                                    │
│                          ▼                             ▼                                    │
│                ┌────────────────────┐       ┌────────────────────────┐                     │
│                │ ☁️ Gemini Provider │       │ 🖥️ Optional Local LLM │                     │
│                │                    │       │        via vLLM        │                     │
│                │ • Gemini API       │       │                        │                     │
│                │ • Primary LLM      │       │ • Open-source model    │                     │
│                │ • JSON generation  │       │ • Qwen 0.6B            │                     │
│                └─────────┬──────────┘       │ • OpenAI-compatible API│                     │
│                          │                  └────────────┬───────────┘                     │
│                          │                               │                                 │
│                          └───────────────┬───────────────┘                                 │
│                                          │                                                 │
│                                          ▼                                                 │
│                               ┌─────────────────────┐                                      │
│                               │   🛡️ Reliability    │                                      │
│                               │                     │                                      │
│                               │ • Error handling    │                                      │
│                               │ • Rate-limit aware  │                                      │
│                               │ • Provider fallback │                                      │
│                               │ • Deterministic     │                                      │
│                               │   fallback          │                                      │
│                               │ • Graceful degrade  │                                      │
│                               │ • Response caching  │                                      │
│                               └──────────┬──────────┘                                      │
│                                          │                                                 │
│                                          ▼                                                 │
│                               ┌─────────────────────┐                                      │
│                               │ 📦 Structured JSON   │                                      │
│                               │                     │                                      │
│                               │ • intent             │                                      │
│                               │ • answer             │                                      │
│                               │ • confidence         │                                      │
│                               │ • sources            │                                      │
│                               │ • tool_used          │                                      │
│                               │ • routing_method     │                                      │
│                               │ • generation_method  │                                      │
│                               │ • cached             │                                      │
│                               └──────────┬──────────┘                                      │
│                                          │                                                 │
│                                          ▼                                                 │
│                                  🖥️ STREAMLIT UI                                           │
│                                          │                                                 │
│                                          ▼                                                 │
│                                   👤 USER RESPONSE                                         │
│                                                                                              │
│ ─────────────────────────────────────────────────────────────────────────────────────────── │
│                                                                                              │
│ This version reflects the **actual ShopAssist implementation and the assignment            │
│ requirements**, including the FastAPI backend, Streamlit UI, hybrid routing, specialized   │
│ agents, tools, mock transactional data, RAG, Gemini, structured JSON, caching,             │
│ deterministic fallbacks, reliability handling, Docker Compose, and optional vLLM local     │
│ deployment.                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────


Recommended location:



```text

docs/

└── architecture.png

```



The final diagram should represent the complete implementation, including:



\* Customer

\* Streamlit frontend

\* FastAPI backend

\* ChatService

\* IntentRouter

\* Gemini provider

\* deterministic fallback router

\* specialized agents

\* tool registry

\* mock transactional data

\* RAG retrieval

\* knowledge base

\* embeddings/vector retrieval

\* response generation

\* caching

\* structured JSON response

\* optional vLLM deployment

\* Docker containers

\* backend/frontend ports

\* error handling and graceful degradation



The diagram should represent the actual implementation rather than unrelated infrastructure.



\---



\# 🔧 Architecture Components



\## 1. Streamlit Frontend



The frontend provides the user-facing chat interface.



It is responsible for:



\* Accepting customer messages

\* Sending requests to the backend

\* Displaying assistant responses

\* Presenting the ShopAssist AI interface



The frontend runs on:



```text

http://localhost:8501

```



\---



\## 2. FastAPI Backend



The backend provides the API layer for ShopAssist AI.



The FastAPI application exposes endpoints including:



```text

GET /health

POST /chat

```



The backend runs inside Docker on port `8000`.



The host maps this to:



```text

localhost:8002

```



Therefore:



```text

Host:      8002

Container: 8000

```



Health check:



```text

http://localhost:8002/health

```



Example response:



```json

{

&#x20; "status": "healthy",

&#x20; "service": "shopassist-ai"

}

```



\---



\# 🔄 Application Request Flow



A typical request follows this sequence:



```text

User

&#x20;│

&#x20;▼

Streamlit

&#x20;│

&#x20;▼

POST /chat

&#x20;│

&#x20;▼

ChatService

&#x20;│

&#x20;▼

IntentRouter

&#x20;│

&#x20;├───────────────┐

&#x20;│               │

&#x20;▼               ▼

Gemini       Deterministic

Router        Fallback

&#x20;│               │

&#x20;└───────┬───────┘

&#x20;        ▼

&#x20;  Detected Intent

&#x20;        │

&#x20;        ▼

&#x20;Specialized Agent

&#x20;        │

&#x20;   ┌────┴────┐

&#x20;   ▼         ▼

&#x20; Tools      RAG

&#x20;   │         │

&#x20;   └────┬────┘

&#x20;        ▼

&#x20;     Context

&#x20;        │

&#x20;        ▼

&#x20;     Gemini

&#x20;        │

&#x20;        ├── Success

&#x20;        │

&#x20;        └── Failure

&#x20;              │

&#x20;              ▼

&#x20;       Deterministic Answer

&#x20;              │

&#x20;              ▼

&#x20;      Structured Response

&#x20;              │

&#x20;              ▼

&#x20;         Streamlit UI

```



\---



\# 🧪 Task 1 — Build an AI Assistant



\## LLM Integration



The application integrates with Google's Gemini API.



Gemini is used for two primary functions:



\### 1. Intent Routing



The model receives a specialized routing prompt and must classify the request into exactly one supported intent.



Example:



```json

{

&#x20; "intent": "returns",

&#x20; "confidence": 0.95

}

```



\### 2. Response Generation



After routing, the system builds a grounded prompt containing:



\* Customer message

\* Detected intent

\* Specialized agent instructions

\* Retrieved knowledge

\* Tool execution results

\* Safety constraints



Gemini then generates the customer-facing response.



\---



\# ✍️ Prompt Engineering



ShopAssist AI uses separate prompts for different responsibilities.



\## Routing Prompt



The routing prompt defines:



\* Available intents

\* Intent definitions

\* Important distinctions

\* Expected JSON format

\* Confidence requirements



For example:



```text

"Where is my order?" → order\_support



"What is the delivery time?" → shipping



"Can I return this?" → returns



"Where is my refund?" → refunds

```



The router is explicitly instructed to return JSON rather than natural-language explanations.



\---



\## Generation Prompt



The generation prompt combines all available context:



```text

CUSTOMER MESSAGE



DETECTED INTENT



SPECIALIZED AGENT INSTRUCTIONS



RETRIEVED KNOWLEDGE BASE CONTEXT



TOOL EXECUTION RESULT

```



The model is instructed to:



\* Avoid inventing policies

\* Avoid inventing transactional information

\* Treat tool results as authoritative

\* Use retrieved knowledge for policy questions

\* Protect sensitive information

\* Never request passwords

\* Never request CVV

\* Never request complete card numbers

\* Keep responses concise



\---



\# 📦 Structured Output



The backend requests structured JSON responses.



The expected response format is:



```json

{

&#x20; "intent": "returns",

&#x20; "answer": "Yes. This order is currently eligible for return.",

&#x20; "confidence": 0.95,

&#x20; "sources": \[],

&#x20; "tool\_used": "check\_return\_eligibility"

}

```



The backend additionally records:



```text

routing\_method

generation\_method

cached

```



This allows the system to distinguish between:



```text

gemini

deterministic\_fallback

```



for routing and generation.



\---



\# 🧭 Intent Routing



The `IntentRouter` implements a hybrid architecture.



\## Primary Path



```text

Customer Message

&#x20;     │

&#x20;     ▼

Gemini

&#x20;     │

&#x20;     ▼

JSON Classification

```



\## Fallback Path



If Gemini fails:



```text

Customer Message

&#x20;     │

&#x20;     ▼

Keyword-Based Classifier

&#x20;     │

&#x20;     ▼

Intent

```



This prevents a temporary LLM outage from completely disabling routing.



\---



\# 🏷️ Supported Intents



| Intent                | Example                            |

| --------------------- | ---------------------------------- |

| `order\_support`       | Where is my order?                 |

| `shipping`            | How long does shipping take?       |

| `returns`             | I want to return something         |

| `refunds`             | Where is my refund?                |

| `cancellations`       | Can I cancel my order?             |

| `payments`            | My payment failed                  |

| `account\_support`     | I forgot my password               |

| `product\_information` | Is this compatible with my device? |

| `general\_support`     | General customer support           |



\---



\# 👨‍💼 Specialized Agent Layer



After routing, the system retrieves specialized instructions using:



```text

get\_agent\_instruction(intent)

```



This creates a separation between:



```text

Routing

```



and:



```text

Response behavior

```



The architecture can therefore be extended with additional agents without redesigning the entire application.



\---



\# 🛠️ Tool Calling



ShopAssist AI includes a centralized tool registry.



Tools are selected based on intent and available identifiers.



Currently implemented transactional tools include:



\### Order Status



```text

get\_order\_status

```



\### Product Information



```text

get\_product\_info

```



\### Return Eligibility



```text

check\_return\_eligibility

```



The system extracts identifiers from user messages.



For example:



```text

ORD-1001

ORD-1002

ORD-1003

```



and:



```text

PROD-001

PROD-002

PROD-003

```



\---



\# 🔎 RAG Pipeline



ShopAssist AI includes a Retrieval-Augmented Generation layer.



The RAG pipeline follows:



```text

Documents

&#x20;  │

&#x20;  ▼

Document Ingestion

&#x20;  │

&#x20;  ▼

Chunking

&#x20;  │

&#x20;  ▼

Embeddings

&#x20;  │

&#x20;  ▼

Vector Storage

&#x20;  │

&#x20;  ▼

Similarity Retrieval

&#x20;  │

&#x20;  ▼

Top-K Relevant Chunks

&#x20;  │

&#x20;  ▼

Formatted Context

&#x20;  │

&#x20;  ▼

LLM Prompt

```



The application retrieves relevant knowledge using:



```python

results = retrieve(

&#x20;   message,

&#x20;   top\_k=3,

)

```



The retrieved results are then converted into prompt context using:



```python

format\_context(results)

```



This provides the generation model with relevant knowledge instead of relying exclusively on its internal knowledge.



\---



\# 📚 Knowledge Grounding



The generation layer follows a grounded-response strategy.



The system explicitly instructs the LLM:



```text

Do not invent policies.



Do not invent customer/order/product information.



Treat tool results as authoritative for mock transactional data.



Use retrieved knowledge for policy and FAQ information.



If the knowledge base and tools are insufficient, say so clearly.

```



This reduces hallucination risk and separates:



```text

Transactional truth

```



from:



```text

Knowledge-base information

```



\---



\# 🖥️ Local LLM Deployment



The Docker Compose configuration includes an optional vLLM service.



The configured local model is:



```text

Qwen/Qwen3-0.6B

```



The vLLM service uses the OpenAI-compatible API architecture.



The configured endpoint inside Docker is:



```text

http://vllm:8000/v1

```



The configuration supports:



```text

LOCAL\_LLM\_MODEL

LOCAL\_LLM\_BASE\_URL

```



The vLLM service is placed behind the:



```text

local-llm

```



Docker Compose profile.



This means the local LLM infrastructure can be enabled when required without forcing it to run during normal Gemini-based development.



\---



\# 🐳 Containerization



ShopAssist AI is containerized using Docker.



The application uses a Python 3.12 slim base image.



The Docker image installs dependencies from:



```text

requirements.txt

```



and copies:



```text

backend/

frontend/

data/

scripts/

```



into the container.



\---



\# 🐳 Docker Compose



The application is orchestrated using Docker Compose.



The main services are:



```text

backend

frontend

```



An optional:



```text

vllm

```



service is provided for local LLM inference.



\---



\## Backend



```yaml

backend:

&#x20; build: .

&#x20; container\_name: shopassist-backend

```



Host port:



```text

8002

```



Container port:



```text

8000

```



Therefore:



```text

localhost:8002 → backend:8000

```



\---



\## Frontend



The Streamlit frontend runs on:



```text

8501

```



The frontend communicates with the backend through the Docker Compose network.



Inside Docker:



```text

http://backend:8000

```



\---



\# 🗃️ Mock Transactional Data



The project includes mock e-commerce data.



Example orders include:



```text

ORD-1001

ORD-1002

ORD-1003

```



\### ORD-1001



```text

Status: shipped

Carrier: DHL

Tracking: DHL123456789

Estimated Delivery: 2026-09-04

```



\### ORD-1002



```text

Status: processing

Estimated Delivery: 2026-09-06

```



\### ORD-1003



```text

Status: delivered

Carrier: FedEx

Tracking: FDX987654321

Estimated Delivery: 2026-08-28

```



The transactional data is treated as authoritative by the application when a relevant tool is executed.



\---



\# 🔄 Return Eligibility Example



The return workflow demonstrates the complete routing and tool architecture.



Customer:



```text

I want to return order ORD-1003.

```



Routing:



```text

returns

```



Tool:



```text

check\_return\_eligibility

```



Because ORD-1003 is delivered, the system returns:



```text

Yes. This order is currently eligible for return under the available return policy.

```



For ORD-1001, which is shipped:



```text

This order is not currently eligible for return. Only delivered orders can currently be returned.

```



\---



\# 📦 Order Status Example



Customer:



```text

What is the status of ORD-1002?

```



The router detects:



```text

order\_support

```



The system extracts:



```text

ORD-1002

```



and calls:



```text

get\_order\_status

```



The response is:



```text

Your order ORD-1002 is currently processing. The estimated delivery date is 2026-09-06.

```



\---



\# ⚡ Caching



The application supports prompt/response caching.



Repeated requests can therefore avoid unnecessary repeated LLM generation.



Responses can include:



```text

cached: True

```



or:



```text

cached: False

```



This improves efficiency for repeated queries and reduces unnecessary calls to the LLM provider.



Caching is particularly useful when operating against rate-limited API tiers.



\---



\# 🛡️ Reliability and Graceful Degradation



Reliability is one of the major productionization features of ShopAssist AI.



The application does not depend entirely on Gemini being available.



\---



\## Gemini Rate Limiting



During testing, the Gemini API returned HTTP 429 rate-limit errors when the free-tier quota was exceeded.



The backend correctly detected this condition.



Example:



```text

RateLimitError: Error code: 429

```



Instead of crashing, the application switched to:



```text

deterministic\_fallback

```



\---



\# 🔁 Deterministic Routing Fallback



When Gemini routing is unavailable:



```text

Gemini

&#x20; │

&#x20; X

&#x20; │

&#x20; ▼

Deterministic Classifier

```



The classifier uses predefined phrases to identify intents.



For example:



```text

"return something I bought"

```



is mapped to:



```text

returns

```



and:



```text

"What is the status of ORD-1002?"

```



is mapped to:



```text

order\_support

```



This allows the application to continue operating during LLM failures.



\---



\# 🔁 Deterministic Generation Fallback



The same principle is applied during answer generation.



If Gemini generation fails, the backend uses deterministic responses based on available tool results.



For example:



```text

get\_order\_status

```



produces a deterministic answer containing:



\* Order ID

\* Status

\* Carrier

\* Tracking number

\* Estimated delivery



This is particularly important for transactional queries because the response can be generated directly from authoritative tool data.



\---



\# 🚨 Error Handling



The backend catches provider-level exceptions.



Instead of terminating the application, the error is logged and the fallback path is executed.



The architecture therefore follows:



```text

Primary AI Path

&#x20;     │

&#x20;     ▼

Failure?

&#x20;┌────┴────┐

&#x20;No        Yes

&#x20;│          │

&#x20;▼          ▼

Response   Fallback

```



This improves system resilience.



\---



\# 🌐 Web Interface



The application includes a Streamlit-based web interface.



The frontend provides:



```text

ShopAssist AI

AI-powered e-commerce customer support

```



Users can enter natural-language questions and receive responses without interacting directly with the FastAPI API.



The frontend is available at:



```text

http://localhost:8501

```



\---



\# 🧪 Backend API



\## Health Check



```http

GET /health

```



Example:



```powershell

Invoke-RestMethod http://localhost:8002/health

```



Expected:



```text

status   service

\------   -------

healthy  shopassist-ai

```



\---



\# 💬 Chat API



The main endpoint is:



```http

POST /chat

```



Example PowerShell request:



```powershell

Invoke-RestMethod `

&#x20; -Uri http://localhost:8002/chat `

&#x20; -Method Post `

&#x20; -ContentType "application/json" `

&#x20; -Body '{"message":"Where is my order ORD-1001?"}'

```



\---



\# 📤 Example Structured Response



A successful response has the following conceptual structure:



```json

{

&#x20; "answer": "Your order ORD-1001 is currently shipped. The carrier is DHL. Your tracking number is DHL123456789. The estimated delivery date is 2026-09-04.",

&#x20; "confidence": 0.95,

&#x20; "sources": \[],

&#x20; "tool\_used": "get\_order\_status",

&#x20; "intent": "order\_support",

&#x20; "routing\_method": "deterministic\_fallback",

&#x20; "generation\_method": "deterministic\_fallback",

&#x20; "cached": false

}

```



The exact routing and generation methods depend on whether Gemini is available and whether the response was retrieved from cache.



\---



\# 🧪 Example Requests



\## Return Request



```text

I want to return something I bought.

```



Expected behavior:



```text

Intent → returns

```



The assistant requests an order ID because a transactional return check requires an order identifier.



\---



\## Eligible Return



```text

I want to return order ORD-1003.

```



Expected:



```text

Yes. This order is currently eligible for return under the available return policy.

```



\---



\## Ineligible Return



```text

I want to return order ORD-1001.

```



Expected:



```text

This order is not currently eligible for return. Only delivered orders can currently be returned.

```



\---



\## Order Status



```text

What is the status of ORD-1002?

```



Expected:



```text

Your order ORD-1002 is currently processing.

The estimated delivery date is 2026-09-06.

```



\---



\## Missing Order ID



```text

Where is my order?

```



Expected:



```text

I can help you check your order status.

Please provide your order ID.

```



\---



\# ⚙️ Configuration



The application uses environment variables for configuration.



Important settings include:



```text

LLM\_PROVIDER

GEMINI\_MODEL

GEMINI\_API\_KEY

LOCAL\_LLM\_BASE\_URL

LOCAL\_LLM\_MODEL

HUGGING\_FACE\_HUB\_TOKEN

```



Example:



```text

LLM\_PROVIDER=gemini

GEMINI\_MODEL=gemini-3.6-flash

LOCAL\_LLM\_MODEL=Qwen/Qwen3-0.6B

```



API keys should never be committed to GitHub.



The `.env` file should remain excluded through `.gitignore`.



\---



\# 📁 Project Structure



The project follows a modular architecture.



```text

ShopAssist-AI/

│

├── backend/

│   │

│   ├── main.py

│   │

│   ├── agents/

│   │   └── agents.py

│   │

│   ├── llm/

│   │   ├── gemini\_provider.py

│   │   └── prompts.py

│   │

│   ├── routing/

│   │   └── router.py

│   │

│   ├── services/

│   │   └── chat\_service.py

│   │

│   ├── rag/

│   │   └── retrieval.py

│   │

│   └── tools/

│       └── registry.py

│

├── frontend/

│   └── app.py

│

├── data/

│   └── mock\_data/

│       └── orders.json

│

├── scripts/

│

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

├── .env

├── .gitignore

└── README.md

```



\---



\# ▶️ Running the Application



\## Prerequisites



Install:



\* Docker Desktop

\* Docker Compose

\* Git



For development outside Docker, Python 3.12 is recommended.



\---



\# 🐳 Start the Application



From the project directory:



```powershell

docker compose up -d backend frontend

```



Check the running containers:



```powershell

docker compose ps

```



Expected:



```text

shopassist-backend

shopassist-frontend

```



\---



\# ❤️ Verify Backend Health



Run:



```powershell

Invoke-RestMethod http://localhost:8002/health

```



Expected:



```text

status   service

\------   -------

healthy  shopassist-ai

```



\---



\# 🌐 Open the Application



Open:



```text

http://localhost:8501

```



The Streamlit interface should display:



```text

ShopAssist AI

AI-powered e-commerce customer support

```



\---



\# 📜 View Backend Logs



Use:



```powershell

docker compose logs --tail=100 backend

```



Follow live logs:



```powershell

docker compose logs -f backend

```



\---



\# 🔄 Rebuild After Source Changes



When backend source code changes:



```powershell

docker compose build backend

docker compose up -d backend

```



Verify:



```powershell

docker compose ps

```



Then:



```powershell

Invoke-RestMethod http://localhost:8002/health

```



\---



\# 🧹 Stop the Application



```powershell

docker compose down

```



This stops and removes the application containers and Compose network.



\---



\# 🧪 Testing the Application



The implementation was tested through direct API requests and the Streamlit interface.



The following scenarios were verified:



\### Return request



```text

I want to return something I bought.

```



\### Eligible return



```text

I want to return order ORD-1003.

```



\### Ineligible return



```text

I want to return order ORD-1001.

```



\### Shipped order



```text

Where is my order ORD-1001?

```



\### Processing order



```text

What is the status of ORD-1002?

```



\### Missing identifier



```text

Where is my order?

```



These tests verified:



\* Intent classification

\* Fallback routing

\* Identifier extraction

\* Tool execution

\* Transactional data retrieval

\* Return eligibility

\* Deterministic response generation

\* Structured API responses

\* Dockerized backend operation

\* Streamlit-to-backend communication



\---



\# 🏭 Production Engineering



ShopAssist AI incorporates several production-oriented design principles.



\## Modular Architecture



Responsibilities are separated into:



```text

Routing

Agents

LLM

RAG

Tools

Services

Frontend

```



This makes individual components easier to maintain and replace.



\---



\## Provider Abstraction



Gemini interaction is encapsulated in:



```text

GeminiProvider

```



This makes it possible to introduce additional LLM providers in the future.



Potential providers include:



```text

OpenAI

Claude

Azure OpenAI

Local vLLM

```



without redesigning the entire application.



\---



\# ⚡ Latency and Throughput Considerations



The architecture reduces unnecessary work through:



\* Prompt/response caching

\* Tool-based deterministic answers

\* Top-K retrieval

\* Lightweight routing fallback

\* Optional local inference

\* Containerized services



Transactional requests can also bypass unnecessary generation when deterministic tool information is sufficient.



\---



\# 🔐 Security Considerations



The application prompt explicitly prevents the assistant from requesting highly sensitive information.



The assistant must not request:



```text

Passwords

CVV codes

Complete card numbers

```



API credentials are provided through environment variables rather than source code.



\---



\# 🧯 Graceful Degradation



The system has multiple levels of fallback.



```text

&#x20;               Gemini

&#x20;                 │

&#x20;            unavailable

&#x20;                 │

&#x20;                 ▼

&#x20;       Deterministic Router

&#x20;                 │

&#x20;                 ▼

&#x20;       Transactional Tools

&#x20;                 │

&#x20;                 ▼

&#x20;     Deterministic Generation

```



Therefore, a Gemini quota failure does not necessarily mean that the complete application becomes unusable.



For example, during testing the Gemini API reached its free-tier request quota. The backend continued to respond using:



```text

routing\_method:

deterministic\_fallback

```



and:



```text

generation\_method:

deterministic\_fallback

```



This demonstrates graceful degradation under real API failure conditions.



\---



\# 📋 Assignment Requirements Coverage



\## Task 1 — Build an AI Assistant



| Requirement          | Implementation                        | Status |

| -------------------- | ------------------------------------- | ------ |

| Major LLM provider   | Gemini                                | ✅      |

| Prompt engineering   | Routing and generation prompts        | ✅      |

| Temperature          | Configured during generation          | ✅      |

| top\_p                | Configured during generation          | ✅      |

| Structured output    | JSON response schema                  | ✅      |

| Tool calling         | Tool registry and transactional tools | ✅      |

| RAG                  | Retrieval pipeline                    | ✅      |

| Document ingestion   | RAG/document pipeline                 | ✅      |

| Chunking             | RAG pipeline                          | ✅      |

| Embeddings           | Vectorization pipeline                | ✅      |

| Vector retrieval     | Top-K retrieval                       | ✅      |

| Local LLM            | vLLM configuration                    | ✅      |

| Open-source model    | Qwen/Qwen3-0.6B                       | ✅      |

| Docker               | Dockerfile                            | ✅      |

| Docker Compose       | docker-compose.yml                    | ✅      |

| README               | This document                         | ✅      |

| Architecture diagram | To be inserted                        | ⏳      |



\---



\# 📋 Task 2 — Productionize the AI Assistant



| Requirement                 | Implementation                                      | Status         |

| --------------------------- | --------------------------------------------------- | -------------- |

| Web UI                      | Streamlit                                           | ✅              |

| Backend API                 | FastAPI                                             | ✅              |

| LLM integration             | Gemini provider                                     | ✅              |

| Model optimization          | Not required for primary Gemini API                 | ⚠️             |

| ONNX conversion             | Not applicable to Gemini API                        | ⚠️             |

| Inference optimization      | Local vLLM option                                   | ✅              |

| Concurrent request handling | FastAPI/Uvicorn architecture                        | ✅              |

| Latency considerations      | Caching, retrieval limits, deterministic tools      | ✅              |

| Prompt/response caching     | Implemented                                         | ✅              |

| Retry/error handling        | Provider exception handling and fallback            | ✅              |

| Rate-limit handling         | Gemini 429 graceful fallback                        | ✅              |

| Fallback model/provider     | Deterministic fallback + optional vLLM architecture | ✅              |

| Error handling              | Exception handling                                  | ✅              |

| Graceful degradation        | Implemented                                         | ✅              |

| Dockerization               | Dockerfile                                          | ✅              |

| Docker Compose              | docker-compose.yml                                  | ✅              |

| Deployment instructions     | README                                              | ✅              |

| Architecture diagram        | To be inserted                                      | ⏳              |

| Cloud deployment            | Not implemented                                     | Optional/Bonus |



\---



\# ⚠️ ONNX Requirement



The assignment lists ONNX conversion as:



```text

optional where applicable

```



The primary model used by ShopAssist AI is accessed through the Gemini API.



Because Gemini is a remotely hosted API model, its internal model weights are not available for conversion to ONNX within this project.



Therefore, ONNX conversion is not applicable to the primary Gemini deployment.



For the optional local model deployment, vLLM is used instead because it is specifically designed for efficient serving of transformer-based language models.



\---



\# ☁️ Cloud Deployment



Cloud deployment to:



```text

Azure

AWS

GCP

```



was not required for the core implementation.



It can be added as a future deployment stage.



The Dockerized architecture makes the application suitable for deployment to cloud container platforms.



\---



\# 🔮 Future Improvements



Potential future improvements include:



\## 1. Persistent Vector Database



Replace development-oriented retrieval storage with a production vector database such as:



```text

FAISS

Chroma

Qdrant

Pinecone

Weaviate

```



depending on deployment requirements.



\---



\## 2. Persistent Conversation Memory



Add conversation-level memory so the assistant can understand follow-up questions such as:



```text

User:

Where is my order ORD-1001?



Assistant:

Your order is shipped.



User:

When will it arrive?

```



\---



\## 3. Authentication



Add customer authentication so transactional tools can verify that the requesting customer owns the requested order.



\---



\## 4. Observability



Introduce:



\* Structured logging

\* Metrics

\* Tracing

\* Request IDs

\* Latency monitoring

\* LLM token monitoring

\* Error dashboards



\---



\## 5. Advanced Rate Limiting



Implement API-level rate limiting to protect the backend from excessive traffic.



\---



\## 6. Production Database



Replace mock JSON transactional data with a real database-backed order management system.



\---



\## 7. Automated Testing



Add comprehensive:



\* Unit tests

\* Integration tests

\* API tests

\* RAG evaluation

\* LLM evaluation

\* Load testing

\* Regression tests



\---



\# 🧠 Engineering Principles Demonstrated



ShopAssist AI demonstrates several important AI engineering principles:



\### Separation of Concerns



Routing, retrieval, tools, agents, LLM providers, and UI are separated.



\### Grounded Generation



The assistant uses retrieved knowledge and transactional tools instead of relying exclusively on model memory.



\### Deterministic Fallbacks



Critical customer-support functionality remains available during LLM failures.



\### Structured Interfaces



Components communicate through predictable structured data.



\### Provider Abstraction



LLM functionality is isolated behind a provider interface.



\### Containerized Deployment



The application can be reproduced using Docker Compose.



\### Production-Oriented Reliability



The system explicitly handles:



\* Rate limits

\* Provider failures

\* Invalid model responses

\* Missing identifiers

\* Missing knowledge

\* Tool failures



\---



\# 📊 End-to-End Example



Consider:



```text

I want to return order ORD-1003.

```



The system processes the request as follows:



```text

1\. Streamlit receives the message

&#x20;         ↓

2\. FastAPI receives POST /chat

&#x20;         ↓

3\. ChatService starts processing

&#x20;         ↓

4\. IntentRouter classifies request

&#x20;         ↓

5\. Intent = returns

&#x20;         ↓

6\. Order ID ORD-1003 is extracted

&#x20;         ↓

7\. check\_return\_eligibility is executed

&#x20;         ↓

8\. Mock order database is queried

&#x20;         ↓

9\. Order is confirmed as delivered

&#x20;         ↓

10\. Return eligibility = true

&#x20;         ↓

11\. RAG context is retrieved

&#x20;         ↓

12\. Specialized returns-agent instructions are loaded

&#x20;         ↓

13\. Gemini attempts response generation

&#x20;         ↓

14\. If Gemini fails, deterministic fallback is used

&#x20;         ↓

15\. Structured JSON response is returned

&#x20;         ↓

16\. Streamlit displays the customer-facing answer

```



Final customer-facing answer:



```text

Yes. This order is currently eligible for return under the available return policy.

```



\---



\# 🏁 Conclusion



ShopAssist AI demonstrates the design and implementation of a modern AI-powered customer-support system.



The project combines:



```text

LLM

\+

Prompt Engineering

\+

Intent Routing

\+

Specialized Agents

\+

Tool Calling

\+

RAG

\+

Embeddings

\+

Local LLM Serving

\+

Caching

\+

Fallbacks

\+

FastAPI

\+

Streamlit

\+

Docker

\+

Docker Compose

```



The resulting architecture is modular, testable, containerized, and designed with production reliability in mind.



The system was also tested under an actual Gemini API rate-limit condition. Rather than crashing, the application successfully degraded to deterministic routing and deterministic generation, demonstrating the reliability principles required for production AI systems.



The final architecture diagram should be added to:



```text

docs/architecture.png

```



and referenced from the Architecture section above.



\---



\# 👤 Created By



\*\*Rameshwor Poudel\*\*



