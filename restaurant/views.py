from django.shortcuts import render

import random, time

# Create your views here.

Menu = [
    {"text": "Nihari"},
    {"text": "Biryani"},
    {"text": "Sheermal"},
    {"text": "Barfi"},
]


def main(request):
    '''Show the web page with the form.'''
    
    template_name = 'restaurant/main.html'
    
    context = {
        'image_path': "food1.jpeg",
    } 
    
    return render(request, template_name, context)

def order(request):
    '''Show the web page with the form.'''
    
    random_menu = random.choice(Menu)
    
    template_name = 'restaurant/order.html'
    
    context = {
        'menuitem1': "nihari.jpg",
        'menuitem2': "biryani.jpg",
        'menuitem3': "bread.jpeg",
        'menuitem4': "barfi.jpg",
        'Menu_of_the_day': random_menu['text'],
    } 
    return render(request, template_name, context)

def submit(request):
    '''Process the form submission, and generate a result.'''
    
    minutes = random.randint(30, 60)
    ready_time = time.ctime(time.time() + minutes * 60)
    
    template_name = 'restaurant/confirmation.html'
    
    # read the form data into python variables:
    if request.POST:
        
        name = request.POST['Name']
        nihari = request.POST['Nihari']
        
        context = {
            'minutes': minutes,
            'current_time': time.ctime(),
            'ready_time': ready_time,
            'Name': name,
            'Nihari': nihari,
        }
    
    return render(request, template_name, context=context)
