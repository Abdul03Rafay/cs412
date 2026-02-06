from django.shortcuts import render

import random, time

# Create your views here.

Menu = [
    {"text": "Nihari", "price": 18.99},
    {"text": "Biryani", "price": 12.99},
    {"text": "Sheermal", "price": 4.99},
    {"text": "Barfi", "price": 1.99},
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
    if request.POST:
    
        # read the form data into python variables:
        
        # Capture Customer Info
        name = request.POST.get('Name')
        phone = request.POST.get('Phone')
        email = request.POST.get('Email')
        instructions = request.POST.get('Special_instructions')
        special_item = request.POST.get('special_item')
        
        items_ordered = []
        total_price = 0
        
        # Logic for food item : Nihari
        if 'Nihari' in request.POST:
            price = 18.99
            if special_item == "Nihari": price *= 0.8 # for daily special discount 20%
            total_price += price
            garnishes = []
            if "Ginger" in request.POST: garnishes.append("Ginger")
            if "Lemon" in request.POST: garnishes.append("Lemon")
            if "Coriander" in request.POST: garnishes.append("Coriander") 
            items_ordered.append(f"Nihari (Garnishes: {', '.join(garnishes) if garnishes else 'None'})")
            
        # Logic for food item : Biryani
        if 'Biryani' in request.POST:
            price = 12.99
            if 'Medium' in request.POST: price += 2.99
            elif "Large" in request.POST: price += 4.99
            
            if special_item == "Biryani": price *= 0.8
            total_price += price
            items_ordered.append("Biryani")
            
        # Logic for food item : Sheermal
        if 'Sheermal' in request.POST:
            price = 4.99
            if 'S3' in request.POST: price += 2.99
            elif 'S5' in request.POST: price += 4.99
            
            if special_item == "Sheermal": price *= 0.8
            total_price += price
            items_ordered.append("Sheermal Bread")
        
        # Logic for food item : Barfi
        if "Barfi" in request.POST:
            price = 1.99
            if 'B3' in request.POST: price += 1.99
            elif 'B5' in request.POST: price += 3.99
            
            if special_item == "Barf": price *= 0.8
            total_price += price
            items_ordered.append("Barfi")
        
        template_name = 'restaurant/confirmation.html'
        
        # Time calculation
        minutes = random.randint(30, 60)
        
        ready_time_raw = time.time() + (minutes * 60)
        ready_time = time.strftime("%I: %M %p", time.localtime(ready_time_raw)) # format time nicely
            
        context = {
                'name': name,
                'phone': phone,
                'email': email,
                'instructions': instructions,
                'items_ordered': items_ordered,
                'total_price': f"{total_price: .2f}",
                'minutes': minutes,
                'ready_time': ready_time,
        }
        return render(request, template_name, context=context)

    return render(request, 'restaurant/order.html')
