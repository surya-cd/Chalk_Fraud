import joblib
import os

def load_model_and_encoders():
    # Update the paths to reflect the new directory structure
    base_path = os.path.dirname(__file__)  # Get the directory of the current file
    model_path = os.path.join(base_path, 'Encoder weights', 'decision_tree_fraud_model.pkl')
    label_encoder_ip_path = os.path.join(base_path, 'Encoder weights', 'ip_encoder.pkl')
    label_encoder_publisher_path = os.path.join(base_path, 'Encoder weights', 'publisher_encoder.pkl')
    label_encoder_request_id_path = os.path.join(base_path, 'Encoder weights', 'request_id_encoder.pkl')
    label_encoder_uid_path = os.path.join(base_path, 'Encoder weights', 'uid_encoder.pkl')
    invalid_ips_set_path = os.path.join(base_path, 'Encoder weights', 'invalid_ips_set.pkl')

    model = joblib.load(model_path)
    label_encoder_ip = joblib.load(label_encoder_ip_path)
    label_encoder_publisher = joblib.load(label_encoder_publisher_path)
    label_encoder_request_id = joblib.load(label_encoder_request_id_path)
    label_encoder_uid = joblib.load(label_encoder_uid_path)
    invalid_ips_set = joblib.load(invalid_ips_set_path)

    return model, label_encoder_ip, label_encoder_publisher, label_encoder_request_id, label_encoder_uid, invalid_ips_set
