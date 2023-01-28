from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from app.client_utils import register_link, get_accounts, get_transactions
from app.forms import BasicForm
from app.models import Institution, Link

@login_required(login_url='login')
def app_index(request):
    return render(request,'modules/index.html')

@login_required(login_url='login')
def app_index(request):
    links = request.user.link_set.all()
    context = {'links': links}
    return render(request,'modules/index.html', context)

@login_required(login_url='login')
def add_bank(request):
    context = { 'banks': Institution.objects.all() }
    return render(request,'modules/add_bank.html', context)

@login_required(login_url='login')
def login_bank(request, bank_slug):
    user = request.user
    bank = get_object_or_404(Institution, slug=bank_slug)

    if Link.objects.filter(user=user).filter(institution=bank):
        messages.warning(request,'Banco ya registrado')
        return redirect('/index')

    if request.method == 'GET':
        form = BasicForm()
        context = {
            'bank': bank,
            'form': form
        }
        return render(request,'modules/login_bank.html',context)
    elif request.method == 'POST':
        form = BasicForm(request.POST)
        if form.is_valid():
            register_link(user, form, bank)
            return redirect('/index')
        context = {
            'bank': bank,
            'form': form
        }
        return render(request,'modules/login_bank.html',context)
        
    return HttpResponseNotAllowed()

@login_required(login_url='login')
def link_accounts(request, link_id):
    user = request.user
    link = Link.objects.filter(id=link_id).filter(user=user)
    if link:
        bank = link[0].institution
        context = {
            'link_id': link_id,
            'bank': bank,
            'accounts': get_accounts(str(link_id)),
        }
        
        return render(request,'modules/accounts.html', context)

    return render(request, '401.html', status=401)

@login_required(login_url='login')
def transactions(request, link_id, account_id):
    user = request.user
    link = Link.objects.filter(id=link_id).filter(user=user)
    if link:
        bank = link[0].institution
        context = {
            'account': get_accounts(str(link_id), str(account_id)),
            'link': link,
            'bank': bank,
            'transactions': get_transactions(str(link_id), str(account_id)),
        }
        
        return render(request,'modules/transactions.html', context)

    return render(request, '401.html', status=401)

# acc = {'id': '3adaf03e-10fc-444e-89ed-52b77e80af13', 'link': 'c9a2ba01-655f-46f8-b450-914af2fb2908', 'institution': {'name': 'erebor_mx_retail', 'type': 'bank'}, 'created_at': '2023-01-23T01:15:01.552802Z', 'collected_at': '2023-01-22T22:30:44.161646Z', 'currency': 'MXN', 'category': 'LOAN_ACCOUNT', 'type': 'Créditos', 'number': '542815', 'agency': '15310826', 'bank_product_id': '3486586', 'internal_identification': '15652267', 'public_identification_name': 'ACCOUNT_NUMBER', 'public_identification_value': '1536668', 'credit_data': None, 'loan_data': {'collected_at': '2023-01-20T18:03:08.468752Z', 'credit_limit': 96908, 'cutting_day': '10', 'cutting_date': '2023-03-16', 'next_payment_date': '2023-02-02', 'limit_date': '2023-01-24', 'limit_day': '1', 'monthly_payment': None, 'no_interest_payment': None, 'last_payment_date': '2023-01-15', 'last_period_balance': None, 'interest_rate': None, 'principal': None, 'loan_type': None, 'payment_due_day': None, 'outstanding_balance': None, 'outstanding_principal': None, 'number_of_installments_total': None, 'number_of_installments_outstanding': None, 'contract_start_date': None, 'contract_number': None, 'interest_rates': None}, 'name': 'Cuenta digital', 'balance': {'current': 72363.81, 'available': 72363.81}, 'last_accessed_at': '2023-01-22T21:37:22', 'balance_type': 'LIABILITY'}
# tran = [{'accounting_date': '2023-01-17T19:41:14', 'amount': 508.59, 'category': 'Taxes', 'description': 'TELEFONICATAAPP MEXICO DF 0000000', 'status': 'PENDING'}, {'accounting_date': '2023-01-22T05:09:41', 'amount': 3000, 'category': 'Online Platforms & Leisure', 'description': 'PEAR MUSIC', 'status': 'PROCESSED'}, {'accounting_date': '2023-01-15T07:45:18', 'amount': 39.5, 'category': None, 'description': 'Oxxo deposito a Tarjeta Deb.', 'status': 'PROCESSED'}, {'accounting_date': '2023-01-13T08:30:21', 'amount': 563.7, 'category': 'Personal Shopping', 'description': 'MERCADO PAGO 1 CIUDAD DE MEX 0000000', 'status': 'PENDING'}, {'accounting_date': '2023-01-19T09:10:49', 'amount': 3.56, 'category': 'Transport & Travel', 'description': 'Oxxo deposito a Tarjeta Deb.', 'status': 'PENDING'}]

# @login_required(login_url='login')
# def transactions(request, link_id, account_id):
#     user = request.user
#     link = Link.objects.filter(id=link_id).filter(user=user)
#     if link:
#         bank = link[0].institution
#         context = {
#             'account': acc,
#             'link': link,
#             'bank': bank,
#             'transactions': tran,
#         }
        
#         return render(request,'modules/transactions.html', context)

#     return render(request, '401.html', status=401)

def page_error_401(request, exception):
    return render(request, '401.html')

def page_error_404(request, exception):
    return render(request, '404.html')

def page_error_500(request):
    return render(request, '500.html')