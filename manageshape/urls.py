from django.urls import path
from manageshape import views

app_name = "manageshape"
urlpatterns = [
    path('', views.shapes, name="shapes"), # list shapes
    path('create', views.update_or_create_shape, name="create_shape"), # create shape
    path('<int:id>', views.shape, name="shape") # read and delete shape
]