import asyncio  # Import asyncio to run async functions
#from fraud_detection import predict_fraud  # Import predict_fraud from fraud_detection.py
from fastapi import HTTPException
# from fraud_detection import FraudDetectionInput  # Import the input model
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fraud_detection import predict_fraud, FraudDetectionInput


# Define the data to send
data = {
    "ip_address": "98.227.129.109",
    "publisher_name": "appnexus",
    "request_id": "f0fcc7a2-4343-4cd6-a77b-b654d96255cf",
    "lat": 40.4339,
    "long": -79.9996,
    "uid": "96064616-a4d7-4055-8ee3-4128cc11719f"
}

# Create an instance of the input model
input_data = FraudDetectionInput(**data)

# Asynchronous main function to run predict_fraud
async def main():
    try:
        prediction = await predict_fraud(input_data)  # Use await to call the async function

        # Print the response from the prediction
        print(prediction)

    except HTTPException as e:
        print(f"HTTP Exception: {e.detail}")
    except Exception as e:
        print(f"Error: {str(e)}")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
