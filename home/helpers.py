from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from .models import *




def send_email_with_attachment(subject,messsage,recepient_list,file_path):
    mail =EmailMessage(subject=subject,body=messsage, from_email= settings.EMAIL_HOST_USER,
                       to=recepient_list)
    
    mail.attach_file(file_path)
    mail.send()



def send_email_to_client(m):
    message=m
    subject = "Price is triggered"
    from_email = settings.EMAIL_HOST_USER
    recepient_list = ["sonaryash1406@gmail.com"]
    send_mail(subject,message,from_email,recepient_list)

def trigger_mail():
    alerts = LaptopPriceAlert.objects.all()
    for alert in alerts:
        name = alert.laptop_name
        desired_price = alert.desired_price
        laptops = Gaminglaptop.objects.filter(Name__icontains=name)
        for laptop in laptops:
            if laptop.Price <= desired_price:
                message = f'Price for {name} is reduced to ₹{laptop.Price}'
                send_email_to_client(message)
                # messages.info(request, 'Email alert sent successfully.')
                # alert.delete()