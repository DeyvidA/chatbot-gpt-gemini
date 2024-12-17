from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from gemini_ia import gemini_ai_client
from open_ai import open_ai_client
from models import PromptRequest

from fastapi.middleware.cors import CORSMiddleware
# Add CORS middleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


open_ai_client()
@app.get("/")
async def root():    
    return {"message": "Hello World"}


@app.post("/ask-gemini-ai")
async def ask(body: PromptRequest):
    try:
            model = gemini_ai_client().GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(body.prompt)
            print(response.text)
            ai_message = response.text
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))
    return {"message": ai_message}


@app.post("/ask-open-ai")
async def ask(body: PromptRequest):
    client = open_ai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": body.prompt
            }
        ]
    )
    ai_message = response.choices[0].message.content
    
    return {"message": ai_message}
            
