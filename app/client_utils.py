from belvo.client import Client
from datetime import datetime

from app.models import Link
from dashboard.settings import BELVO_SECRET_ID, BELVO_SECRET_KEY, BELVO_ENVIROMENT

client = Client(BELVO_SECRET_ID, BELVO_SECRET_KEY, BELVO_ENVIROMENT)

def register_link(model_user, user_form, institution):
    user = user_form.cleaned_data['user']
    password = user_form.cleaned_data['password']
    link = client.Links.create(
        institution = institution.slug,
        username    = user,
        password    = password
    )

    Link.objects.create(
        user = model_user,
        id = link['id'],
        institution = institution
    )

def get_accounts(link_id, account_id=None):
    accounts = client.Accounts.create(
        link = link_id
    )

    if account_id is not None:
        for account in accounts:
            if account['id'] == account_id:
                return account

    return accounts

format = lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

def get_transactions(link_id, account_id):
    transactions = []
    for transaction in client.Transactions.list(
        link    = link_id,
        account = account_id
    ):
        transactions.append({
            'accounting_date': format(transaction['accounting_date']),
            'amount': transaction['amount'],
            'category': transaction['category'],
            'description': transaction['description'],
            'status': transaction['status']
        })

    return transactions