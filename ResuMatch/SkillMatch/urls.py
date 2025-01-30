
from django.urls import path
from . import views

urlpatterns = [
    path("upload/" , views.upload_resume , name="upload_resume"),
    path("analyze/" , views.analyze_now , name="analyze_now"),
    path("results/" , views.analysis_results , name= "results")
    
    

    
]
