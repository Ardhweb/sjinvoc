from django.urls import path
from . import views
app_name="toolszest"
urlpatterns=[
path('imager-resizer',views.image_resizer_stage, name='image_resizer'),
]