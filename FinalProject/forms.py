from django import forms
from .models import UnassignedTasks, AssignedTasks


class PriorityForm(forms.Form):
    OPERATION_CHOICES = [
        ('Grinding','grinding'),
        ('Milling','grinding'),
        ('Lathe','lathe'),
        ('Drilling','drilling'),
        ('Additive','additive'),
    ]

    MACHINE_CHOICES = [
        ('M01','M001'),
        ('M02','M002'),
        ('M03','M003'),
        ('M04','M004'),
        ('M05','M005'),
    ]

    Operation_Type = forms.ChoiceField(choices=OPERATION_CHOICES,label='Operation Type')
    Material_Used = forms.FloatField(label='Material Used')
    Processing_Time = forms.FloatField(label='Processing Time(Mins)')
    Energy_Consumption = forms.FloatField(label='Energy Consumption')
    Machine_Availability = forms.FloatField(label='Machine Availability(%)')
    Machine_ID = forms.ChoiceField(choices=MACHINE_CHOICES,label='Machine ID')

    Scheduled_Start = forms.DateTimeField(
        label='Scheduled Start',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    Deadline = forms.DateTimeField(
        label='Deadline',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

class UnassignedTasksForm(forms.ModelForm):
    class Meta:
        model = UnassignedTasks
        fields='__all__'

class AssignedTasksForm(forms.ModelForm):
    class Meta:
        model = AssignedTasks
        fields='__all__'