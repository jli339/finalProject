import pandas as pd
import joblib
from datetime import datetime

# 加载训练好的模型（包含预处理器 + 分类器）
model = joblib.load('FinalProject/ml_models/priority_model.pkl')

# 用于从用户输入中计算时间特征，并预测优先级
def predict_priority(user_input):
    """
    参数 user_input 是一个字典，包含：
    - Scheduled_Start (datetime)
    - Deadline (datetime)
    - Processing_Time (float)
    - 其他原始模型输入特征
    """

    user_input.columns = [c.lower() for c in user_input.columns]

    if isinstance(user_input, pd.DataFrame):
        user_input = user_input.iloc[0]
    # 解析时间
    print(user_input)
    start = pd.to_datetime(user_input['scheduled_start'])
    deadline = pd.to_datetime(user_input['deadline'])
    processing_time = float(user_input['processing_time'])

    # 自动推导时间衍生特征
    time_budget = (deadline - start).total_seconds()/ 60
    time_risk = time_budget - processing_time
    exceeds_deadline = int(time_risk < 0)

    # 构造模型输入
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

    # 强制列顺序对齐
    ordered_columns = [
        'Operation_Type', 'Material_Used', 'Processing_Time',
        'Energy_Consumption', 'Machine_Availability', 'Machine_ID',
        'Time_Budget', 'Time_Risk', 'Exceeds_Deadline'
    ]

    model_input = model_input[ordered_columns]

    # 最关键的 debug 打印
    print("🚨 model_input.columns:", list(model_input.columns))
    print("🚨 model_input shape:", model_input.shape)
    print("✔ used input:", model_input.columns.tolist())
    # 模型预测
    priority_label = model.predict(model_input)[0]
    proba = model.predict_proba(model_input)[0]
    priority_score = proba[model.classes_.tolist().index('High')]

    return {
        'priority_label': priority_label,
        'priority_score': round(priority_score, 4),

    }