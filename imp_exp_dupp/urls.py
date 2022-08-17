from django.urls import path,include
from imp_exp_dupp import views

urlpatterns = [ 
    path('page/',views.index,name='index'),
    path('duplicate/',views.duplicate,name='duplicate')
]