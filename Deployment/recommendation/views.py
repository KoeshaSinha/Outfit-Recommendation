from django.shortcuts import HttpResponse, render, redirect
from recommendation.models import outfit, outfit_image, credentials
from django import forms
from django.http import HttpResponseBadRequest, JsonResponse
import os
from PIL import Image
import io
import numpy as np
import cv2
from tensorflow.keras.preprocessing import image
import tensorflow as tf
from django.conf import settings



def home(request):
    context = {"home_nav_active": "active"}
    return render(request, 'home.html',context)

def user_home(request,username):
    print("user_home" + username)
    if username == None :
        return redirect('login')
    context = {'username': username}
    return render(request, 'user_home.html',context)

def aboutus(request):
    context = {"aboutus_nav_active": "active"}
    return render(request, "aboutus.html",context)

def explore(request):
    context = {"explore_nav_active": "active"}
    return render(request, "explore.html",context)

def tips(request):
    context = {"tips_nav_active": "active"}
    return render(request, "tips.html",context)

def contact(request):
    context = {"contact_nav_active": "active"}
    return render(request, "contact.html",context)


class LoginForm(forms.ModelForm):
    class Meta:
        model = credentials
        fields = ['username', 'Password']

def login(request):
    print("hi")
    if request.method == 'POST':
        form = LoginForm(request.POST)
        try:
            user = outfit.objects.get(username = form.data['username'])
            
            if user.Password == form.data['Password']:
                print("redirect")
                return redirect('user_home',user.username)
            else:
                print("s:"+user.Password+" d:"+form.data['Password'])
        except Exception as ex:
            print(ex)
        print('no-redirect')
        return render(request, "login.html",{'form': form, 'message': "username and password did not match"})
    else:
        form = LoginForm()
    return render(request, "login.html",{'form': form})




class SignupForm(forms.ModelForm):
    class Meta:
        model = outfit
        fields = ['username', 'mobile_no', 'email',  'Password']


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            print("hiii")
            # Redirect to a success page or login page
            return redirect('homepage')
    else:
        form = SignupForm()

    return render(request, 'signup.html',{'form':form})



class UploadForm(forms.ModelForm):
    class Meta:
        model = outfit_image
        fields = ['User_Name', 'Top', 'Bottom', 'Shoes', 'Outerwear', 'Purse']
        widgets = {
            'User_Name': forms.TextInput(attrs={'class': 'form-control'}),
            'Top': forms.FileInput(attrs={'class': "form-control"}),
            'Bottom': forms.FileInput(attrs={'class': "form-control"}),
            'Shoes': forms.FileInput(attrs={'class': "form-control"}),
            'Outerwear': forms.FileInput(attrs={'class': "form-control"}),
            'Purse': forms.FileInput(attrs={'class': "form-control"}),
            }
    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        # Set required to False for Outerwear and Purse fields
        self.fields['Outerwear'].required = False
        self.fields['Purse'].required = False



def upload_images(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_images')  # Redirect to the same page after a successful upload
    else:
        form = UploadForm()

    return render(request, 'upload.html', {'form': form,"upload_image1_nav_active": "active"})
   

class UploadForm2(forms.ModelForm):
    class Meta:
        model = outfit_image
        fields = ['User_Name', 'Dress', 'Shoes', 'Outerwear', 'Purse']



def upload_images2(request):
    if request.method == 'POST':
        form = UploadForm2(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_images2')  # Redirect to the same page after a successful upload
    else:
        form = UploadForm2()

    return render(request, 'upload2.html', {'form': form,"upload_image2_nav_active": "active"})




class UploadForm(forms.ModelForm):
    class Meta:
        model = outfit_image
        fields = ['User_Name', 'Top', 'Bottom', 'Shoes', 'Outerwear', 'Purse']




def preprocess_image(image):
    try:
        print(f"File: {image}")

        # Ensure the uploaded file is an image
        if image is None:
            raise ValueError("No file provided.")

        # Get the path to the "outfit_images" folder
        outfit_images_folder = os.path.join(settings.MEDIA_ROOT, 'outfit_images')

        # Get a list of all image files in the folder
        image_files = os.listdir(outfit_images_folder)

        image_path = os.path.join(outfit_images_folder, os.path.basename(image.name)).replace('\\', '/').replace(' ', '_')

        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        print("preprocessing")

        # Verify that the image is not corrupted
        #img.verify()

        # Resize the image to the desired input size of the model
        new_size =  (224, 224)
        img = cv2.resize(img, new_size)

        # Adjust size as needed
       

        # Convert the image to a numpy array
        img_array = np.asarray(img)
        print(img_array.shape)


        # Normalize the image data
        img_array = img_array / 255.0

        img_array = np.expand_dims(img_array, axis=0)

        print("preprocessing successful")

        return img_array

    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")






from django.shortcuts import render
from .models import outfit_image

import os
import base64
from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image






def encode_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded_string}"






def preprocess_images(file):
    try:
        print(f"File: {file}")

        # Ensure the uploaded file is an image
        if file is None:
            raise ValueError("No file provided.")


        # Read the content of the uploaded file
        content = file.read()


        # Create a BytesIO object and load the image
        img = Image.open(io.BytesIO(content))


        # Verify that the image is not corrupted
        img.verify()

        # Rewind the BytesIO object to the beginning
        file.seek(0)


        # Resize the image to the desired input size of the model
        #img = img.resize((224, 224))  # Adjust size as needed


        print("pre processing")

        # Convert the image to a numpy array
        img_array = np.array(img)

        # Normalize the image data
        img_array = img_array / 255.0

        img_array = np.expand_dims(img_array, axis=0)

        print("pre process successful")

        return img_array

    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")


def predictions(request):
    try:
        # Retrieve the latest OutfitImage instance from the database
        latest_outfit_image = outfit_image.objects.latest('id')
        print(latest_outfit_image)

        # Extract image URLs from the model instance
        top_url = latest_outfit_image.Top.url
        bottom_url = latest_outfit_image.Bottom.url
        shoes_url = latest_outfit_image.Shoes.url
        outerwear_url = latest_outfit_image.Outerwear.url
        purse_url = latest_outfit_image.Purse.url

        print("Top URL:", top_url)
        print("Bottom URL:", bottom_url)
        print("Shoes URL:", shoes_url)
        print("Outerwear URL:", outerwear_url)
        print("Purse URL:", purse_url)

        # Process the images
        processed_image1 = preprocess_image(latest_outfit_image.Top)
        processed_image2 = preprocess_image(latest_outfit_image.Bottom)
        processed_image3 = preprocess_image(latest_outfit_image.Shoes)
        processed_image4 = preprocess_image(latest_outfit_image.Outerwear)
        processed_image5 = preprocess_image(latest_outfit_image.Purse)

        # Calculate compatibility score
        compatibility_score, incompatibility_score = predict_outfit_compatibility(
            request, processed_image1, processed_image2, processed_image3, processed_image4, processed_image5
        )

        # Pass the URLs and scores to the template
        context = {
            'compatibility_score_predictions': compatibility_score,
            'incompatibility_score_predictions': incompatibility_score,
            'top_url': top_url,
            'bottom_url': bottom_url,
            'shoes_url': shoes_url,
            'outerwear_url': outerwear_url,
            'purse_url': purse_url,
        }

        print(context)
        return render(request, 'predictions.html', context)

    except Exception as e:
        return render(request, 'predictions.html', {'error': str(e)})



def predictions2(request):
    try:
        print("Entered")
        # Retrieve the latest OutfitImage instance from the database
        latest_outfit_image = outfit_image.objects.latest('id')
        print(latest_outfit_image)

        # Get the recently saved outfit_images instance
        outfit_instance = outfit_image.objects.latest('id')
        print(outfit_instance)

        # Extract image URLs from the model instance
        dress_url = latest_outfit_image.Dress.url
        shoes_url = latest_outfit_image.Shoes.url
        outerwear_url = latest_outfit_image.Outerwear.url
        purse_url = latest_outfit_image.Purse.url

        print("Dress URL:", dress_url)
        print("Shoes URL:", shoes_url)
        print("Outerwear URL:", outerwear_url)
        print("Purse URL:", purse_url)

        # Process the images
        processed_image1 = preprocess_image(latest_outfit_image.Dress)
        processed_image2 = preprocess_image(latest_outfit_image.Shoes)
        processed_image3 = preprocess_image(latest_outfit_image.Outerwear)
        processed_image4 = preprocess_image(latest_outfit_image.Purse)

        # Calculate compatibility score
        compatibility_score, incompatibility_score = predict_outfit_compatibility2(
            request, processed_image1, processed_image2, processed_image3, processed_image4
        )


        # Store the compatibility score in the database
        outfit_instance.Compatibility_Score = compatibility_score
        outfit_instance.save()



        # Pass the URLs and scores to the template
        context = {
            'compatibility_score_predictions': compatibility_score,
            'incompatibility_score_predictions': incompatibility_score,
            'dress_url': dress_url,
            'shoes_url': shoes_url,
            'outerwear_url': outerwear_url,
            'purse_url': purse_url,
        }

        print(context)
        return render(request, 'predictions2.html', context)

    except Exception as e:
        return render(request, 'predictions2.html', {'error': str(e)})


def predict_outfit_compatibility(request, image1, image2, image3, image4, image5):
    try:

        # Load your model and make predictions as before
        best_model_path = 'C:/Users/KOYESHA/outfit/best_model_4_normal_outfits'

        model = tf.keras.models.load_model(best_model_path)

        # Perform predictions using your model
        predictions = model.predict([image1, image2, image3, image4, image5])

        # Assuming your model outputs a single value for compatibility
        compatibility_score = float(predictions[0])

        incompatibility_score = 1 - compatibility_score

        # You can customize the output format as needed
        response_data = {'Compatible': compatibility_score, 'Incompatible': 1 - compatibility_score}
        print(compatibility_score)
        return compatibility_score, incompatibility_score

    except Exception as e:
        response_data = {'error': str(e)}
        return compatibility_score


def predict_outfit_compatibility2(request, image1, image2, image3, image4):
    try:
        # Load your model and make predictions as before

        best_model_path = 'C:/Users/KOYESHA/outfit/best_model_4_all-body_outfits_lstm'

        model = tf.keras.models.load_model(best_model_path)
        print("hi")

        # Perform predictions using your model
        predictions = model.predict([image1, image2, image3, image4])
        print(predictions)

        if isinstance(predictions, (list, tuple, np.ndarray)):
            # Assuming your model outputs a single value for compatibility
            compatibilityScore2 = float(predictions[0])
        else:
            # Handle the case where predictions may be in a different format
            compatibilityScore2 = float(predictions)

        print(compatibilityScore2)

        incompatibilityScore2 = 1 - compatibilityScore2
       
        return compatibilityScore2, incompatibilityScore2

    except Exception as e:
        response_data = {'error': str(e)}
        return compatibilityScore2

def upload_view(request):
    if request.method == 'POST':
        try:
            image1 = request.FILES['Top']
            image2 = request.FILES['Bottom']
            image3 = request.FILES['Shoes']
            image4 = request.FILES['Outerwear']
            image5 = request.FILES['Purse']


            print(f"Image1: {image1.name}")
            print(f"Image2: {image2.name}")
            print(f"Image3: {image3.name}")
            print(f"Image4: {image4.name}")
            print(f"Image5: {image5.name}")


            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                # Save the form data to the database
                form.save()


            # Get the recently saved outfit_images instance
            outfit_instance = outfit_image.objects.latest('id')

            print(outfit_instance)

            processed_image1 = preprocess_image(image1)
            processed_image2 = preprocess_image(image2)
            processed_image3 = preprocess_image(image3)
            processed_image4 = preprocess_image(image4)
            processed_image5 = preprocess_image(image5)

            compatibility_score, incompatibility_score = predict_outfit_compatibility(request, processed_image1, processed_image2, processed_image3, processed_image4, processed_image5)

            print(compatibility_score)


            # Store the compatibility score in the database
            outfit_instance.Compatibility_Score = compatibility_score
            outfit_instance.save()
           

            return redirect('predictions')
        except Exception as e:
            return render(request, 'predictions.html', {'error': str(e)})

    else:
        form = UploadForm()

    return render(request, 'upload.html', {'form': form})


def upload_view2(request):
    if request.method == 'POST':
        try:
            image1 = request.FILES['Dress']
            image2 = request.FILES['Shoes']
            image3 = request.FILES['Outerwear']
            image4 = request.FILES['Purse']


            print(f"Image1: {image1.name}")
            print(f"Image2: {image2.name}")
            print(f"Image3: {image3.name}")
            print(f"Image4: {image4.name}")


            form = UploadForm2(request.POST, request.FILES)
            if form.is_valid():
                # Save the form data to the database
                form.save()


            return redirect('predictions2')
        except Exception as e:
            return render(request, 'predictions2.html', {'error': str(e)})

    else:
        form = UploadForm2()

    return render(request, 'upload2.html', {'form': form})


            
            



def previous_outfits(request):
    try:
        # Retrieve the user's outfit choices based on User_Id
        # Assuming User_Id is a string field in the model

        latest_outfit_image = outfit_image.objects.latest('id')
        print(latest_outfit_image)

        user_name = latest_outfit_image.User_Name
        print("User Name:", user_name)


        if user_name is not None:
            outfits = outfit_image.objects.filter(User_Name=user_name).order_by('-id')
            outfits = outfits[1:]
            for outfit in outfits:
                print("hi")
                print(f"Outfit ID: {outfit.id}, User Name: {outfit.User_Name}")

            # Pass the outfit data to the template
            context = {'outfits': outfits}
            return render(request, 'previous_outfits.html', context)
        else:
            return HttpResponse("User_Name not found in session.")

    except Exception as e:
        return render(request, 'previous_outfits.html', {'error': str(e)})

def previous_outfits2(request):
    try:

        latest_outfit_image = outfit_image.objects.latest('id')
        print(latest_outfit_image)

        user_name = latest_outfit_image.User_Name
        print("User Name:", user_name)


        if user_name is not None:
            outfits = outfit_image.objects.filter(User_Name=user_name).order_by('-id')
            outfits = outfits[1:]
            for outfit in outfits:
                print(f"Outfit ID: {outfit.id}, User ID: {outfit.User_Name}, score: {outfit.Compatibility_Score}")
            # Pass the outfit data to the template
            context = {'outfits': outfits}
            return render(request, 'previous_outfits.html', context)
        else:
            return HttpResponse("User_Id not found in session.")

    except Exception as e:
        return render(request, 'previous_outfits.html', {'error': str(e)})

