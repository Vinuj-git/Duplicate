import csv
from django.shortcuts import render,redirect
import io
# Create your views here.
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
import pandas as pd
import numpy as np
# def listing(request):
#     contact_list = User.objects.all()
#     paginator = Paginator(contact_list, 5) # Show 25 contacts per page.

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'list.html', {'page_obj': page_obj})


# def index(request):
#     posts = User.objects.all()  # fetching all post objects from database
#     print("***************",posts)
#     p = Paginator(posts, 2)  # creating a paginator object
#     # getting the desired page number from url
#     page_number = request.GET.get('page')
#     try:
#         page_obj = p.get_page(page_number)  # returns the desired page object
#     except PageNotAnInteger:
#         # if page_number is not an integer then assign the first page
#         page_obj = p.page(1)
#     except EmptyPage:
#         # if page is empty then return last page
#         page_obj = p.page(p.num_pages)
#     context = {'page_obj': page_obj}
#     # sending the page object to index.html
#     return render(request, 'list.html', context)

def index(request):

    arrayRows=[]
    with open('dups.csv','r') as f:
        fileObj=csv.reader(f,delimiter=',')
        linCount=0
        for row in fileObj:
            if linCount==0:
                headerInfo=row
                linCount +=1
            else:
                arrayRows.append(row)
    
    if request.GET.get('pageNo') == None:
        pageNO=1
    else:
        pageNO=request.GET.get('pageNo')
    if request.GET.get('noOfElements') == None:
        noOfElements=10
    else:
        noOfElements=request.GET.get('noOfElements')
        pagC=Paginator(arrayRows,noOfElements)
        pacgObj=pagC.page(pageNO)
        data=pacgObj.object_list
        context={'data':data,'headerInfo':headerInfo,'noOfPages':list(pagC.page_range)}
        return render(request,'pagination.html',context)

def duplicate(request):
    template = "pagination.html"
    data = {}
    print("---------daata-----------",data)
    if "GET" == request.method:
        return render(request, template, data)
    # if not GET, then proceed

    csv_file = request.FILES["csv_file_student"]
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'File is not CSV type')
        return redirect(request,template)

    data_set = csv_file.read().decode('UTF-8')    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    #loop over the lines and save them in db. If error , store as string and then display
    for fields in csv.reader(io_string, delimiter=',', quotechar="|"):
        data_dict = {}
        data_dict["username"] = fields[0]
        data_dict["first_name"] = fields[1]
        data_dict["last_name"] = fields[2]
        data_dict["email"] = fields[3]
        # data_dict["studentClass"] = fields[4]
        # data_dict["exam"] = fields[5]
        #data_dict["subject7"] = fields[24]
        #data_dict["subject7Marks"] = fields[25]
        #data_dict["subject7Result"] = fields[26]
        #print(data_dict["studentClass"])
        #print(data_dict)
        UserInfo = User.objects.update_or_create(UserClass__icontains=data_dict["username"], registerNo__icontains=data_dict["email"]).update_or_create(
                registerNo=data_dict["username"],
                studentName=data_dict["first_name"],
                result=data_dict["last_name"],
                studentClass=data_dict["email"],
                totalMarks=data_dict["totalMarks"],
                exam=data_dict["exam"],
                subject1=data_dict["subject1"],
                #subject7=data_dict["subject7"],
                #subject7Marks=data_dict["subject7Marks"],
                #subject7Result=data_dict["subject7Result"]
                )



    #return render(request, "listuploads.html", context)