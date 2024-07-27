from fastapi import FastAPI, HTTPException

from pydantic import BaseModel
from transformers import DistilBertForQuestionAnswering, DistilBertTokenizer
import torch
import logging

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Allow requests from your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



model_name = "distilbert-base-uncased-distilled-squad"
model = DistilBertForQuestionAnswering.from_pretrained(model_name)
tokenizer = DistilBertTokenizer.from_pretrained(model_name)

class QARequest(BaseModel):
    question: str
    context: str

def preprocess(question: str, context: str):
    inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
    return inputs


@app.post("/qa/")
def get_answer(request: QARequest):
    try:
        inputs = preprocess(request.question, request.context)
        with torch.no_grad():
            outputs = model(**inputs)
            answer_start_scores = outputs.start_logits
            answer_end_scores = outputs.end_logits

        answer_start = torch.argmax(answer_start_scores)
        answer_end = torch.argmax(answer_end_scores) + 1

        answer_tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end])
        answer = tokenizer.convert_tokens_to_string(answer_tokens)

        # Log intermediate outputs
        print(f"Start Logits: {answer_start_scores}")
        print(f"End Logits: {answer_end_scores}")
        print(f"Answer Tokens: {answer_tokens}")
        print(f"Answer: {answer}")

        if not answer.strip():  # Check if the answer is empty
            raise HTTPException(status_code=404, detail="No answer found.")

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
