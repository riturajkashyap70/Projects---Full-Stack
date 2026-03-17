from django.urls import path
from defectsapp import views

urlpatterns = [
    path("",views.all_defects,name="all_defects"),
    path("<int:id>",views.description,name="description"),
    path('edit/<int:id>',views.edit,name="edit"),
    path('add_defect/', views.add_defect, name='add_defect'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('dev_filter/', views.dev_filter, name='dev_filter'),
    path('delete_defect/<int:id>', views.delete_defect, name='delete_defect'),
    path('completed_defects/', views.completed_defects, name='completed_defects'),
    path('pending_defects/', views.pending_defects, name='pending_defects'),



    
    
   

    

]
