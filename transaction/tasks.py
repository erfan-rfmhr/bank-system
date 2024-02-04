from datetime import datetime, timedelta
from celery import shared_task
from .models import AccountModel


@shared_task
def release_blocked_amount(*args, **kwargs):
    today = datetime.now().date()
    seporde_accounts = AccountModel.objects.filter(blocked_until=today)

    print("Task pass")
    for account in seporde_accounts:
        amount = account.balance

        if AccountModel.objects.filter(user = account.user.id , type ='jari').exists():
            jari_account = AccountModel.objects.get(user = account.user.id  , type ='jari')
        else:
            continue

        profit = calculate_profit(amount)
        
        account.balance -= amount
        jari_account.balance += amount + profit

        account.blocked_until = None
        account.is_blocked = False
        account.save()
        jari_account.save()
        

def calculate_profit(amount):
    profit = amount * 0.1
    return profit