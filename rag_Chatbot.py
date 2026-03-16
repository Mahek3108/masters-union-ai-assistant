import os
from dotenv import load_dotenv
from mistralai import Mistral

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

#load api key
load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")

MODEL = "mistral-small-latest"

client = Mistral(api_key=API_KEY)


# EMBEDDING MODEL


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# LOAD VECTOR DATABASES


priority_db = FAISS.load_local(
    "vector_db_priority",
    embeddings,
    allow_dangerous_deserialization=True
)

fallback_db = FAISS.load_local(
    "vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)


# MEMORY


chat_memory = []


# CONVERT COURSE NAME → FILE KEY


def course_to_key(course):

    return (
        course.lower()
        .replace("&", "and")
        .replace("(", "")
        .replace(")", "")
        .replace(",", "")
        .replace(" ", "_")
    )


# RETRIEVE CONTEXT

from course_config import COURSE_FILE_MAP   
def retrieve_context(query, course):

    course_key = COURSE_FILE_MAP[course]

    # FIRST SEARCH PRIORITY DB 
    docs = priority_db.similarity_search(
        query,
        k=4,
        filter={"course": course_key}
    )

    # IF NOTHING FOUND --> SEARCH FULL DB
    if len(docs) == 0:

        docs = fallback_db.similarity_search(query, k=4)

    context = "\n".join([doc.page_content for doc in docs])

    sources = list(set([doc.metadata.get("source", "unknown") for doc in docs]))

    return context, sources


# GENERATE ANSWER

def general_answer(query):
    q=query.lower()
    if "location" in q or "where" in q:
        return "Masters Union is located in Gurugram, Haryana, India."
    docs = fallback_db.similarity_search(query, k=4)

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an AI assistant helping users with information about Masters Union.

Context:
{context}

Question:
{query}
"""

    response = client.chat.complete(
        model=MODEL,
        messages=[{"role":"user","content":prompt}]
    )

    answer = response.choices[0].message.content

    return answer

def generate_answer(query, course):

    context, sources = retrieve_context(query, course)

    history = "\n".join(chat_memory[-4:])

    prompt = f"""
You are an AI assistant helping prospective students understand the programme:

{course}

Conversation history:
{history}

Use ONLY the provided context.
Important rules:
- Do NOT paraphrase location or factual details.
- If the context mentions a city or place name, mention it exactly.
- Do NOT add marketing or promotional language.
- Answer factually.

If the context does not belong to the selected course, say, don't use it and say you couldn't find the information in the course materials.

If the answer is not present in the context say:
"I could not find this information in the programme materials."

Context:
{context}

Question:
{query}

Provide a clear and concise answer for a prospective student.
"""

    response = client.chat.complete(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    # store conversation memory
    chat_memory.append(f"User: {query}")
    chat_memory.append(f"Assistant: {answer}")

    return answer, sources