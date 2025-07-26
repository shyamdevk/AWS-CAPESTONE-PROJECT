from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

import random

# Create your views here.

from django.shortcuts import render,redirect 
from datetime import datetime  
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *  
from django.template import loader  
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse


def home(request):
    allproduct=Product.objects.all()
    return render(request,"hero.html",{'filename':allproduct})


def login(request): 
    return render(request, "login.html")

def DBLogin(request): 
    template = loader.get_template('login.html') 
    context = {}
    if request.method == "POST": 
            username = request.POST.get('txtEmail') 
            password = request.POST.get('txtPassword') 
            login_obj = User.objects.filter(username=username).exists()
            if login_obj:
                user_obj = User.objects.get(username=username, password=password) 
                request.session['USERNAME'] = user_obj.username 
                request.session['USER_ID'] = user_obj.id 
                return redirect('home') # Redirect to home after login
            else:
                context = {"error": "invalid user"}
                return HttpResponse(template.render(context, request)) 
            context = {"error": "invalid password"} 
            return HttpResponse(template.render(context, request)) 
    return HttpResponse(template.render(context, request)) 
def logout(request): 
    del request.session['USERNAME'] 
    return render(request, "login.html")

def registration(request):
    return render(request,"register.html")
def register(request): 
    if request.method=="POST":
        Username=request.POST["username"]
        Password=request.POST["password"]
        Email=request.POST["email"]
        Role=request.POST["role"]
        Phone=request.POST["contact"]
        std=User(username=Username,password=Password,email=Email,role=Role,phone=Phone)
        std.save()
    return render(request,"login.html")




            




def productupload(request):
    if request.method == 'POST':
        # Ensure the user is logged in
        user_id = request.session.get('USER_ID')
        if not user_id:
            return redirect('login')  # Redirect to login if the user is not logged in

        # Get the form data
        name = request.POST.get("productname")
        actualprice = request.POST.get("actual_price")
        offerprice = request.POST.get("offer_price")
        description = request.POST.get("productdetails")
        category = request.POST.get("category")
        quantity = request.POST.get("quantity")
        Type = request.POST.get("type")

        # Handle image files
        myFile1 = request.FILES.get('image1')
        myFile2 = request.FILES.get('image2')
        myFile3 = request.FILES.get('image3')

        # Create FileSystemStorage instance to store files (Optional if using ImageField)
        fs = FileSystemStorage()

        file_name1 = str(datetime.timestamp(datetime.now())) + myFile1.name if myFile1 else ''
        file_name2 = str(datetime.timestamp(datetime.now())) + myFile2.name if myFile2 else ''
        file_name3 = str(datetime.timestamp(datetime.now())) + myFile3.name if myFile3 else ''
        
        # Save the files
        if myFile1:
            fs.save(file_name1,myFile1)
        if myFile2:
            fs.save(file_name2,myFile2)
        if myFile3:
            fs.save(file_name3,myFile3)

        # Create a Product object
        product = Product(
            user_id=user_id,  # Use user_id to link product to the logged-in user
            productname=name,
            productdetails=description,
            actual_price=actualprice,
            offer_price=offerprice,
            category=category,
            types=Type,
            quantity=quantity,
            image1=file_name1,  # Directly assign file object for ImageField
            image2=file_name2,
            image3=file_name3
        )
        
        # Save the product to the database
        product.save()

        # Redirect to the product view page after uploading
        return redirect('viewproductupload')  # Redirect to view uploaded products page

    # If it's a GET request, render the product upload form
    return render(request,'productupload.html')



def viewproductupload(req):  

    # Check if the user is logged in (check if session has 'USER_ID')
    user_id = req.session.get('USER_ID')

    if not user_id:
        return redirect('login')  # Redirect to login page if no user_id in session

    # Retrieve the user object using the user_id from the session
    user = User.objects.get(id=user_id)

    # Get products associated with the logged-in user
    display_profile = Product.objects.filter(user=user)

    # Return the template with the products
    return render(req, 'viewproduct.html', {'filename': display_profile})
def delFile(request, id):
    try:
        fu = get_object_or_404(Product, id=id)
        fs = FileSystemStorage()
        if fu.image1 and fs.exists(fu.image1): 
            fs.delete(fu.image1)
        if fu.image2 and fs.exists(fu.image2): 
            fs.delete(fu.image2)
        if fu.image3 and fs.exists(fu.image3): 
            fs.delete(fu.image3)
        fu.delete()
        return redirect('/viewproductupload')
    
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


def edit(request, sid):
    products = Product.objects.get(id=sid)
    context = {'products': products}
    return render(request, 'edit.html',context)


def updateStd(request, sid):
    try:
        # Get the product object by ID
        product = Product.objects.get(id=sid)
        
        if request.method == 'POST':
            # Ensure the user is logged in
            user_id = request.session.get('USER_ID')
            if not user_id:
                return redirect('login')  # Redirect to login if the user is not logged in

            # Get the form data
            name = request.POST.get("productname")
            actualprice = request.POST.get("actual_price")
            offerprice = request.POST.get("offer_price")
            description = request.POST.get("productdetails")
            category = request.POST.get("category")
            quantity = request.POST.get("quantity")
            Type = request.POST.get("type")

            # Handle image files (if provided)
            myFile1 = request.FILES.get('image1')
            myFile2 = request.FILES.get('image2')
            myFile3 = request.FILES.get('image3')

            # Create FileSystemStorage instance to store files
            fs = FileSystemStorage()

            # Generate unique filenames based on the current timestamp
            file_name1 = str(datetime.timestamp(datetime.now())) + myFile1.name if myFile1 else product.image1
            file_name2 = str(datetime.timestamp(datetime.now())) + myFile2.name if myFile2 else product.image2
            file_name3 = str(datetime.timestamp(datetime.now())) + myFile3.name if myFile3 else product.image3
            
            # Save the files if they were uploaded
            if myFile1:
                fs.save(file_name1, myFile1)
            if myFile2:
                fs.save(file_name2, myFile2)
            if myFile3:
                fs.save(file_name3, myFile3)

            # Update the product object with new data
            product.productname = name
            product.productdetails = description
            product.actual_price = actualprice
            product.offer_price = offerprice
            product.category = category
            product.types = Type
            product.quantity = quantity
            product.image1 = file_name1  # Update with the new file name
            product.image2 = file_name2
            product.image3 = file_name3

            # Save the updated product object to the database
            product.save()

            # Redirect to the product view page after uploading
            return redirect('viewproductupload')  # Redirect to view uploaded products page

        # If it's a GET request, render the update form with the current product data
        return render(request, 'updateproduct.html', {'product': product})
    
    except Product.DoesNotExist:
        return redirect('/')  # O




def cakes_page(request):
    cakes = Product.objects.filter(types="cakes")  # Adjust based on your model
    return render(request, 'cakes.html', {'cakes': cakes})

def crafts_page(request):
    craft = Product.objects.filter(types="craft")  # Adjust based on your model
    return render(request, 'crafts.html',{'crafts': craft})

def mehandi_page(request):
    meh = Product.objects.filter(types="mehandi").select_related('user')  # Fetch products with related user data
    return render(request, 'mehandi.html', {'mehandi': meh})


def deals(request):
    return render(request,"deals.html")



def place_order(request, product_id):
    # Ensure the user is logged in (checking the session)
    if 'USER_ID' not in request.session:
        return redirect('login')  # Redirect to login page if the user is not logged in

    try:
        product = Product.objects.get(id=product_id)  # Fetch the product
    except Product.DoesNotExist:
        return HttpResponse("Product not found.", status=404)

    if request.method == "POST":
        # Get user details from the session
        user_id = request.session.get('USER_ID')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('login')  # If user doesn't exist, redirect to login page

        # Creating an order
        new_order = order(  # Use lowercase 'order' here
            user=user,
            product=product,
            fullname=request.POST['fullname'],
            address=request.POST['address'],
            phone=request.POST['phone'],
            message=request.POST['message'],
            price=product.offer_price if product.offer_price else product.actual_price,
            quantity=request.POST['quantity']
        )
        new_order.save()

        # Redirect to a success page or another page after order completion
        return redirect('order_confirmation')  # You can replace this with the actual success page URL

    return render(request, 'place_order.html', {'product': product})

def order_confirmation(request):
    return render(request, 'order_confirmation.html')




def my_orders(request):
    # Check if the user is logged in using session
    if 'USER_ID' not in request.session:
        return redirect('login')  # Redirect to login if not logged in

    user_id = request.session.get('USER_ID')

    # Retrieve orders placed by the logged-in user
    user_orders = order.objects.filter(user_id=user_id).select_related('product')

    return render(request, 'my_orders.html', {'orders': user_orders})


def received_orders(request):
    # Check if user is logged in using session
    user_id = request.session.get('USER_ID')

    if not user_id:
        return redirect('login')  # Redirect to login page if user is not logged in

    # Fetch products owned by the logged-in user (seller)
    user_products = Product.objects.filter(user_id=user_id)

    # Get orders placed for these products (but by other users)
    received_orders = order.objects.filter(product__in=user_products).exclude(user_id=user_id)

    return render(request, 'received_orders.html', {'received_orders': received_orders})



def ProfileEdit(request):
    # Get the user based on the username stored in the session
    try:
        tprofileedit = User.objects.get(username=request.session['USERNAME'])
        context = {'tprofileedit': tprofileedit}
        return render(request, "profile.html", context)
    except User.DoesNotExist:
        # Handle if the user does not exist
        return redirect('tlogin')

  
# def ProfileUpdate(request):
#     if request.method == 'POST':
       
#         Name=request.POST["username"]
#         email=request.POST["email"]
#         password=request.POST["tpwd"]
#         phone=request.POST["phone"]
#         role=request.POST["role"]
        
    
#         User.objects.filter(email=request.session['USERNAME']).update(
            
#             username=Name,
#             phone=phone,
#             password=password,
#             email=email,
#             role=role,
            
            
#          )
    
#         return redirect('login')
#     else:
#         return redirect('ProfileEdit')    


def ProfileUpdate(request):
    if request.method == 'POST':
        # Get the data from the form
        Name = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["tpwd"]
        phone = request.POST["phone"]
        role = request.POST["role"]

        # Update the user profile without hashing the password
        try:
            user = User.objects.get(id=request.session['USER_ID'])  # Use USER_ID from session
            user.username = Name
            user.email = email
            user.phone = phone
            user.role = role
            user.password = password  # No hashing, store password as plain text
            user.save()
        except User.DoesNotExist:
            # Handle the case where the user doesn't exist in the database
            return redirect('login')  # Redirect to login if user is not found

        # Redirect to profile page or login after successful update
        return redirect('login')  # Redirect to profile page (adjust URL name as necessary)
    
    else:
        # If the request method is not POST, redirect to the ProfileEdit page
        return redirect('ProfileEdit')


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            otp = str(random.randint(100000, 999999))
            OTPVerification.objects.update_or_create(user=user, defaults={'otp': otp})

            # Send OTP via Email
            send_mail(
                'Password Reset OTP',
                f'Your OTP is: {otp}',
                'your-email@gmail.com',  # Replace with your email
                [email],
                fail_silently=False,
            )
            request.session['reset_email'] = email
            return redirect('verify_otp')
    return render(request, 'forgot_password.html')

def verify_otp(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')

    if request.method == "POST":
        otp = request.POST.get('otp')
        user = User.objects.filter(email=email).first()
        otp_record = OTPVerification.objects.filter(user=user, otp=otp).first()
        if otp_record:
            return redirect('reset_password')
    return render(request,'verify_otp.html')

def reset_password(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')

    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            user = User.objects.filter(email=email).first()
            if user:
                user.password = new_password
                user.save()
                OTPVerification.objects.filter(user=user).delete()
                return redirect('login')
    return render(request,'reset_password.html')



def add_to_wishlist(request, product_id):
    if request.method == "POST":
        # Ensure the user is logged in
        if request.session.get('USER_ID'):
            user = User.objects.get(id=request.session['USER_ID'])

            try:
                # Get the product that the user wants to add to the wishlist
                product = Product.objects.get(id=product_id)

                # Check if the product is already in the user's wishlist
                wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)

                if created:
                    return HttpResponse("Product added to your wishlist.")
                else:
                    return HttpResponse("Product is already in your wishlist.")
            except Product.DoesNotExist:
                return HttpResponse("Product not found.")
        else:
            return redirect('login')  # Redirect to login if the user is not logged in
    else:
        return HttpResponse("Invalid request method.")
    

def view_wishlist(request):
    if 'USER_ID' not in request.session:
        return redirect('login')  # Redirect to login if the user is not logged in

    user_id = request.session['USER_ID']  # Get logged-in user ID from session
    wishlist_items = Wishlist.objects.filter(user_id=user_id).select_related('product')  # Fetch wishlist items

    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


def remove_from_wishlist(request, product_id):
    if 'USER_ID' not in request.session:
        return redirect('login')

    user_id = request.session['USER_ID']
    Wishlist.objects.filter(user_id=user_id, product_id=product_id).delete()
    
    return redirect('view_wishlist')  # Redirect back to the wishlist page


def page(request):
    return render(request,"adm/login.html")

def adLogin(request):
    template = loader.get_template('adm/login.html')
    context = {}
    
    # Hardcoded admin credentials
    admin_username = "liya"
    admin_password = "123"
    
    if request.method == "POST":
        username = request.POST.get('txtUname')
        password = request.POST.get('txtPassword')
        
        # Check hardcoded credentials
        if username == admin_username and password == admin_password:
            request.session['RIZVAN'] = username  # Store session for logged-in admin
            
            # Fetch all users
            allusers = User.objects.all()
            
            # Load the correct template
            template = loader.get_template('adm/home.html')
            
            # Pass context correctly inside render()
            context = {'users': allusers}
            return HttpResponse(template.render(context, request))
        else:
            context = {"error": "Invalid username or password"}

    return HttpResponse(template.render(context, request))


def logout(request): 
 del request.session['RIZVAN'] 
 return render(request, "adm/login.html")

def userlogout(request): 
 del request.session['USERNAME'] 
 return render(request, "login.html")


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")
        user.role = request.POST.get("role")
        user.save()
        return redirect('page')
    return render(request, "adm/edit_user.html", {"user": user})

# Delete User View
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('page')


def product_list(request):
    query = request.GET.get('q')  # Get search query
    products = Product.objects.all()  # Fetch all products by default

    if query:
        products = products.filter(productname__icontains=query)  # Filter products

    return render(request, 'product_list.html', {'products': products, 'query': query})

def add_feedbacks(request):
    return render(request,"add_feedback.html")

def add_feedback(request):
    if 'USER_ID' in request.session:  # Check if user is logged in
        user = User.objects.get(id=request.session['USER_ID'])
        
        if request.method == "POST":
            feedback_text = request.POST.get('feedback')
            Feedback.objects.create(user=user, feedback_text=feedback_text)
            return redirect('view_feedbacks')

        return render(request, "add_feedback.html")
    else:
        return redirect('login')

def view_feedbacks(request):
    if 'USER_ID' in request.session:
        user = User.objects.get(id=request.session['USER_ID'])
        feedbacks = Feedback.objects.filter(user=user)
        return render(request, "view_feedbacks.html", {"feedbacks": feedbacks})
    else:
        return redirect('login')

def edit_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)

    if 'USER_ID' in request.session and request.session['USER_ID'] == feedback.user.id:
        if request.method == "POST":
            feedback_text = request.POST.get('feedback')
            feedback.feedback_text = feedback_text
            feedback.save()
            return redirect('view_feedbacks')

        return render(request, "edit_feedback.html", {"feedback": feedback})
    else:
        return redirect('login')
    
def viewallfeed(request):
    allfeed=Feedback.objects.all()
    return render(request,"viewallfeed.html",{'feed':allfeed})


def delete_feedback(request, feedback_id):
    # Check if the user is logged in and if the user is the owner of the feedback
    if 'USER_ID' in request.session:
        user_id = request.session['USER_ID']
        feedback = get_object_or_404(Feedback, id=feedback_id)

        if feedback.user.id == user_id:  # Check if the feedback belongs to the logged-in user
            feedback.delete()
            return redirect('view_feedbacks')  # Redirect to the page displaying all feedbacks after deletion
        else:
            return HttpResponse("You are not authorized to delete this feedback.", status=403)
    else:
        return redirect('login')  # If not logged in, redirect to the login page