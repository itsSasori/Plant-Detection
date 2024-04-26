from django.urls import path

from . import views

urlpatterns = [
    path('',views.home_page,name="home_page"),
    path('contact/',views.contact,name="contact"),
    path('index/',views.ai_engine_page,name="index"),    
    path('submit/',views.submit,name="submit"),    
    path('mobile-device/',views.mobile_device_detected_page,name="mobile-device"),    
    path('market/',views.market,name="market"),    

  
]