from django.shortcuts import render,redirect
import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
from home.models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from home.helpers import *
from io import BytesIO
from django.template.loader import *
import xhtml2pdf.pisa as pisa
import pandas as pd
from .forms import *
from django.contrib import messages
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity





def save_pdf(laptops):
    params = {'laptops': laptops}
    template = get_template("pdf.html")
    html = template.render(params)

    file_path = str(settings.BASE_DIR) + '/Laptops.pdf'
    
    try:
        with open(file_path, 'wb+') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
    except Exception as e:
        print(e)
        return None

    if pdf.err:
        return None

def scrape_data(request):
    url = "https://www.flipkart.com/search?q=gaming+laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&as-pos=1&as-type=RECENT&suggestionId=gaming+laptop%7CLaptops&requestId=b5a0e973-2626-4eb7-b11d-bf6e9775f976&as-searchtext=gaming%20laptop"
    r = rq.get(url)
    soup = bs(r.text, "lxml")

    product = []
    price = []
    description = []

    names = soup.find_all("div", class_="KzDlHZ")
    prices = soup.find_all("div", class_="Nx9bqj _4b5DiR")
    desc = soup.find_all("ul", class_="G4BRas")

    for i in names:
        name = i.text
        product.append(name)
    for i in prices:
        p = i.text
        p_cleaned = int(p.replace('₹', '').replace(',', ''))
        price.append(p_cleaned)
        
    for i in desc:
        d = i.text
        description.append(d)

    data = {
        "Name": product,
        "Price": price,
        "Description": description
    }

    df = pd.DataFrame(data)
    records = df.to_dict('records')
    Gaminglaptop.objects.all().delete()

    for record in records:
        Gaminglaptop.objects.create(
            Name=record['Name'],
            Price=record['Price'],
            Description=record['Description']
        )

    g = Gaminglaptop.objects.all()
    similar_items = []

    if request.GET.get('search'):
        search = request.GET.get('search')
        try:
            search_price = int(search)
            g = g.filter(Q(Price__lte=search_price))
        except ValueError:
            g = g.filter(
                Q(Name__icontains=search) |
                Q(Description__icontains=search)
            )    
        g = g.order_by('Price') 
        save_pdf(g)       
        filtered_data = g.values('Name', 'Price', 'Description')
        df_filtered = pd.DataFrame(list(filtered_data))
        df_filtered.to_csv("Laptops.csv", index=False)

        descriptions = df_filtered['Name'].tolist()
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(descriptions)
        search_vec = vectorizer.transform([search])
        similarity = cosine_similarity(search_vec, X).flatten()
        similar_indices = similarity.argsort()[:-6:-1] 
        similar_items = [df_filtered.iloc[i] for i in similar_indices]

    paginator = Paginator(g, 6) 
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(request, "index.html", context={'laptops': page_obj, 'recommendations': similar_items})


# def scrape_data(request):
#     url = "https://www.flipkart.com/search?q=gaming+laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&as-pos=1&as-type=RECENT&suggestionId=gaming+laptop%7CLaptops&requestId=b5a0e973-2626-4eb7-b11d-bf6e9775f976&as-searchtext=gaming%20laptop"
#     r = rq.get(url)
#     soup = bs(r.text, "lxml")

#     product = []
#     price = []
#     description = []

#     names = soup.find_all("div", class_="KzDlHZ")
#     prices = soup.find_all("div", class_="Nx9bqj _4b5DiR")
#     desc = soup.find_all("ul", class_="G4BRas")

#     for i in names:
#         name = i.text
#         product.append(name)
#     for i in prices:
#         p = i.text
#         # Remove ₹ and , then convert to float
#         p_cleaned = int(p.replace('₹', '').replace(',', ''))
#         price.append(p_cleaned)
        
#     for i in desc:
#         d = i.text
#         description.append(d)



#     data = {
#         "Name": product,
#         "Price": price,
#         "Description": description
#     }

#     df = pd.DataFrame(data)
#     records = df.to_dict('records')
#     Gaminglaptop.objects.all().delete()
#     # df.to_csv("Data.csv")

#     for record in records:
#         Gaminglaptop.objects.create(
#             Name=record['Name'],
#             Price=record['Price'],
#             Description=record['Description']
#         )
#     g = Gaminglaptop.objects.all()

#     if request.GET.get('search'):
#         search  = request.GET.get('search')
#         try:
#             search_price = int(search)
#             g = g.filter(Q(Price__lte=search_price))
#         except ValueError:
#             g = g.filter(
#                 Q(Name__icontains=search) |
#                 Q(Description__icontains=search)
#             )    
#         g=g.order_by('Price') 
#         save_pdf(g)       
#         filtered_data = g.values('Name', 'Price', 'Description')
#         df_filtered = pd.DataFrame(list(filtered_data))
#         df_filtered.to_csv("Laptops.csv", index=False)
#     paginator = Paginator(g, 6) 
#     page_number = request.GET.get("page",1)
#     page_obj = paginator.get_page(page_number)
#     return render(request, "index.html",context={'laptops':page_obj})




def send_email(request):
    g = Gaminglaptop.objects.all()
    
    # Save filtered records to PDF

    pdf_file_path = str(settings.BASE_DIR) + '/Laptops.pdf'
    filtered_data = g.values('Name', 'Price', 'Description')
    csv_file_path = str(settings.BASE_DIR) + '/Laptops.csv'
    subject = "Filtered Gaming laptops"
    message = "Attached are the filtered gaming laptops."
    recepient_list = ["sonaryash1406@gmail.com"]
    
    email = EmailMessage(subject, message, to=recepient_list)
    if pdf_file_path:
        email.attach_file(pdf_file_path)
    email.attach_file(csv_file_path)
    
    try:
        email.send()
    except Exception as e:
        print(f"Failed to send email: {e}")
    messages.info(request, 'Email sent successfully.')
    return redirect('/')


def set_price_alert(request):
    if request.method == 'POST':
        form = LaptopPriceAlertForm(request.POST)
        if form.is_valid():
            laptop_name = form.cleaned_data['laptop_name']
            desired_price = form.cleaned_data['desired_price']
            LaptopPriceAlert.objects.create(laptop_name=laptop_name,desired_price=desired_price)
            form.save()
            messages.info(request,'Price alert set successfully')
            trigger_mail()
            return redirect('/')
  # Saves the form data to the database
    else:
        form = LaptopPriceAlertForm()
    return render(request, 'alert.html', {'form': form})


from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset and fit the TF-IDF vectorizer once when the server starts
df = pd.read_csv('Data.csv')
df['Name'] = df['Name'].str.lower()
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['Name'])

def recommend_names(request):
    # print(df.head(5))
    input_name = request.GET.get('name', '')
    if input_name:
        input_vector = vectorizer.transform([input_name.lower()])
        similarity_scores = cosine_similarity(input_vector, tfidf_matrix)
        top_indices = similarity_scores[0].argsort()[-6:][::-1]
        recommendations = df.iloc[top_indices].to_dict(orient='records')
        return render(request,"result.html",{'recommendations': recommendations})
    # return JsonResponse({'error': 'No name provided'}, status=400)
    return render(request,"result.html")


def rc(request):
    return render(request,"rc.html")