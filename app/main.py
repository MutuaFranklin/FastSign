from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.routers import auth, documents
from app.database import Base, engine, get_db
from fastapi.responses import RedirectResponse
from app.models import user, document  # Import models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastSign", description="Digital Signature Solution")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include only auth router for now
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        # Try to execute a simple query
        db.execute("SELECT 1")
        return {"message": "Successfully connected to the database"}
    except Exception as e:
        return {"error": f"Database connection failed: {str(e)}"} 