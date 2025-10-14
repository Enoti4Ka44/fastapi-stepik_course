from fastapi import FastAPI
from .models.models import Feedback

app = FastAPI()

lst = []


@app.post("/feedback")
async def send_feedback(feedback: Feedback):
    lst.append({"name": feedback.name, "comments": feedback.message})
    return f"Feedback received. Thank you, {feedback.name}!"


@app.get("/comments")
async def show_feedback():
    return lst