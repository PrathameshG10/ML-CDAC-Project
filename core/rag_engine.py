import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from core.vector_store import build_vector_store, load_vector_store, get_retriever

def get_llm():
    api_key = os.getenv("MISTRAL_API_KEY")

    if not api_key:
        raise ValueError(
            "MISTRAL_API_KEY not found. Check your .env file."
        )

    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=api_key,
        temperature=0,
    )

def format_docs(docs):

    text=[]

    for i,doc in enumerate(docs):

        text.append(
            f"Chunk {i+1}\n{doc.page_content}"
        )

    return "\n\n".join(text)

def build_rag_chain(transcript:str):

    vector_store = build_vector_store(transcript)

    retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k":4,
        "fetch_k":10
    }
)

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(

        [(
            "system",
            """You are an expert meeting assistant. Answer the user's question 
based ONLY on the meeting transcript context provided below.

If the answer is not found in the context, say: 
"I could not find this information in the meeting transcript."

Always be concise and precise. If quoting someone, mention it clearly.

Context from meeting transcript:
{context}""",
        ),
        ("human", "{question}"),
    ]
    )

    #full LCEL Rag pipeline 

    rag_chain = (

        {"context" : retriever | RunnableLambda(format_docs),
         "question": RunnablePassthrough()
         }
         |prompt|llm|StrOutputParser()
    )

    return rag_chain


def load_rag_chain():
    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k":4,
        "fetch_k":10
    }
)

    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
(
"system",
"""
You are an AI Meeting Intelligence Assistant.

Answer ONLY using the provided meeting transcript.

Rules:

1. Never make up information.

2. If the answer is unavailable say:
"I could not find this information in the meeting transcript."

3. Keep answers concise.

4. Mention names only if they appear.

5. Mention dates only if they appear.

6. If multiple answers exist, summarize them.

Meeting Transcript

{context}
"""
),
("human","{question}")
])

    rag_chain = (
        {
            "context":  retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def ask_question(rag_chain, question:str) -> str:
    print(f"Question : {question}")
    try:

        answer = rag_chain.invoke(question)

    except Exception as e:
        print(f"RAG Error: {e}")
        answer = (
            "Sorry, I couldn't answer that question "
            "because an internal error occurred."
        )
    print(f"answer :{answer}")
    return answer
