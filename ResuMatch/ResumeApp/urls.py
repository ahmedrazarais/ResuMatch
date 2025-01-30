
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_resume, name='create_resume'),
    path('work_experience/', views.create_work_experience, name='create_work_experience'),
    path('education/', views.create_education, name='create_education'),
    path("convert/" , views.convert_to_pdf , name="convert_to_pdf"),
    path("download/" ,views.download_resume , name="download_resume")
    

    
]
