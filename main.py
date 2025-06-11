from fastapi import FastAPI
import os

app = FastAPI(title="Market Research Agent Team", version="1.0.0")

@app.get("/")
async def root():
    return {
        "message": "Market Research Agent Team - Phase 1 Live! 🚀",
        "status": "running",
        "next_milestone": "Business Intelligence Agent"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "market-research-agents"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
