from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

import os 

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

def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap = 300
    )

    return splitter.split_text(transcript)

def summarize(transcript : str) -> str:

    if not transcript.strip():
        raise ValueError("Transcript is empty.")

    llm = get_llm()

    map_prompt = ChatPromptTemplate.from_messages([
(
"system",
"""
You are an expert meeting summarizer.

Summarize this transcript section.

Keep:

• Important discussions

• Decisions

• Action items

• Deadlines

Ignore small talk.
"""
),
("human","{text}")
])

    map_chain = map_prompt | llm | StrOutputParser()

    chunks = split_transcript(transcript)

    chunk_summaries = [map_chain.invoke({"text" : chunk}) for chunk in chunks]

    combined = "\n\n".join(chunk_summaries)

    combined_prompt = ChatPromptTemplate.from_messages(
        [
        (
            "system",
            "You are an expert meeting summarizer. Combine these partial summaries "
            "into one final professional meeting summary in bullet points.",
        ),
        ("human", "{text}"),
    ]
    )

    combined_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | combined_prompt | llm | StrOutputParser()
    )

    try:
        return combined_chain.invoke(combined)
    except Exception as e:
        return f"Summary generation failed:\n{e}"

def generate_title(transcript : str) -> str:

    if not transcript.strip():
        raise ValueError("Transcript is empty.")

    llm = get_llm()

    title_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | 
        ChatPromptTemplate.from_messages([
             (
"system",
"""
Generate a concise professional meeting title.

Rules:

- Maximum 8 words
- No punctuation at the end
- Do not use quotation marks
- Return only the title
"""
),
            ("human", "{text}"),
        ])
        | llm
        |StrOutputParser()
    )

    return title_chain.invoke(transcript[:2000])




