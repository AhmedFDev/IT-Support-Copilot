from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def generate_answer(question, matches):

    context = ""

    for match in matches:
        context += f"Title: {match['title']}\n"

        for step in match["steps"]:
            context += f"- {step}\n"

    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions=(
            "You are an IT support assistant. "
            "Answer the user's question using only the provided "
            "troubleshooting information. "
            "Do not invent information. "
            "If the provided information is insufficient, tell the "
            "user to contact IT support."
        ),
        input=f"""
User question:
{question}

Troubleshooting information:
{context}
"""
    )

    return response.output_text



