from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import MemberForm, CreateUserForm, StatusForm
from .filters import MemberFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from .resources import MemberResource, MemberFeeResource
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Count
import json
from datetime import datetime
from django.db.models import Sum, Max
from tablib import Dataset
from django.utils import timezone
from collections import Counter


def opt(request):
    return render(request, 'member/opt.html')

@login_required(login_url='login')
@admin_only
def home(request):

    membersChart = Member.objects.filter(status__in=['Member', 'New Member'])
    members = Member.objects.all()
    memberfee = MemberFee.objects.all()
    
    totalMember = members.count() 
    jumlahAhli = members.filter(status='Member').count()
    totalPending = members.filter(status='Waiting for Approval').count()
    totalTerminate = members.filter(status='Not a Member').distinct().count()
    totalNewMember = members.filter(status='New Member').count()
    totalAhli =  jumlahAhli + totalNewMember

    now = timezone.now()

    #currTerminate = members.filter(status="Not a Member", fees__date__year=now.year, fees__date__month=now.month).distinct().count()
    currTerminate = members.filter(status="Not a Member", fees__date__month=8).count()


    
    
    #Bar Chart
    # Get the current year
    current_year = datetime.now().year

    # Aggregate the total fee amount for each month of the current year
    monthly_fees = MemberFee.objects.filter(date__year=current_year).values('date__month').annotate(total=Sum('amount')).order_by('date__month')

    # Prepare data for the bar chart
    labelsY = [datetime(current_year, month['date__month'], 1).strftime('%B') for month in monthly_fees]
    dataY = [float(month['total']) if month['total'] is not None else 0 for month in monthly_fees]

    # Filter out None values and count occurrences
    fakulti_data = Counter(member.fakulti for member in membersChart if member.fakulti)
    cawangan_data = Counter(member.cawangan for member in membersChart if member.cawangan)
    jantina_data = Counter(member.jantina for member in membersChart if member.jantina)
    bangsa_data = Counter(member.bangsa for member in membersChart if member.bangsa)
    status_data = Counter(member.status for member in members if member.status)

    #Member fee table
    # Get all member fees
    fees = MemberFee.objects.all()

    # Initialize a dictionary to store the aggregated data
    data = {}

    # Iterate over each fee and aggregate the amounts by month for each member
    for fee in fees:
        if fee.noPekerja not in data:
            data[fee.noPekerja] = {
                'nama': fee.nama,
                'January': 0,
                'February': 0,
                'March': 0,
                'April': 0,
                'May': 0,
                'June': 0,
                'July': 0,
                'August': 0,
                'September': 0,
                'October': 0,
                'November': 0,
                'December': 0,
            }
        
        # Determine the month from the date field
        month_name = calendar.month_name[fee.date.month]
        data[fee.noPekerja][month_name] += int(fee.amount)

    # Convert the data dictionary to a list of dictionaries for easier template rendering
    data_list = [{'noPekerja': k, **v} for k, v in data.items()]

    context = {'members':members,
               'data': data_list,
               'totalMember':totalMember,
               'totalAhli':totalAhli,
               'totalPending':totalPending, 
               'totalTerminate':totalTerminate,
               'currTerminate': currTerminate,
               'labelsY': json.dumps(labelsY),
                'dataY': json.dumps(dataY),
                'totalNewMember':totalNewMember,
                'fakulti_labels': list(fakulti_data.keys()),
                'fakulti_values': list(fakulti_data.values()),
                'cawangan_labels': list(cawangan_data.keys()),
                'cawangan_values': list(cawangan_data.values()),
                'jantina_labels': list(jantina_data.keys()),
                'jantina_values': list(jantina_data.values()),
                'bangsa_labels': list(bangsa_data.keys()),
                'bangsa_values': list(bangsa_data.values()),
                'status_labels': list(status_data.keys()),
                'status_values': list(status_data.values()),
               }

    return render(request, 'member/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listAhli(request):

    members = Member.objects.all()
    user = User.objects.all()

    listAhli = members.filter(status='Member').all()


    context = {'listAhli':listAhli, 'user':user, 'members':members}

    return render(request, 'member/listAhli.html', context, )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listPending(request):

    members = Member.objects.all()
    
    listPending = members.filter(status='Waiting for Approval').all()

    

    context = {'listPending':listPending, }

    return render(request, 'member/listPending.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listNewMember(request):

    members = Member.objects.all()
    listNewMember = members.filter(status='New Member').all()


    context = {'members':members, 'listNewMember':listNewMember}
    return render(request, 'member/listNewMember.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listTerminate(request):

    members = Member.objects.all()
    
    listTerminate = members.filter(status='Not a Member').all()

    context = {'listTerminate':listTerminate}

    return render(request, 'member/listTerminate.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def registration(request):
    form = MemberForm()
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return redirect('listMember')


    

    context = {'form':form}
    return render(request, 'member/registration.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listMember(request):

    members = Member.objects.all()



    context = {'members':members}
    return render(request, 'member/listMember.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateMember(request, pk):
    member = Member.objects.get(id=pk)

    form = StatusForm(instance = member)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return redirect('listPending')

    context = {'form':form}
    
    return render(request, 'member/updateStatus.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def member(request, pk):
    member = Member.objects.get(id=pk)
    fees = member.fees.all()

    context = {'member':member,'fees':fees}

    return render(request, 'member/member.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def memberEdit(request, pk):
    member = Member.objects.get(id=pk)

    form = MemberForm(instance=member)

    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member')

    context = {'form':form, 'member':member}
    return render(request, 'member/memberEdit.html', context)


def register(request):

    registerForm = MemberForm()
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        registerForm = MemberForm(request.POST)
        if form.is_valid() and registerForm.is_valid():
            
            user = form.save(commit=False)
            user.user = request.user
            form.instance = user
            
            user.save()

            group = Group.objects.get(name='member')
            user.groups.add(group)
            

            
            member = registerForm.save(commit=False)
            member.user = user
            member.save()
            
            
            messages.success(request, "Account was create for " + user.username)
            return redirect('login')
        


    context = {'form':form, 'registerForm':registerForm}
    return render(request, 'member/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name="member").exists():
                return redirect('user-page')
            if user.groups.filter(name="admin").exists():
                return redirect('dashboard')
        else:
            messages.info(request, "Username OR Password is incorrect")
            return render(request, 'member/login.html',)

            
    context= {}
    return render(request, 'member/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteMember(request, pk):
    member = Member.objects.get(id=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('/')

    context = {'member':member}
    return render(request, 'member/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['member'])
def userPage(request):
    member = Member.objects.get(user=request.user)
    form = MemberForm(instance=member)


    context = {'member':member, 'form':form}
    return render(request, 'member/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['member'])
def accountSetting(request):
    member = request.user.member
    form = MemberForm(instance=member)

    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'member/accountSetting.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['member'])
def userEdit(request):
    member = request.user.member
    form = MemberForm(instance=member)

    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('user-page')

    context = {'form':form}
    return render(request, 'member/userEdit.html', context)

def errorPage(request):
    context = {}
    return render(request, 'member/error.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_member_status(request):
    members = Member.objects.all()
    for member in members:
        # Get the latest MemberFee for the member
        latest_fee = member.fees.order_by('date').first()
        
        if latest_fee is None:
            member.status = 'Not a Member'
        else:
            total_amount = member.fees.filter(date=latest_fee.date).aggregate(total=Sum('amount'))['total']
            
            if total_amount in [5, 6]:
                member.status = 'Member'
            elif total_amount == 16:
                member.status = 'New Member'
            else:
                member.status = 'Anomaly'
        
        member.save()
    
    return HttpResponse("Member statuses updated successfully.")

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def export_members(request):
    status = request.GET.get('status')
    if status:
        members = Member.objects.filter(status=status)
    else:
        members = Member.objects.all()
    
    member_resource = MemberResource()
    dataset = member_resource.export(members)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="members_{status}.csv"'
    return response



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def import_member_fees(request):
    if request.method == 'POST':
        member_fee_resource = MemberFeeResource()
        dataset = Dataset()
        new_member_fees = request.FILES['myfile']

        imported_data = dataset.load(new_member_fees.read(), format='xlsx')
        result = member_fee_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            member_fee_resource.import_data(dataset, dry_run=False)  # Actually import now
            # Update members who did not match any MemberFee data
            processed_noPekerja = member_fee_resource.processed_noPekerja
            Member.objects.exclude(noPekerja__in=processed_noPekerja).update(status='Not a Member')
            messages.success(request, 'Import was successful')
            

        else:
            messages.error(request, 'Import failed due to errors')


    return render(request, 'member/import_member_fees.html')



def member_fee_detail(request, member_id):
    # Get the member by ID
    member = get_object_or_404(Member, id=member_id)
    # Get all MemberFee entries related to this member
    member_fees = member.fees.all()

    context = {
        'member': member,
        'member_fees': member_fees,
    }
    return render(request, 'member/member_fee_detail.html', context)



# ======================== - Txt to Excel - ========================

import os
import pandas as pd  # New code: Import pandas
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from .forms import UploadFileForm


def clean_file_content(content):
    lines = content.splitlines()
    cleaned_lines = []

    
    for line in lines:
        if line.strip() == '':
            continue
        if 'Sistem Gaji' in line:
            continue
        if 'Penerima :' in line:
            continue
        if '-----' in line:
            continue
        if 'Pengurusan (Shah Alam)' in line:
            continue
        if 'Laporan Senarai Penerima' in line:
            continue
        if 'JUMLAH BAGI' in line:
            continue
        if 'JUMLAH KESELURUHAN' in line:
            continue
        if 'TAMAT LAPORAN' in line:
            continue
        if 'Kod' in line and 'Jbtn' in line and 'Keterangan' in line:
            continue
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            date = form.cleaned_data['date']  # New code: Get the date from the form
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)

            with open(file_path, 'r') as file:
                content = file.read()

            cleaned_content = clean_file_content(content)
            cleaned_filename = f"cleaned_{uploaded_file.name}"
            cleaned_file_path = os.path.join(fs.location, cleaned_filename)

            with open(cleaned_file_path, 'w') as file:
                file.write(cleaned_content)

            # New code: Convert cleaned text file to Excel using fixed-width formatting
            cleaned_lines = cleaned_content.splitlines()
            cleaned_file_path = os.path.join(fs.location, cleaned_filename)
            with open(cleaned_file_path, 'w') as file:
                file.write(cleaned_content)

            # Define column widths based on the red lines in the image
            colspecs = [(0, 5), (5, 13), (13, 41), (41, 50), (50, 81), (81, 96), (96, 117), (117, 130)]
            df = pd.read_fwf(cleaned_file_path, colspecs=colspecs, header=None)
            df.columns = ['kod', 'jbtn', 'keterangan', 'noPekerja', 'nama', 'noIC', 'NoRujukan', 'amount']

            # New code: Add the date column
            df['date'] = date

            excel_filename = f"cleaned_{uploaded_file.name.split('.')[0]}.xlsx"
            excel_file_path = os.path.join(fs.location, excel_filename)
            df.to_excel(excel_file_path, index=False)

            with open(excel_file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename={excel_filename}'
                return response

    else:
        form = UploadFileForm()
    return render(request, 'member/upload.html', {'form': form})


# ==================================================================





from django.shortcuts import render
from django.db.models import Sum
from .models import MemberFee
import calendar

def member_fees_table_(request):
    # Get all member fees
    fees = MemberFee.objects.all()

    # Initialize a dictionary to store the aggregated data
    data = {}

    # Iterate over each fee and aggregate the amounts by month for each member
    for fee in fees:
        if fee.noPekerja not in data:
            data[fee.noPekerja] = {
                'nama': fee.nama,
                'January': 0,
                'February': 0,
                'March': 0,
                'April': 0,
                'May': 0,
                'June': 0,
                'July': 0,
                'August': 0,
                'September': 0,
                'October': 0,
                'November': 0,
                'December': 0,
            }
        
        # Determine the month from the date field
        month_name = calendar.month_name[fee.date.month]
        data[fee.noPekerja][month_name] += int(fee.amount)

    # Convert the data dictionary to a list of dictionaries for easier template rendering
    data_list = [{'noPekerja': k, **v} for k, v in data.items()]

    return render(request, 'member/member_fee.html', {'data': data_list})

def download_excel_(request):
    # Get all member fees
    fees = MemberFee.objects.all()

    # Initialize a dictionary to store the aggregated data
    data = {}

    # Iterate over each fee and aggregate the amounts by month for each member
    for fee in fees:
        if fee.noPekerja not in data:
            data[fee.noPekerja] = {
                'nama': fee.nama,
                'January': 0,
                'February': 0,
                'March': 0,
                'April': 0,
                'May': 0,
                'June': 0,
                'July': 0,
                'August': 0,
                'September': 0,
                'October': 0,
                'November': 0,
                'December': 0,
            }
        
        # Determine the month from the date field
        month_name = calendar.month_name[fee.date.month]
        data[fee.noPekerja][month_name] += int(fee.amount)

    # Convert the data dictionary to a DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')

    # Create a HttpResponse object with the appropriate Excel header
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=member_fees.xlsx'

    # Use pandas to write the DataFrame to the response
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Member Fees')

    return response

from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import calendar
from .models import MemberFee

def member_fees_table(request):
    # Get all member fees
    fees = MemberFee.objects.all()

    # Get the list of years available in the data
    years = fees.dates('date', 'year').distinct()

    # Get the selected year from the request, default to the first available year
    selected_year = request.GET.get('year', years[0].year if years else None)
    if selected_year:
        fees = fees.filter(date__year=selected_year)

    # Initialize a dictionary to store the aggregated data
    data = {}

    # Iterate over each fee and aggregate the amounts by month for each member
    for fee in fees:
        if fee.noPekerja not in data:
            data[fee.noPekerja] = {
                'nama': fee.nama,
                'January': 0,
                'February': 0,
                'March': 0,
                'April': 0,
                'May': 0,
                'June': 0,
                'July': 0,
                'August': 0,
                'September': 0,
                'October': 0,
                'November': 0,
                'December': 0,
            }
        
        # Determine the month from the date field
        month_name = calendar.month_name[fee.date.month]
        data[fee.noPekerja][month_name] += int(fee.amount)

    # Convert the data dictionary to a list of dictionaries for easier template rendering
    data_list = [{'noPekerja': k, **v} for k, v in data.items()]

    return render(request, 'member/member_fee.html', {'data': data_list, 'years': years, 'selected_year': int(selected_year)})

def download_excel(request):
    # Get all member fees
    fees = MemberFee.objects.all()

    # Initialize a dictionary to store the aggregated data
    data = {}

    # Iterate over each fee and aggregate the amounts by month for each member
    for fee in fees:
        if fee.noPekerja not in data:
            data[fee.noPekerja] = {
                'nama': fee.nama,
                'January': 0,
                'February': 0,
                'March': 0,
                'April': 0,
                'May': 0,
                'June': 0,
                'July': 0,
                'August': 0,
                'September': 0,
                'October': 0,
                'November': 0,
                'December': 0,
            }
        
        # Determine the month from the date field
        month_name = calendar.month_name[fee.date.month]
        data[fee.noPekerja][month_name] += int(fee.amount)

    # Convert the data dictionary to a DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')

    # Create a HttpResponse object with the appropriate Excel header
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=member_fees.xlsx'

    # Use pandas to write the DataFrame to the response
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Member Fees')

    return response