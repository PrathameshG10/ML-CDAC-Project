import os
import time
from datetime import datetime
from dotenv import load_dotenv

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()


def run_pipeline(source: str, language: str = "english") -> dict:
    """Run the complete  Intelligence Meeting pipeline."""

    print("\n" + "=" * 70)
    print("🎬  Intelligence Meeting Assistant")
    print("=" * 70)

    start_time = time.time()
    meeting_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # -----------------------------------------------------------------
    # Step 1
    # -----------------------------------------------------------------
    print("\n[1/6] Processing Audio...")
    chunks = process_input(source)
    print(f"✔ Audio Ready ({len(chunks)} chunk(s))")

    # -----------------------------------------------------------------
    # Step 2
    # -----------------------------------------------------------------
    print("\n[2/6] Transcribing...")
    transcript = transcribe_all(chunks, language)

    if not transcript.strip():
        raise RuntimeError("Transcription produced an empty transcript.")

    print("✔ Transcription Completed")

    # -----------------------------------------------------------------
    # Step 3
    # -----------------------------------------------------------------
    print("\n[3/6] Generating Title...")
    title = generate_title(transcript)
    print("✔ Title Generated")

    # -----------------------------------------------------------------
    # Step 4
    # -----------------------------------------------------------------
    print("\n[4/6] Generating Summary...")
    summary = summarize(transcript)
    print("✔ Summary Generated")

    # -----------------------------------------------------------------
    # Step 5
    # -----------------------------------------------------------------
    print("\n[5/6] Extracting Information...")

    action_items = extract_action_items(transcript)
    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)

    print("✔ Extraction Completed")

    # -----------------------------------------------------------------
    # Step 6
    # -----------------------------------------------------------------
    print("\n[6/6] Building RAG Engine...")

    rag_chain = build_rag_chain(transcript)

    print("✔ RAG Ready")

    processing_time = round(time.time() - start_time, 2)

    # ---------------- Statistics -----------------

    word_count = len(transcript.split())

    sentence_count = (
        transcript.count(".")
        + transcript.count("?")
        + transcript.count("!")
    )

    char_count = len(transcript)

    stats = {
        "Words": word_count,
        "Characters": char_count,
        "Sentences": sentence_count,
        "Audio Chunks": len(chunks),
    }

    return {
        "meeting_date": meeting_date,
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
        "processing_time": processing_time,
        "stats": stats,
    }


if __name__ == "__main__":

    print("=" * 70)
    print("🎬 AI Meeting Intelligence Assistant")
    print("=" * 70)

    source = input("\nEnter YouTube URL or Local File Path:\n> ").strip()

    if not source:
        print("\n❌ Source cannot be empty.")
        exit()

    if not (source.startswith("http") or os.path.exists(source)):
        print("\n❌ Invalid file path or URL.")
        exit()

    language = input("\nLanguage (english/hinglish): ").strip().lower()

    if language not in ["english", "hinglish"]:
        language = "english"

    try:

        result = run_pipeline(source, language)

    except Exception as e:

        print("\n" + "=" * 70)
        print("❌ Pipeline Failed")
        print("=" * 70)
        print(e)
        exit()

    print("\n" + "=" * 70)
    print("📌 MEETING DETAILS")
    print("=" * 70)

    print(f"\nMeeting Date : {result['meeting_date']}")
    print(f"Meeting Title: {result['title']}")

    print("\n" + "=" * 70)
    print("📋 SUMMARY")
    print("=" * 70)
    print(result["summary"])

    print("\n" + "=" * 70)
    print("✅ ACTION ITEMS")
    print("=" * 70)
    print(result["action_items"])

    print("\n" + "=" * 70)
    print("🔑 KEY DECISIONS")
    print("=" * 70)
    print(result["key_decisions"])

    print("\n" + "=" * 70)
    print("❓ OPEN QUESTIONS")
    print("=" * 70)
    print(result["open_questions"])

    print("\n" + "=" * 70)
    print("📊 MEETING STATISTICS")
    print("=" * 70)

    for key, value in result["stats"].items():
        print(f"{key:15}: {value}")

    print(f"{'Processing Time':15}: {result['processing_time']} sec")

    print("\n" + "=" * 70)
    print("💬 CHAT WITH YOUR MEETING")
    print("=" * 70)

    print("""
Available Commands

/summary      -> Show meeting summary
/actions      -> Show action items
/decisions    -> Show key decisions
/questions    -> Show open questions
/stats        -> Show meeting statistics
/help         -> Show commands
/exit         -> Exit
""")

    rag_chain = result["rag_chain"]

    while True:

        question = input("\nYou: ").strip()

        if not question:
            continue

        cmd = question.lower()

        if cmd in ["/exit", "exit", "quit", "q"]:

            print("\nMeeting session completed.")
            print("Thank you for using AI Meeting Intelligence Assistant.")
            print("👋 Goodbye!")
            break

        elif cmd == "/summary":
            print("\n" + result["summary"])

        elif cmd == "/actions":
            print("\n" + result["action_items"])

        elif cmd == "/decisions":
            print("\n" + result["key_decisions"])

        elif cmd == "/questions":
            print("\n" + result["open_questions"])

        elif cmd == "/stats":
            print()

            for key, value in result["stats"].items():
                print(f"{key:15}: {value}")

            print(f"{'Processing Time':15}: {result['processing_time']} sec")

        elif cmd == "/help":

            print("""
Available Commands

/summary
/actions
/decisions
/questions
/stats
/help
/exit
""")

        else:

            answer = ask_question(rag_chain, question)

            print("\n🤖 Assistant:\n")
            print(answer)