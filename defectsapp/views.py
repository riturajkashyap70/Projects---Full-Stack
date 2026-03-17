from django.shortcuts import render,redirect,get_object_or_404
from defectsapp.models import defects_mod, tester,defect_screenshot,developer
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from defectsapp.forms import defect_edit_form,add_defect_form,filter_data
from as_g5_app.forms import forgetPasswordForm
from django.contrib import messages
from django.contrib.auth.models import User
from defectsapp.utils import send_email_view



@login_required(login_url='login')
def all_defects(request):
    data = defects_mod.objects.all()
    d=len(data)

    is_admin = tester.objects.filter(tester_name=request.user, is_admin=True).exists()
    paginator=Paginator(data,3)
    page_num=request.GET.get('pg')
    data=paginator.get_page(page_num)
    context={'data': data,'is_admin': is_admin,'d':d}
    
    
    #?#logged in user details (alternate of :  is_admin = tester.objects.filter(tester_name=request.user, is_admin=True).exists() )
    # user= request.user
    # show_button=False

    # try:
    #    test=tester.objects.get(tester_name=user)
    #    if test.is_admin:
    #        show_button=True
    # except:
    #     pass
    # context={
    #     'value':value,
    #     'defect_counts':defect_counts,
    #     'show_button':show_button, 
    # }



    return render(request, 'defects/alldefects.html',context )

    
@login_required(login_url='login')    
def description(request,id=0):
    defects=defects_mod.objects.get(id=id)
    defects_img = defects.defect_screenshot_set.all()
    # defects_img = defect_screenshot.objects.filter(defect=defects)
    
    context = {
        'defects': defects,
        'defects_img': defects_img
    }
    return render(request, 'defects/description.html',context)

@login_required(login_url='login')
def edit(request,id=0):
    defect=defects_mod.objects.get(id=id)
   
    if request.method =='POST':
        form=defect_edit_form(request.POST,instance=defect)
        if form.is_valid():
            form.save()
            return redirect('all_defects')
    else:
        form=defect_edit_form(instance=defect)
    return render(request,'defects/edit.html',{'form':form})



def delete_defect(request, id):
    defect = get_object_or_404(defects_mod, id=id)
    defect.delete()
    messages.success(request, "Defect deleted successfully.")
    return redirect('all_defects')  # This should be your defects listing page



@login_required(login_url='login')
def add_defect(request):
    if request.method == 'POST':
        form=add_defect_form(request.POST)
        if form.is_valid():
            devname=form.cleaned_data['Assigned_To'] 
            user=User.objects.get(username=devname)
            defect_instance = form.save()
            # form.save()
            send_email_view(user.email,defect_instance)  # Send email notification
            return redirect('all_defects')
    else:
        form=add_defect_form()
    return render(request, 'defects/add_defect.html', {'form': form})


def forget_password(request):
    if request.method == 'POST':
        form = forgetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()

            messages.success(request, "Your password has been reset successfully.")
               
    else:
        form = forgetPasswordForm()

    return render(request, 'account/forgetpassword.html', {'form': form})


@login_required(login_url='login')
def dev_filter(request):
    dev_defects = None
    if request.method == 'POST':
        form = filter_data(request.POST)
        if form.is_valid():
            user = form.cleaned_data['Assigned_To']  # This is already a User object
            dev_defects = defects_mod.objects.filter(Assigned_To=user)
    else:
        form = filter_data()
    
    return render(request, 'defects/dev_filter.html', {
        'form': form,
        'dev_defects': dev_defects
    })

@login_required(login_url='login')
def completed_defects(request):
    completed = defects_mod.objects.filter(Defect_Status='Completed')
    COUNT = completed.count()
    return render(request, 'defects/completed_defects.html', {'data': completed, 'COUNT': COUNT})


@login_required(login_url='login')
def pending_defects(request):
    defects = defects_mod.objects.filter(Defect_Status="Pending")  
    COUNT = defects.count()
    return render(request, 'defects/pending_defects.html', {'defects': defects,'COUNT': COUNT})




