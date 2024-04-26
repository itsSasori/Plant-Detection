from django.shortcuts import render


import os
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
from django.conf import settings


# Create your views here.

# Load CSV data
disease_info = pd.read_csv(os.path.join(settings.BASE_DIR, 'disease_info.csv'), encoding='cp1252')
supplement_info = pd.read_csv(os.path.join(settings.BASE_DIR, 'supplement_info.csv'), encoding='cp1252')

# Load the CNN model
model = CNN.CNN(39)
model.load_state_dict(torch.load(os.path.join(settings.BASE_DIR, "plant_disease_model_1_latest.pt")))
model.eval()

def prediction(image_path, model):
    try:
        image = Image.open(image_path)
        
        # Convert image to RGB if it has more than 3 channels
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        image = image.resize((224, 224))
        input_data = TF.to_tensor(image)
        
        # Check tensor shape after conversion
        print("Input tensor shape after conversion:", input_data.shape)
        
        # Reshape input_data if necessary
        if len(input_data.shape) == 3:
            input_data = input_data.unsqueeze(0)  # Add batch dimension if missing
        
        # Perform prediction
        output = model(input_data)
        output = output.detach().numpy()
        index = np.argmax(output)
        
        return index
    except Exception as e:
        print("Error occurred during prediction:", e)
        return None



def home_page(request):
    context={}
    return render(request,'home.html',context)


def contact(request):
    return render(request,'contact-us.html')


def ai_engine_page(request):
    return render(request,'index.html')


def mobile_device_detected_page(request):
    return render(request,'mobile-device.html')


def submit(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        filename = image.name
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
        
        with open(file_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        # Pass file_path to the prediction function
        pred = prediction(file_path,model)
        
        # Retrieve information based on prediction
        title = disease_info['disease_name'][pred]
        description = disease_info['description'][pred]
        prevent = disease_info['Possible Steps'][pred]
        input_image_url = '/media/uploads/' + filename  # Construct input file URL
        supplement_name = supplement_info['supplement name'][pred]
        supplement_image_url = supplement_info['supplement image'][pred]
        supplement_buy_link = supplement_info['buy link'][pred]

        special_values = [3, 5, 7, 11, 15, 18, 20, 23, 24, 25, 28, 38]
        
        # Prepare context data to pass to the template
        context = {
            'title': title,
            'desc': description,
            'prevent': prevent,
            'image_url': input_image_url,
            'pred': pred,
            'sname': supplement_name,
            'simage': supplement_image_url,
            'buy_link': supplement_buy_link,
            'special_values':special_values
        }
        
        # Render the submit.html template with the context data
        return render(request,'submit.html', context)

    # Render the submit.html template without any context data if the request method is not POST or 'image' is not in request.FILES
    return render(request,'submit.html')


def market(request):
    supplement_images = list(supplement_info['supplement image'])
    supplement_names = list(supplement_info['supplement name'])
    diseases = list(disease_info['disease_name'])
    buy_links = list(supplement_info['buy link'])

    return render(request, 'market.html', {
        'supplement_images': supplement_images,
        'supplement_names': supplement_names,
        'diseases': diseases,
        'buy_links': buy_links,
    })