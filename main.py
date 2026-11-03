from fastapi import FastAPI

app = FastAPI(title="JobPilot")

@app.get("/health")
def health():
    return {"status": "ok"}
