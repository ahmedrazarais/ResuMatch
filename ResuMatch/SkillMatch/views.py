import os
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import UploadFilesForm
import io
import fitz
import easyocr
from PIL import Image
import re
import spacy
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
from .models import Raw_Data



# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Load BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Define folder paths for saving files
RESUME_UPLOAD_FOLDER = os.path.join(settings.MEDIA_ROOT, 'resumes')
JOB_AD_UPLOAD_FOLDER = os.path.join(settings.MEDIA_ROOT, 'job_ads')

def upload_resume(request):
    if request.method == "POST":
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded files
            resume = request.FILES['resume']
            job_ad = request.FILES['job_ad']

            # Ensure the folders exist
            if not os.path.exists(RESUME_UPLOAD_FOLDER):
                os.makedirs(RESUME_UPLOAD_FOLDER)
            if not os.path.exists(JOB_AD_UPLOAD_FOLDER):
                os.makedirs(JOB_AD_UPLOAD_FOLDER)

            # Delete all existing files in the respective folders
            for file in os.listdir(RESUME_UPLOAD_FOLDER):
                file_path = os.path.join(RESUME_UPLOAD_FOLDER, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

            for file in os.listdir(JOB_AD_UPLOAD_FOLDER):
                file_path = os.path.join(JOB_AD_UPLOAD_FOLDER, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

            # Save the new files in their respective folders with original names
            resume_path = os.path.join(RESUME_UPLOAD_FOLDER, resume.name)
            job_ad_path = os.path.join(JOB_AD_UPLOAD_FOLDER, job_ad.name)

            with open(resume_path, 'wb+') as destination:
                for chunk in resume.chunks():
                    destination.write(chunk)

            with open(job_ad_path, 'wb+') as destination:
                for chunk in job_ad.chunks():
                    destination.write(chunk)

            return redirect("analyze_now")
    else:
        form = UploadFilesForm()
    
    return render(request, 'SkillMatch/upload_resume.html', {'form': form})



def analyze_now(request):
    return render(request, 'SkillMatch/analyze_now.html')









# ocr
reader = easyocr.Reader(['en']) 

def analysis_results(request):
    text_job_ad = ""
    text_resume = ""

    
    if len(os.listdir(JOB_AD_UPLOAD_FOLDER)) == 0:
        print("No job ad uploaded")

    else:
        # Get the job ad file path and its extension
        job_ad_file = os.listdir(JOB_AD_UPLOAD_FOLDER)[0]
        job_ad_file_path = os.path.join(JOB_AD_UPLOAD_FOLDER, job_ad_file)
        job_ad_file_extension = job_ad_file.split('.')[-1].lower()

        if job_ad_file_extension in ['jpg', 'jpeg', 'png']:
            # Perform OCR on the job ad image using EasyOCR
            image = Image.open(job_ad_file_path)
            text_job_ad = extract_text_with_easyocr(image)

        elif job_ad_file_extension == 'pdf':
            # Perform OCR on the job ad PDF
            text_job_ad = extract_text_from_pdf(job_ad_file_path)
        else:
            print("Unsupported file format for job ad")

   
    if len(os.listdir(RESUME_UPLOAD_FOLDER)) == 0:
        print("No resume uploaded")

    else:
        
        resume_file = os.listdir(RESUME_UPLOAD_FOLDER)[0]
        resume_file_path = os.path.join(RESUME_UPLOAD_FOLDER, resume_file)
        resume_file_extension = resume_file.split('.')[-1].lower()

        if resume_file_extension == 'pdf':
            # Extract text from the resume PDF
            text_resume = extract_text_from_pdf(resume_file_path)
            # text_resume = clean_and_split_text(text_resume)
        else:
            print("Unsupported file format for resume")

    Raw_Data.objects.all().delete()

    
    raw_data = Raw_Data(job_ad=text_job_ad, resume=text_resume)
    raw_data.save()

    
    # Preprocess the texts
    resume_processed = preprocess_text(text_resume)
    job_processed = preprocess_text(text_job_ad)

    
        # Get BERT embeddings for the processed texts
    try:
        resume_embedding = get_bert_embedding(resume_processed, tokenizer, model)
        job_embedding = get_bert_embedding(job_processed, tokenizer, model)

        # Calculate cosine similarity
        similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]

        if similarity >= 0.9:
             result_message = "Congratulations! You are an excellent match for the job requirements. Just a few minor improvements and you're good to go!"
       
        
        else:
            result_message = "Unfortunately, you are not a strong match for the job requirements. Consider revising your resume or acquiring more relevant skills."

        return render(request, 'SkillMatch/analysis_results.html', {
            'similarity': round(similarity, 2),
            'result_message': result_message
        })

    except Exception as e:
        
        return redirect("upload_resume")
       
    



def extract_text_with_easyocr(image):
   
    result = reader.readtext(image)
    text = ""
    for detection in result:
        text += detection[1] + "\n" 
    return text





def extract_text_from_pdf(pdf_path):
    text = ""
    
    try:
       
        pdf_text = ""
        pdf_document = fitz.open(pdf_path)
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            pdf_text += page.get_text()
        if pdf_text.strip():  
            return pdf_text

       # OCR if direct text extraction fails
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            page_text = extract_text_with_easyocr(img)
            text += page_text + "\n\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")

    return text




def preprocess_text(text):
    # Lowercase the text
    text = text.lower()
    
    # Remove special characters, digits, and extra spaces
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(' +', ' ', text)
    
   
    doc = nlp(text)
    

    processed_text = ' '.join([token.lemma_ for token in doc if not token.is_stop and len(token.text) > 2])
    
    return processed_text.strip()





# Get BERT embeddings for the text
def get_bert_embedding(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    outputs = model(**inputs)
    cls_embedding = outputs.last_hidden_state[:, 0, :]  
    return cls_embedding.detach().numpy()

