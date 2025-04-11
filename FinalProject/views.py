import joblib
import pandas as pd
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
# from FinalProject.models import Credential
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login
from django.utils.text import normalize_newlines
from .forms import PriorityForm, UnassignedTasks, AssignedTasks
from .predictor import predict_priority
from .models import UnassignedTasks, AssignedTasks, HistoricalTasks
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

ML_MODEL_PATH='FinalProject/ml_models/priority_model.pkl'
model=joblib.load(ML_MODEL_PATH)


# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    else:
        username = request.POST.get('usr')
        password = request.POST.get('pwd')
        print("usr:", username)
        print("pwd:", password)
        user=authenticate(request,username=username,password=password)
        print("User object:", user)
        print("User type:", type(user))
        if user is not None:
            print(user.last_login)
            django_login(request,user)
            return redirect('/index/')
        else:
            return render(request,'login.html',{"error":"unauthorized"})

def predict_view(request):
    result = None

    if request.method == 'POST':
        form = PriorityForm(request.POST)

        if form.is_valid():
            # 提取已验证的字段数据
            print(1)
            input_data = form.cleaned_data
            input_data=pd.DataFrame([input_data])
            # 调用模型预测函数
            result = predict_priority(input_data)

    else:
        form = PriorityForm()

    print("🧾 POST 数据：", request.POST)
    print("📋 表单错误：", form.errors)
    return render(request, 'predict.html', {
        'form': form,
        'result': result

    })
# def get_credential(request):
#     answer = Credential.objects.all().values('username')
#     print(answer)
#     return HttpResponse(answer)

def unassigned_list(request):
    tasks = UnassignedTasks.objects.all()
    form=UnassignedTasks()
    return render(request,'Unassigned_list.html',{'tasks':tasks,'form':form})

@csrf_exempt

def predict_unassigned(request,task_id):

    if request.method == "POST":
        task = get_object_or_404(UnassignedTasks, pk=task_id)
        scheduled_start = request.POST.get('scheduled_start')
        deadline = request.POST.get('deadline')
        scheduled_start = pd.to_datetime(scheduled_start)
        deadline = pd.to_datetime(deadline)

        time_budget = (deadline - scheduled_start).total_seconds()/60
        time_risk =time_budget-task.processing_time
        exceeds_deadline=time_risk<0

        input_data=pd.DataFrame([{
            'operation_type': task.operation_type,
            'material_used': task.material_used,
            'processing_time': task.processing_time,
            'energy_consumption': task.energy_consumption,
            'machine_availability': task.machine_availability,
            'machine_ID': task.machine_id,
            'time_budget': time_budget,
            'time_risk': time_risk,
            'exceeds_deadline': exceeds_deadline,
            'scheduled_start': scheduled_start,
            'deadline': deadline
        }])

        prediction = predict_priority(input_data)

        print(prediction)

        AssignedTasks.objects.create(
            material_used=task.material_used,
            processing_time=task.processing_time,
            energy_consumption=task.energy_consumption,
            machine_availability=task.machine_availability,
            machine_id=task.machine_id,
            scheduled_start=scheduled_start,
            deadline=deadline,
            time_budget=time_budget,
            time_risk=time_risk,
            exceeds_deadline=exceeds_deadline,
            priority_label=prediction['priority_label'],
            priority_score=prediction['priority_score'],
        )
        UnassignedTasks.objects.filter(id=task_id).delete()
        return JsonResponse({
            'priority_label': prediction['priority_label'],
            'priority_score': round(prediction['priority_score'], 3)
        })
    return JsonResponse({'error': 'Invalid method'}, status=400)

def assigned_list(request):
    if request.GET.get('sort') == 'priority':
        tasks = AssignedTasks.objects.all().order_by('-priority_score')
        sorted_flag = True
    else:
        tasks = AssignedTasks.objects.all().order_by('id')  # 默认按创建顺序
        sorted_flag = False

    return render(request, 'assigned_list.html', {
        'tasks': tasks,
        'sorted': sorted_flag
    })

@csrf_exempt
def assigned_view(request, task_id):
    if request.method == 'POST':
        try:
            task = AssignedTasks.objects.get(id=task_id)

            # 写入历史表
            HistoricalTasks.objects.create(
                material_used=task.material_used,
                processing_time=task.processing_time,
                energy_consumption=task.energy_consumption,
                machine_availability=task.machine_availability,
                machine_id=task.machine_id,
                scheduled_start=task.scheduled_start,
                deadline=task.deadline,
                time_budget=task.time_budget,
                time_risk=task.time_risk,
                exceeds_deadline=task.exceeds_deadline,
                priority_label=task.priority_label
            )

            # 删除原任务
            task.delete()

            return JsonResponse({'success': True})
        except AssignedTasks.DoesNotExist:
            return JsonResponse({'success': False, 'error': '任务不存在'}, status=404)

def historical_list(request):
    tasks = HistoricalTasks.objects.all()
    form=HistoricalTasks()
    return render(request,'Historical_list.html',{'tasks':tasks,'form':form})


