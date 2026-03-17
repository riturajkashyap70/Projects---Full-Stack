from django import forms
from defectsapp.models import defects_mod,tester,developer
from django.contrib.auth.models import User

class defect_edit_form(forms.ModelForm):
    Defect_Id=forms.CharField(max_length=30,disabled=True)
    Defect_Name=forms.CharField(max_length=30,disabled=True)
    class Meta:
        model=defects_mod
        fields=["Defect_Name","Defect_Id","Assigned_By","Assigned_To","Description","Defect_Status","Priority"]
        
class add_defect_form(forms.ModelForm):
     class Meta:
        model=defects_mod
        fields = "__all__"
        
        
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Assigned_By → testers only
        tester_users = tester.objects.values_list('tester_name', flat=True)
        self.fields['Assigned_By'].queryset = User.objects.filter(id__in=tester_users)

        # Assigned_To → developers only
        developer_users = developer.objects.values_list('dev_name', flat=True)
        self.fields['Assigned_To'].queryset = User.objects.filter(id__in=developer_users)
        
class filter_data(forms.ModelForm):
    class Meta:
        model = defects_mod
        fields = ['Assigned_To']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show developers
        developer_users = developer.objects.values_list('dev_name', flat=True)
        self.fields['Assigned_To'].queryset = User.objects.filter(id__in=developer_users)

        
        
        

       
