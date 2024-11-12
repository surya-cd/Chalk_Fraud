from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import pandas as pd


fraud_detection_router = APIRouter()

# Define the input schema using Pydantic with field validation
class FraudDetectionInput(BaseModel):
    ip_address: str
    publisher_name: str
    request_id: str
    lat: float = Field(..., ge=-90, le=90, description="Latitude must be between -90 and 90.")
    long: float = Field(..., ge=-180, le=180, description="Longitude must be between -180 and 180.")
    uid: str

# Helper function for encoding checks
def encode_if_seen(value, encoder, value_name):
    if value not in encoder.classes_:
        return None, f"Unseen {value_name}: {value}. Automatically classified as: Not Fraud"
    try:
        return encoder.transform([value])[0], None
    except ValueError:
        return None, f"Unseen {value_name}: {value}. Automatically classified as: Not Fraud"

@fraud_detection_router.post("/predict/")
async def predict_fraud(input_data: FraudDetectionInput):
    # Import here to avoid circular import issues
    from models.model_loader import load_model_and_encoders

    # Load the model and encoders
    model, label_encoder_ip, label_encoder_publisher, label_encoder_request_id, label_encoder_uid, invalid_ips_set = load_model_and_encoders()

    # Check if the IP is in the invalid list
    if input_data.ip_address in invalid_ips_set:
        return {"classification": "Fraud (Blocked IP)"}

    # Encode inputs
    ip_encoded, error_message = encode_if_seen(input_data.ip_address, label_encoder_ip, "IP Address")
    if error_message:
        return {"classification": "Not Fraud", "detail": error_message}

    publisher_encoded, error_message = encode_if_seen(input_data.publisher_name, label_encoder_publisher, "Publisher")
    if error_message:
        return {"classification": "Not Fraud", "detail": error_message}

    request_id_encoded, error_message = encode_if_seen(input_data.request_id, label_encoder_request_id, "Request ID")
    if error_message:
        return {"classification": "Not Fraud", "detail": error_message}

    uid_encoded, error_message = encode_if_seen(input_data.uid, label_encoder_uid, "UID")
    if error_message:
        return {"classification": "Not Fraud", "detail": error_message}

    # Create input dataframe for prediction
    input_dataframe = pd.DataFrame({
        'IP_Encoded': [ip_encoded],
        'Publisher_Encoded': [publisher_encoded],
        'Request_ID_Encoded': [request_id_encoded],
        'UID_Encoded': [uid_encoded],
        'Lat_used': [input_data.lat],
        'Longitude_used': [input_data.long]
    })

    # Make the prediction
    try:
        prediction = model.predict(input_dataframe)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    # Return the result
    return {"classification": "The Ad belongs Fraud Category" if prediction[0] == 1 else "The Ad belongs to Not Fraud Category"}
