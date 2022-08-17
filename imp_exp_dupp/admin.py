from django.contrib import admin
from django.contrib.auth.models import User

from .models import Student
from import_export import resources
from django.db.models import Count
from import_export.admin import ImportExportModelAdmin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
import pandas as pd
import numpy as np


import csv

# Register your models here.

class UserResource(resources.ModelResource):

    class Meta:
        model = User
        fields = ('id', 'username', 'email','first_name','last_name')
        import_id_fields = ('id','username','first_name', 'last_name', 'email')
        skip_unchanged = False
        def clean_asset_code(self):
            asset_code = self.cleaned_data['asset_code']
            if User.objects.filter(asset_code=asset_code).exists():
                raise ValidationError("This asset code already exist.")
            return asset_code
        

class UserAdmin(ImportExportModelAdmin):
    list_display = ('id','username','first_name', 'last_name', 'email')
    resource_class = UserResource
    save_as = True
    # df = pd.read_csv("/home/abhijit/Downloads/User-2022-08-05.csv")

    # pd.save_duplicates(inplace=True)
             
    # x = pd.save_duplicates(subset=['username', 'first_name', 'last_name','email'], inplace=True)
    # print("---------------",x)
    # pd.to_csv("/home/abhijit/Downloads/User-2022-08-05.csv", index=False)

   # pd.to_csv("User-2022-08-05.csv", index=False)   
    df = pd.read_csv('/home/abhijit/Downloads/User-2022-08-05.csv')
    df['message'] = np.where(df['username'].duplicated(), 'Duplicate', 'Already Exist')
    print("===================",df['message'])
    #np.savetxt("clear-m.csv", delimiter=",")
    df[df.duplicated()].to_csv('dups.csv')
    #df['message'] = np.where(df['fitst_name'].duplicated(), 'Duplicated', 'Already Exist')
    p = Paginator(list_display, 5)
    print("----------------",df)
    pass

class StudentResource(resources.ModelResource):

    class Meta:
        model = Student
        fields = ('id','username', 'email','first_name','last_name')
        import_id_fields = ('id','username','first_name', 'last_name', 'email')
        report_skipped = True
        #export_id_fields = ('username','first_name', 'last_name', 'email')
        skip_unchanged = False
        def clean_asset_code(self):
            asset_code = self.cleaned_data['asset_code']
            if Student.objects.filter(asset_code=asset_code).exists():
                raise ValidationError("This asset code already exist.")
            return asset_code
        

class StudentAdmin(ImportExportModelAdmin):
    list_display = ('id','username','first_name', 'last_name', 'email')
    resource_class = StudentResource
    save_as = True

@admin.register(Student) 
class TestappImportExport(ImportExportModelAdmin): 
    resource_class = StudentResource



admin.site.unregister(User)
admin.site.register(User,UserAdmin)
#admin.site.register(Student,StudentAdmin)


#duplicates = User.objects.values(
    # 'first_name'
    # ).annotate(name_count=Count('first_name')).filter(name_count__gt=1)
    # print(duplicates,"--------------")
    # records = User.objects.filter(first_name=[item['first_name'] for item in duplicates])
    # print(records)
    # print([item.id for item in records])
    # [2, 11, 13]