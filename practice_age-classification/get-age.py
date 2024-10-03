import requests
import torch
from io import BytesIO
from PIL import Image
from transformers import ViTImageProcessor, ViTForImageClassification
import streamlit as st

@st.cache_resource
def get_model_transformers():
    model = ViTForImageClassification.from_pretrained('nateraw/vit-age-classifier')
    transforms = ViTImageProcessor.from_pretrained('nateraw/vit-age-classifier')
    return model, transforms

st.title("나이를 예측해봅시다!")

# # Get example image from official fairface repo + read it in as an image
# r = requests.get('https://github.com/dchen236/FairFace/blob/master/detected_faces/race_Asian_face0.jpg?raw=true')
# im = Image.open(BytesIO(r.content))
uploaded_file = st.file_uploader("나이를 예측할 사람의 이미지를 업로드하세요.", type=["jpg", "jpeg", "png", 'gif', 'webp'])
if uploaded_file:
    #st.write(f'업로드된 파일 이름: {uploaded_file}')
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

if uploaded_file:
    # Init model, transforms
    model, transforms = get_model_transformers()
    im = Image.open(uploaded_file)
    

    # Transform our image and pass it through the model
    inputs = transforms(im, return_tensors='pt')
    output = model(**inputs)

    # Predicted Class probabilities
    proba = output.logits.softmax(1)

    values, indices = torch.topk(proba, k=5)

    result_dict = {model.config.id2label[i.item()]: v.item() for i, v in zip(indices.numpy()[0], values.detach().numpy()[0])}
    first_result = list(result_dict.keys())[0]
    
    st.header('결과')
    st.subheader(f'예측된 나이는 {first_result} 입니다')
    
    for key, value in result_dict.items():
        st.write(f'{key}: {value * 100:.2f}%')

    print(f'predicted result:{result_dict}')
    print(f'first_result: {first_result}')