from django.db import models


class AssignedTasks(models.Model):
    operation_type = models.CharField(max_length=50)
    material_used = models.FloatField(db_column='Material_Used', blank=True, null=True)  # Field name made lowercase.
    processing_time = models.FloatField(db_column='Processing_Time', blank=True, null=True)  # Field name made lowercase.
    energy_consumption = models.FloatField(db_column='Energy_Consumption', blank=True, null=True)  # Field name made lowercase.
    machine_availability = models.FloatField(db_column='Machine_Availability', blank=True, null=True)  # Field name made lowercase.
    machine_id = models.CharField(db_column='Machine_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    time_budget = models.FloatField(db_column='Time_Budget', blank=True, null=True)  # Field name made lowercase.
    time_risk = models.FloatField(db_column='Time_Risk', blank=True, null=True)  # Field name made lowercase.
    exceeds_deadline = models.IntegerField(db_column='Exceeds_Deadline', blank=True, null=True)  # Field name made lowercase.
    priority_label = models.CharField(db_column='Priority_Label', max_length=20, blank=True, null=True)  # Field name made lowercase.
    scheduled_start = models.DateTimeField(db_column='Scheduled_Start', blank=True, null=True)  # Field name made lowercase.
    deadline = models.DateTimeField(db_column='Deadline', blank=True, null=True)  # Field name made lowercase.
    priority_score = models.FloatField(db_column='Priority_Score')  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'assigned_tasks'





class HistoricalTasks(models.Model):
    material_used = models.FloatField(blank=True, null=True)
    processing_time = models.FloatField(blank=True, null=True)
    energy_consumption = models.FloatField(blank=True, null=True)
    machine_availability = models.FloatField(blank=True, null=True)
    machine_id = models.CharField(max_length=50, blank=True, null=True)
    time_budget = models.FloatField(blank=True, null=True)
    time_risk = models.FloatField(blank=True, null=True)
    exceeds_deadline = models.IntegerField(blank=True, null=True)
    priority_label = models.CharField(max_length=20, blank=True, null=True)
    scheduled_start = models.DateTimeField(db_column='Scheduled_Start', blank=True, null=True)  # Field name made lowercase.
    deadline = models.DateTimeField(db_column='Deadline', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'historical_tasks'


class UnassignedTasks(models.Model):
    operation_type = models.CharField(max_length=50)
    material_used = models.FloatField(blank=True, null=True)
    processing_time = models.FloatField(blank=True, null=True)
    energy_consumption = models.FloatField(blank=True, null=True)
    machine_availability = models.FloatField(blank=True, null=True)
    machine_id = models.CharField(max_length=50, blank=True, null=True)
    scheduled_start = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed=True
        db_table = 'unassigned_tasks'
