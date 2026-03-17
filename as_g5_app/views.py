from django.shortcuts import render
from as_g5_app.forms import userForm,userForm2,updateForm,updateForm2
from as_g5_app.models import userData
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from defectsapp.models import developer,defects_mod


# Create your views here.
def registration(request):
    registered=False
    if request.method=='POST':
        form=userForm(request.POST)
        form1=userForm2(request.POST,request.FILES)
        if form.is_valid() and form1.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            
            profile=form1.save(commit=False)
            profile.user=user #both models merged together
            profile.save()
            registered=True
            
    else:
        form=userForm()
        form1=userForm2() 
    context={
           'form':form,
           'form1':form1,
           'registered':registered
           
    }
    return render(request,'account/registration.html',context)


def display(request):
    dis_1=userData.objects.all()

    return render(request,'account/display.html',{'dis_1':dis_1})

def user_login(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        
        user=authenticate(username=username,password=password)
        
        if user:
            if user.is_active:
                login(request,user)
                return redirect('home')
            else:
                return HttpResponse("User is Not Active")
        else:
            return HttpResponse("Pls Check Your Credentials")
        
        
    return render(request,'account/login.html',{})

@login_required(login_url='login')
def home(request):
    return render(request,'account/home.html',{})

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
        # user = request.user
        # is_developer = developer.objects.filter(dev_name=user).exists()
        # return render(request,'account/profile.html',{'is_developer': is_developer,'user': user})
        
    

    user = request.user
    dev_obj = developer.objects.filter(dev_name=user).first()
    # Default values
    total_assigned = pending_count = completed_count = 0
    if dev_obj:
        # Total defects assigned to this developer
        total_assigned = defects_mod.objects.filter(Assigned_To=user).count()

        # Pending defects (you can adjust the status value as per your data)
        pending_count = defects_mod.objects.filter(Assigned_To=user,Defect_Status__iexact='Pending').count()

        # Completed defects
        completed_count = defects_mod.objects.filter(Assigned_To=user,Defect_Status__iexact='Completed').count()

    return render(request, 'account/profile.html', {'is_developer': bool(dev_obj),'developer_info': dev_obj,
        'total_assigned': total_assigned,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'user': user
    })


@login_required(login_url='login')
def update(request):
    if request.method == 'POST':
        form = updateForm(request.POST, instance=request.user)
        form1 = updateForm2(request.POST,request.FILES,instance=request.user.userdata)

        if form.is_valid() and form1.is_valid():
            user= form.save()
            user.save()
            profile = form1.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('profile')
    else:
        form = updateForm(instance=request.user)
        form1 = updateForm2(instance=request.user.userdata)


    return render(request,'account/update.html',{'form': form,'form1': form1})



