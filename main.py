from fastapi import FastAPI
from fraud_detection import fraud_detection_router  # Import your router

# Create the FastAPI app
app = FastAPI()

# Include the fraud detection API routes
app.include_router(fraud_detection_router)

# Health Check Endpoint
@app.get("/")
def read_root():
    return {"message": "Fraud Detection API is running"}

# You can also add other endpoints or routers here if necessary
