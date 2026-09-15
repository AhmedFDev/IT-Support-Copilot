from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.search import search_solutions

from app.llm import generate_answer

from fastapi.responses import FileResponse


app = FastAPI(
    title="AI IT Support Assistant",
    description="An API that retrieves solutions for common IT support questions.",
    version="1.0.0",
)


class SupportRequest(BaseModel):
    question: str = Field(
        min_length=3,
        description="The user's IT support question.",
    )


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy"
    }


@app.post("/support")
def get_support(
    request: SupportRequest,
) -> dict:
    matches = search_solutions(request.question)

    if not matches:
        return {
            "question": request.question,
            "answer": (
                "I couldn't find enough information. Please contact IT support. "
            ),
            "matches": [],
        }

    answer = generate_answer(
        request.question,
        matches
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": matches,
    }