from django.shortcuts import render, redirect
from .froms import JobApplicationForm
from .models import Category, JobApplication
from .models import SubCategory
from .models import Work


def index(request, contex=None):
    ctg = Category.objects.all()
    contex = {
        'ctg': ctg
    }
    return render(request,'main/index.html',contex)


def about(request):
    ctx = {
    }
    return render(request,'main/about.html', ctx)

def work(request, id):
    wctg = Work.objects.filter(id=id).all()
    ctx = {
        'wctg' : wctg
    }

    return render(request,'main/work.html',ctx)

#  Api chiqarish ushun
def workapi(request, id):
    wctg = Work.objects.filter(id=id).all()
    ctx = {
        'wctg' : wctg
    }
    wctg = list(wctg.values())
    from django.http import JsonResponse
    return JsonResponse({"data": wctg})

def works(request, id):
    sctg = SubCategory.objects.filter(id=id).all()
    ctx = {
        'sctg' : sctg
            }

    return render(request,'main/works.html',ctx)

def contact(request):
    ctx = {}
    return render(request,'main/contact.html',ctx)

def success(request):
    ctx = {}
    return render(request,'main/success.html',ctx)
    ctx = {

    }
def registor_file(request):
    ctx = {
    }
    return render(request, 'main/registor_file.html', ctx)

def login(request):
    ctx = {}
    return render(request, 'main/login.html', ctx)

def admin_page(request):
    rctg = JobApplicationForm.objects.all()
    ctx = {
        'rctg': rctg
    }
    return render(request, 'main/admin_page.html', ctx)

def user_page(request):
    ctx = {}
    return render(request, 'main/user_page.html', ctx)

def password_save(request):
    ctx = {}
    return render(request, 'main/password_save.html', ctx)

def message_user(request):
    ctx = {}
    return render(request, 'main/masseg_user.html', ctx)

def registor(request):
    ctx = {}
    return render(request, 'main/registor.html', ctx)

from .froms import loginForm
def register(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = loginForm()

    return render(request, 'main/registor.html', {'form': form})




def catigory_page(request):
    ctg = Category.objects.all()
    ctx = {
        'ctg': ctg
    }
    return render(request, 'main/catigory.html', ctx)


