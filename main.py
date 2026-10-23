import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Vibe Coding AI Assistant API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection Setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client.vibe_coding_chat
chat_collection = db.conversations


# Initialize OpenAI Client (or adjust for Claude)
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Tone Mapping for the "Vibe Check" feature
TONE_INSTRUCTIONS = {
    "Professional": "You are a professional, formal, and precise assistant. Maintain a business-appropriate tone.",
    "Casual": "You are a friendly, relaxed, and casual assistant. Keep it conversational and laid-back.",
    "Concise": "You are an ultra-concise assistant. Provide direct, brief, and straight-to-the-point answers."
}

class ChatRequest(BaseModel):
    thread_id: str
    prompt: str
    tone: str = "Professional"  # Default tone

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Get system instruction based on the selected tone toggle
        system_instruction = TONE_INSTRUCTIONS.get(
            request.tone, 
            TONE_INSTRUCTIONS["Professional"]
        )

        # Call AI API with streaming enabled
        stream = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": request.prompt}
            ],
            stream=True
        )

        async def generate():
            complete_response = ""
            async for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                complete_response += content
                yield content

            # Save the conversation to MongoDB asynchronously after streaming completes
            await chat_collection.insert_one({
                "threadId": request.thread_id,
                "timestamp": datetime.utcnow(),
                "userPrompt": request.prompt,
                "aiResponse": complete_response,
                "tone": request.tone
            })

        return StreamingResponse(generate(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history/{thread_id}")
async def get_history(thread_id: str):
    # Fetch past conversation threads for the History Sidebar
    messages = await chat_collection.find({"threadId": thread_id}).sort("timestamp", 1).to_list(length=100)
    for msg in messages:
        msg["_id"] = str(msg["_id"])  # Convert ObjectId to string for JSON serialization
    return messages

@app.get("/")
def root():
    return {"status": "Vibe Coding Backend is running!"}