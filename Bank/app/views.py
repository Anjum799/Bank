from django.shortcuts import render,HttpResponse
from .forms import AccountForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Account

# Create your views here.
def home(request):
    return render (request,"index.html")
# vzod cnnb davb hrei
def create(request):
    form = AccountForm()
    if request.method =="POST":
        form = AccountForm(request.POST,request.FILES) 
        if form.is_valid():
            form.save()
            print("successfull")
            # print(form.data)
            reciver_email = form.data["email"]
            data = Account.objects.get(email = reciver_email)
            acc = data.account_number
            print("successfull")
            try:
                send_mail(
                    "Thanks for Registration",  #subject
                    f"Thank you for registring with our ARJS Bank. We are excited to have youon board! Your account number is <h1>{acc}</h1>, /n thank you /n regards ARJS Bank manager", #body
                    settings.EMAIL_HOST_USER ,
                    [reciver_email],
                    fail_silently=False,
                )
                print("mail send")
            except Exception as e:
                return HttpResponse(f" Error sending Email:{e} ")     
    return render(request,"create.html",{'form':form})

def Pin_generation(request):
    form = AccountForm()
    if request.method == "POST":
        acc = request.POST.get('account_number')
        mobile = request.POST.get('mobile')
        pin = int(request.POST.get('pin'))
        cpin = int(request.POST.get('cpin'))

        try:
            account = Account.objects.get(account_number=acc)
        except Account.DoesNotExist:
            return HttpResponse("Account not found in database")
        
        if account.mobile == int(mobile):
            if pin == cpin:
                pin += 111  # PIN modification
                account.pin = pin
                account.save()
                
                # Sending email confirmation
                try:
                    send_mail(
                        "PIN Generated Successfully",
                        f"Dear {account.name},\n\nYour PIN has been successfully created for your account {acc}. Please keep it secure.\n\nThank you,\nARJS Bank Team",
                        settings.EMAIL_HOST_USER,
                        [account.email],
                        fail_silently=False,
                    )
                    print("PIN generation email sent")
                except Exception as e:
                    return HttpResponse(f"Error while pin generator sending Email: {e}")
                return HttpResponse("PIN generated successfully, and email sent.")
            else:
                return HttpResponse("Both PINs do not match.")
        else:
            return HttpResponse("Mobile number does not match our records.")
    
    return render(request, "pin_gen.html", {'form': form})
def Balance(request):
    bal=0
    var=False
    if request.method == "POST":
        var=True
        acc=request.POST.get("acc")
        pin= int(request.POST.get("pin"))
        # print(acc,pin)
        try:
            account=Account.objects.get(account_number=acc)
            # print(account)
        except:
            return HttpResponse("account not found")
        encpin=account.pin-111
        if pin == encpin:
            # print("pin matched")
            bal=account.balance
        else:
          return HttpResponse("pin didn't match")         
    return render(request,"balance.html",{"bal":bal,"var":var})


def deposit(request):
    bal = 0
    var = False
    if request.method == "POST":
        var = True
        acc = request.POST.get("acc")
        phone = int(request.POST.get("mobile"))
        amt = int(request.POST.get("amt"))

        try:
            account = Account.objects.get(account_number=acc)
        except Account.DoesNotExist:
            return HttpResponse("Account not found")  
        
        if account.mobile == phone:
            if 100 <= amt <= 10000:
                account.balance += amt
                account.save()
                bal = account.balance

                # Sending deposit email
                try:
                    send_mail(
                        "Deposit Successful",
                        f"Dear {account.name},\n\nYou have successfully deposited {amt} into your account {acc}.\nYour updated balance is {bal}.\n\nThank you,\nARJS Bank Team",
                        settings.EMAIL_HOST_USER,
                        [account.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    return HttpResponse(f"Error while sending deposit email: {e}")

                # return HttpResponse(f"Deposit successful. Updated balance: {bal}")
            else:
                return HttpResponse("Please enter a valid amount to deposit.")
        else:
            return HttpResponse("Enter a valid mobile number.")

    return render(request, "deposit.html", {"bal": bal, "var": var})

def withdrawl(request):
    var = False
    bal = 0
    if request.method == "POST":
        var = True
        acc = request.POST["acc"]
        pin = int(request.POST["pin"])
        amt = int(request.POST["amt"])

        try:
            account = Account.objects.get(account_number=acc)
        except Account.DoesNotExist:
            return HttpResponse("Account not found")  

        check_pin = account.pin - 111
        if check_pin == pin:
            if account.balance > amt and 500 <= amt <= 10000:
                account.balance -= amt
                account.save()
                bal = account.balance

                # Sending withdrawal email
                try:
                    send_mail(
                        "Withdrawal Successful",
                        f"Dear {account.name},\n\nYou have successfully withdrawn {amt} from your account {acc}.\nYour updated balance is {bal}.\n\nThank you,\nARJS Bank Team",
                        settings.EMAIL_HOST_USER,
                        [account.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    return HttpResponse(f"Error while sending withdrawal email: {e}")

                # return HttpResponse(f"Withdrawal successful. Updated balance: {bal}")
            else:
                return HttpResponse("Please enter a valid amount.")
        else:
            return HttpResponse("Incorrect PIN.")

    return render(request, "withdrawl.html", {'bal': bal, "var": var})


def account_transfer(request):
    if request.method == "POST":
        acc = request.POST["acc"]
        tacc = request.POST["tacc"]
        amt = int(request.POST["amt"])
        pin = int(request.POST["pin"])
        try:
            account = Account.objects.get(account_number=acc)
        except Account.DoesNotExist:
            return HttpResponse("Sender account not found")  
        try:
            to_account = Account.objects.get(account_number=tacc)
        except Account.DoesNotExist:
            return HttpResponse("Receiver account not found")  
        check_pin = account.pin - 111
        if check_pin == pin:
            if account.balance > amt:
                account.balance -= amt
                to_account.balance += amt
                account.save()
                to_account.save()
                # Sending transfer email
                try:
                    send_mail(
                        "Funds Transfer Successful",
                        f"Dear {account.name},\n\nYou have successfully transferred {amt} to account {tacc}.\nYour updated balance is {account.balance}.\n\nThank you,\nARJS Bank Team",
                        settings.EMAIL_HOST_USER,
                        [account.email],
                        fail_silently=False,
                    )
                    send_mail(
                        "Funds Received",
                        f"Dear {to_account.name},\n\nYou have received {amt} from account {acc}.\nYour updated balance is {to_account.balance}.\n\nThank you,\nARJS Bank Team",
                        settings.EMAIL_HOST_USER,
                        [to_account.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    return HttpResponse(f"Error while sending transfer email: {e}")
                # return HttpResponse(f"Transfer successful. Updated balance: {account.balance}")
            else:
                return HttpResponse("Insufficient balance.")
        else:
            return HttpResponse("Incorrect PIN.")
    return render(request, "transfer.html") 