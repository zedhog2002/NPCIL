from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import Registerform,Addrecordform
from .models import Package
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import FileResponse
import io
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views  here.
def home(request):
    packages = Package.objects.all()

    if request.method == 'POST':
        Email_input = request.POST.get('Email')
        Password_input = request.POST.get('Password')
        user = authenticate(request, username = Email_input , password = Password_input )
        if user is not None:
            login(request, user)
            messages.success(request,"You are now logged in ",extra_tags='alert-success')
            return redirect('home')
        else:
            messages.error(request,'There was an error',extra_tags='alert-danger')
            return redirect('home')
    else:
        return render(request, 'home.html',{'packages':packages})


def logout_user(request):
    logout(request)
    messages.success(request,'You have been logged out',extra_tags='alert-success')
    return redirect('home')
#
def register_user(request):
    if request.method == 'POST':
        form = Registerform(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Registerform()
        return render(request,'register.html', {'form':form})

def package_record(request, pk):
    if request.user.is_authenticated:
        node_info = Package.objects.get(package_id=pk)
        return render(request,'package_info.html',{'node_info':node_info})
    else:
        messages.error(request,'You need to login to see the info',extra_tags='alert-error')
        return redirect('home')

def delete_package_record(request, pk):
    if request.user.is_authenticated:
        Package.objects.get(package_id=pk).delete()
        messages.success(request, "Package deleted successfully",extra_tags='alert-success')
        return redirect('home')
    else:
        messages.error(request,'You need to login to delete info',extra_tags='alert-error')
        return redirect('home')

def add_package_record(request):
    form = Addrecordform(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                new_package = Package(
                    package_id=form.cleaned_data['package_id'],
                    name=form.cleaned_data['name'],
                    version=form.cleaned_data['version'],
                    node_id=form.cleaned_data['node_id']
                )
                new_package.save()
                messages.success(request,"Package added",extra_tags='alert-success')
                return redirect('home')
        return render(request, 'add_package_record.html',{'form':form})
    else:
        messages.error(request, 'You need to be logged in to add', extra_tags='alert-error')
        return redirect('home')

def update_package_record(request, pk):
    if request.user.is_authenticated:
        node_info = Package.objects.get(package_id=pk)
        form = Addrecordform(request.POST or None,instance=node_info )
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated successfully",extra_tags='alert-success')
            return redirect('home')
        return render(request, 'update_package_record.html', {'form': form } )

    else:
        messages.error(request,'You need to login to see the info',extra_tags='alert-error')
        return redirect('home')

def show_package_record(request):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)

    # Container for the 'Flowable' elements
    elements = []
    page_width, page_length = letter
    table_width = 0.8 * page_width  # 80% of the page width

    # Get the packages
    packages = Package.objects.all()

    # Define the table data and style
    data = [['Package ID', 'Package Name', 'Version', 'Node ID']]
    for package in packages:
        data.append([package.package_id, package.name, package.version, package.node_id])

    # Define the table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Row background color
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid lines
        ('WIDTH', (0, 0), (-1, -1), table_width),  # Set table width to 80% of page width
    ])

    # Create the table and apply the style
    table = Table(data)
    table.setStyle(style)

    # Add the table to the elements list
    elements.append(table)

    # Build the PDF document
    doc.build(elements)

    # Reset buffer position and return the PDF response
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='report.pdf')
