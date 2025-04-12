import pandas as pd
import joblib
from datetime import datetime

# load the model
model = joblib.load('FinalProject/ml_models/priority_model.pkl')

# This function takes input and send to the model to calculate priority
def predict_priority(user_input):

    # Column names are converted to lowercase to ensure consistency.
    user_input.columns = [c.lower() for c in user_input.columns]

    # If a DataFrame is passed, only the first row is processed.
    if isinstance(user_input, pd.DataFrame):
        user_input = user_input.iloc[0]

    #  Converts 'scheduled_start' and 'deadline' to datetime.
    start = pd.to_datetime(user_input['scheduled_start'])
    deadline = pd.to_datetime(user_input['deadline'])
    processing_time = float(user_input['processing_time'])

    # calculate time features(input features)
    time_budget = (deadline - start).total_seconds()/ 60
    time_risk = time_budget - processing_time
    exceeds_deadline = int(time_risk < 0)

    # construct the input for the model
    model_input = pd.DataFrame([{
        'Operation_Type': user_input['operation_type'],
        'Material_Used': float(user_input['material_used']),
        'Processing_Time': float(user_input['processing_time']),
        'Energy_Consumption': float(user_input['energy_consumption']),
        'Machine_Availability': float(user_input['machine_availability']),
        'Machine_ID': user_input.get('machine_id') or user_input.get('machine_ID'),
        'Time_Budget': time_budget,
        'Time_Risk': time_risk,
        'Exceeds_Deadline': exceeds_deadline
    }])

    # ensure columns are in the correct sequence
    ordered_columns = [
        'Operation_Type', 'Material_Used', 'Processing_Time',
        'Energy_Consumption', 'Machine_Availability', 'Machine_ID',
        'Time_Budget', 'Time_Risk', 'Exceeds_Deadline'
    ]

    model_input = model_input[ordered_columns]

    # Just for testing while development
    print(" model_input.columns:", list(model_input.columns))
    print(" model_input shape:", model_input.shape)
    print("✔ used input:", model_input.columns.tolist())

    # Model prediction
    priority_label = model.predict(model_input)[0]
    proba = model.predict_proba(model_input)[0]       # predicted probability
    priority_score = proba[model.classes_.tolist().index('High')]

    #return the result
    return {
        'priority_label': priority_label,
        'priority_score': round(priority_score, 4),

    }