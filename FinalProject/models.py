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
        managed = False
        db_table = 'assigned_tasks'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
        managed = False
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
        managed = False
        db_table = 'unassigned_tasks'
