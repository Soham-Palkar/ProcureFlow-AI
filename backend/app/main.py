
from fastapi import FastAPI, HTTPException

from app.database.connection import test_db_connection
from app.routes.suppliers import router as supplier_router
from app.routes.purchase_requests import router as purchase_request_router
from app.routes.quotations import router as quotation_router


app = FastAPI(
    title="ProcureFlow AI",
    description="AI-powered procurement management platform",
    version="1.0.0"
)

app.include_router(supplier_router)
app.include_router(purchase_request_router)
app.include_router(quotation_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to ProcureFlow AI",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/db-health")
def database_health():
    try:
        version = test_db_connection()

        return {
            "status": "connected",
            "database": "Supabase PostgreSQL",
            "version": version
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )
