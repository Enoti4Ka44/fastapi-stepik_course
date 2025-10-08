from fastapi import FastAPI, Form
from fastapi.responses import FileResponse

app = FastAPI()

@app.get('/', response_class=FileResponse)
def root():
    return "index.html"

@app.post('/calculate')
def calculate(num1: float = Form(...), num2: float = Form(...)):
    print("число 1 =", num1, "   число 2 =", num2)
    return {"Результат": num1 + num2}
