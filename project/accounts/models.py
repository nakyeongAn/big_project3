# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.conf import settings
import datetime
from phonenumber_field.modelfields import PhoneNumberField
#test modeling
class Item(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
#회원가입 모델 정의
class AccountUserManager(BaseUserManager):
    use_in_migrations = True


    def create_user(self, member_id, organization, password=None):

        user = self.model(member_id=member_id, organization=organization)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, member_id, organization, password=None):
        user = self.create_user(
            member_id=member_id,
            organization=organization,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


#회원가입 모델 BaseUser 상속
class AccountUser(AbstractBaseUser, PermissionsMixin):
#이름
#아이디 
#비번
#비번확인
#메일   
#성별?  
#나이?  생일에서 현재 년도 빼버림 
#생일   
#전화번호   
#주소검색 내꺼 도로명 1
    GENDER_CHOICHES = {
        ('남자' , '남자'),
        ('여자','여자')
    }
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=255)
    organization = models.CharField(max_length=30)
    member_id = models.CharField(unique=True, max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=20)
    gender = models.CharField(max_length=3, choices = GENDER_CHOICHES, default = '남자')
    birthdate = models.DateField(default= datetime.date.today)
    phone_number = PhoneNumberField(default = '0',region='KR') # unique=True 추가해라 나중에 
    agearound = models.IntegerField(default = 1)
    address = models.CharField(default = 'None', max_length = 100)
    objects = AccountUserManager()

    groups = models.ManyToManyField(
        Group,
        related_name="accountuser_groups",
    )
    
    user_permissions=models.ManyToManyField(
        Permission,
        related_name="accountuser_permissions",
    )
    
    USERNAME_FIELD = 'member_id'
    
    #superuser 용
    REQUIRED_FIELDS = ['organization']

    class Meta:
        db_table = 'account_user'

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


# # 친구 목록 모델
# class FriendRequest(models.Model):
#     use_in_migrations = True
#     STATUS_CHOICES = [
#         ('requested', 'Requested'),
#         ('accepted', 'Accepted'),
#         ('declined', 'Declined'),
#     ]

#     requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_requests_sent')
#     receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_requests_received')
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='requested')
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('requester', 'receiver')
#         db_table = 'friendrequest'
    

# 기타 기본 django db 데이터
class AccountUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AccountUser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_user_groups'
        unique_together = (('user', 'group'),)


class AccountUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AccountUser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_user_user_permissions'
        unique_together = (('user', 'permission'),)


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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountUser, models.DO_NOTHING)

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


