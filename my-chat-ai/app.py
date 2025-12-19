from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

print("Loading Kova AI model...")



model_name = "./models/Kova-Ai-model-beta"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name)

print("✅ Kova AI model loaded!")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "Kova AI is running!", "model": "Kova AI v0.1"}

@app.post("/chat")
def chat(request: ChatRequest):
    user_message = request.message.lower()
    

    creator_keywords = ["who created", "who made", "who built", "who developed", "who trained", "your creator", "your maker", "made you"]
    if any(keyword in user_message for keyword in creator_keywords):
        return {
            "response": "I am a custom AI model made by NextGen!",
            "model": "Kova AI v0.1"
        }
    
  
    prompt = f"### Human: {request.message}\n### Assistant:"
    
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs, 
        max_length=150, 
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        temperature=0.7,
        top_p=0.9  
    )
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
  
    if "### Assistant:" in response_text:
        response_text = response_text.split("### Assistant:")[-1].strip()
    
    return {
        "response": response_text,
        "model": "Kova AI v0.1"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)