# 🎓 Masters Union AI Assistant

An AI-powered course assistant designed to help prospective students explore Masters Union programmes and quickly get answers to their queries.

The assistant understands natural language questions and retrieves relevant information from programme materials such as curriculum, admissions details, and institute information.

The system uses **Retrieval-Augmented Generation (RAG)** to ensure answers are grounded in real data instead of hallucinating information.

---

# 🚀 Features

• AI chatbot for programme discovery  
• Natural language question answering  
• Retrieval-Augmented Generation (RAG)  
• Course-specific question answering  
• Institute information support  
• Intelligent query routing  
• Clean Streamlit chatbot interface  
• Context-grounded responses  

---

# 🧠 System Architecture

The assistant uses a **multi-layer RAG architecture**.

1. **Priority Vector Database**
   - Contains curated programme-specific information
   - Used when a user selects a specific programme

2. **Fallback Vector Database**
   - Contains scraped website content
   - Used for institute-level questions

3. **LLM Response Generation**
   - Generates responses using retrieved context

System Flow:

User Query  
↓  
Mode Selection  
↓  
Course Query → Course Vector DB  
↓  
Others → Institute Vector DB  
↓  
LLM Response Generation

---

# 📂 Project Structure

masters-union-ai-assistant

app.py  
Streamlit chatbot interface

rag_chatbot.py  
RAG retrieval and answer generation logic

course_config.py  
Programme list and configuration

manual_data/  
Curated programme text data

clean_data/  
Cleaned scraped website content

vector_db_priority/  
Programme vector database (not included in repo)

vector_db_clean/  
Website vector database (not included in repo)

requirements.txt  
Python dependencies

README.md  
Project documentation

---

# ⚙️ Installation

### 1. Clone the repository

git clone https://github.com/YOUR_USERNAME/masters-union-ai-assistant.git

cd masters-union-ai-assistant

---

### 2. Create a virtual environment

python -m venv venv

Activate environment

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate

---

### 3. Install dependencies

pip install -r requirements.txt

---

# 🔑 Environment Variables

Create a `.env` file in the root directory and add your API key.

MISTRAL_API_KEY=your_api_key_here

The `.env` file is ignored in GitHub for security.

---

# 📊 Vector Database Setup

Vector databases are **not included in the repository** because they can be large.

They must be generated locally from the dataset.

Typical process:

1. Load raw text data
2. Split documents into chunks
3. Generate embeddings
4. Store vectors in FAISS

Output folders generated locally:

vector_db_priority/  
vector_db_clean/

---

# ▶️ Running the Application

Run the Streamlit application:

streamlit run app.py

The chatbot will open automatically in your browser.

---

# 💬 Example Queries

Programme Queries

• What is the curriculum of the AI programme?  
• What are the fees for the Data Science programme?  
• What skills will I learn in Marketing?

Institute Queries

• Where is Masters Union located?  
• Who teaches at Masters Union?  
• What makes Masters Union unique?

---

# 🧩 Technologies Used

Python  
Streamlit  
FAISS Vector Database  
Sentence Transformers  
Mistral LLM  
Retrieval-Augmented Generation (RAG)

---

# 🛡️ Hallucination Control

The system reduces hallucination by:

• Restricting answers to retrieved context  
• Using programme-specific filtering  
• Implementing fallback retrieval layers  
• Providing contact information for unknown queries

---

# 📬 Contact

For further information about Masters Union programmes:

info@mastersunion.org

---

# 👩‍💻 Author

Developed as an AI-powered programme discovery assistant using Retrieval-Augmented Generation.
