import joblib
import pandas as pd
from django.contrib.auth import authenticate, logout
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
from django.contrib.auth.decorators import login_required

ML_MODEL_PATH='FinalProject/ml_models/priority_model.pkl'    # path to locate the model
model=joblib.load(ML_MODEL_PATH)            #Load the model using joblib


# Create your views here.
def index(request):
    return render(request,'index.html')


# View function to handle priority prediction requests.
# If the request method is POST, it processes the submitted form data,
# validates it, converts it to a DataFrame, and passes it to the prediction function.
# The prediction result is then rendered to the template.

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def predict_view(request):
    result = None

    if request.method == 'POST':
        form = PriorityForm(request.POST)

        if form.is_valid():
            # Extract and clean the input data from the form
            print(1)
            input_data = form.cleaned_data
            input_data=pd.DataFrame([input_data])
            # Call the predict_priority function to get prediction results
            result = predict_priority(input_data)

    else:
        form = PriorityForm() # Initialize an empty form for GET requests

    print("POST DATA：", request.POST)
    print("fORMS ERROR", form.errors)
    # Render the prediction result along with the form
    return render(request, 'predict.html', {
        'form': form,
        'result': result

    })


# def get_credential(request):
#     answer = Credential.objects.all().values('username')
#     print(answer)
#     return HttpResponse(answer)


@login_required
def unassigned_list(request):
    tasks = UnassignedTasks.objects.all()
    form=UnassignedTasks()
    return render(request,'Unassigned_list.html',{'tasks':tasks,'form':form})


@login_required
def add_unassigned_task(request):
    if request.method == 'POST':
        UnassignedTasks.objects.create(
            operation_type=request.POST.get('operation_type'),
            material_used=request.POST.get('material_used'),
            processing_time=request.POST.get('processing_time'),
            energy_consumption=request.POST.get('energy_consumption'),
            machine_availability=request.POST.get('machine_availability'),
            machine_id=request.POST.get('machine_id'),
        )
    return redirect('unassigned_list')



@login_required
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


@login_required
def assigned_list(request):
    if request.GET.get('sort') == 'priority':
        tasks = AssignedTasks.objects.all().order_by('-priority_score')  # order by priority score
        sorted_flag = True
    else:
        tasks = AssignedTasks.objects.all().order_by('id')  # default order
        sorted_flag = False

    return render(request, 'Assigned_list.html', {
        'tasks': tasks,
        'sorted': sorted_flag
    })


@login_required
@csrf_exempt
def assigned_view(request, task_id):
    if request.method == 'POST':
        try:
            task = AssignedTasks.objects.get(id=task_id)

            # clone the row in Historical table
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

            # Delete the original form when pushing finished
            task.delete()

            return JsonResponse({'success': True})
        except AssignedTasks.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tasks not exist'}, status=404)


@login_required
def historical_list(request):
    tasks = HistoricalTasks.objects.all()
    form=HistoricalTasks()
    return render(request,'Historical_list.html',{'tasks':tasks,'form':form})


@login_required
def delete_unassigned_task(request, task_id):
    task = get_object_or_404(UnassignedTasks, id=task_id)
    task.delete()
    return redirect('unassigned_list')


@login_required
def update_unassigned_task(request, task_id):
    task = get_object_or_404(UnassignedTasks, id=task_id)
    if request.method == 'POST':
        task.operation_type = request.POST.get('operation_type')
        task.material_used = request.POST.get('material_used')
        task.processing_time = request.POST.get('processing_time')
        task.energy_consumption = request.POST.get('energy_consumption')
        task.machine_availability = request.POST.get('machine_availability')
        task.machine_id = request.POST.get('machine_id')
        task.save()
        return redirect('unassigned_list')
    return render(request, 'update_task.html', {'task': task})
