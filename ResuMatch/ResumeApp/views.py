

from django.shortcuts import render
from .forms import ResumeForm, WorkExperienceForm, EducationForm
from django.http import HttpResponseRedirect
from fpdf import FPDF
from django.http import HttpResponse
from django.shortcuts import render, redirect  



def create_resume(request):
    if request.method == 'POST':
        resume_form = ResumeForm(request.POST)
        
        if resume_form.is_valid():
                      
            work_experience_data = request.session.get('work_experience_data', [])
            education_data = request.session.get('education_data', [])
   
            request.session['work_experience_data'] = []
            request.session['education_data'] = []

            # Writing the data to a file 
            with open('resume.txt', 'w') as f:
                f.write(f"{resume_form.cleaned_data['full_name']}\n")
                f.write("abc road, Karachi.\n")
                f.write(f"{resume_form.cleaned_data['gmail']}\n")
                f.write(f"{resume_form.cleaned_data['contact_no']}\n")
                f.write("\n")
                
                objective = " ".join(resume_form.cleaned_data['objective'].splitlines()).strip()
                f.write(f"{objective}\n")
                f.write("\n")

                # Work Experience Section
                f.write("Work Experience\n")
                for work in work_experience_data:
                    f.write(f"\n{work['position']}\n")
                    f.write(f"{work['company_name']}\n")
                    f.write(f"{work['start_date']} - {work['end_date']}\n")
                f.write("\n")  # Blank line after work experience

                # Education Section
                f.write("Education\n")
                for edu in education_data:

                    f.write(f"\n{edu['institute_name']}\n")
                    f.write(f"\n{edu['degree']}\n")
                    f.write(f"{edu['start_date']} to {edu['end_date']}\n")
                f.write("\n")  # Blank line after education

                # Skills Section
                f.write("Skills\n")
                for skill in resume_form.cleaned_data['skills'].splitlines():
                    f.write(f"{skill.strip()}\n")
                f.write("\n")  # Blank line after skills

                # Certificates Section
                f.write("Certificates\n")
                for certificate in resume_form.cleaned_data['certificates'].splitlines():
                    f.write(f"{certificate.strip()}\n")
                f.write("\n")  # Blank line after certificates

                # Interests Section
                f.write("Interests\n")
                for interest in resume_form.cleaned_data['interests'].splitlines():
                    f.write(f"{interest.strip()}\n")

         
            return redirect('download_resume')   
            
        else:
            return render(request, 'ResumeApp/create_cv_home.html', {'resume_form': resume_form})
    
    else:
        
        resume_form = ResumeForm()

    # Collect work experience and education data from session
    work_experience_data = request.session.get('work_experience_data', [])
    education_data = request.session.get('education_data', [])
    
    return render(request, 'ResumeApp/create_cv_home.html', {'resume_form': resume_form, 'work_experience_data': work_experience_data, 'education_data': education_data})








def create_work_experience(request):
    if request.method == 'POST':
        work_experience_form = WorkExperienceForm(request.POST)

        if work_experience_form.is_valid():
            # Get the cleaned data from the form
            cleaned_data = work_experience_form.cleaned_data

        
            if cleaned_data.get('start_date'):
                cleaned_data['start_date'] = cleaned_data['start_date'].strftime('%Y-%m-%d')
            if cleaned_data.get('end_date'):
                cleaned_data['end_date'] = cleaned_data['end_date'].strftime('%Y-%m-%d')

         
            work_experience_data = request.session.get('work_experience_data', [])
            work_experience_data.append(cleaned_data)

           
            request.session['work_experience_data'] = work_experience_data

            
            return HttpResponseRedirect('/ResumeApp/create/')

        else:
            return render(request, 'ResumeApp/create_work_experience.html', {'work_experience_form': work_experience_form})
    
    else:
        work_experience_form = WorkExperienceForm()

    return render(request, 'ResumeApp/create_work_experience.html', {'work_experience_form': work_experience_form})


def create_education(request):
    if request.method == 'POST':
        education_form = EducationForm(request.POST)

        if education_form.is_valid():
            # Get the cleaned data from the form
            cleaned_data = education_form.cleaned_data

          
            if cleaned_data.get('start_date'):
                cleaned_data['start_date'] = cleaned_data['start_date'].strftime('%Y-%m-%d')
            if cleaned_data.get('end_date'):
                cleaned_data['end_date'] = cleaned_data['end_date'].strftime('%Y-%m-%d')

       
            education_data = request.session.get('education_data', [])
            education_data.append(cleaned_data)

          
            request.session['education_data'] = education_data

            # Redirect to the create_resume view
            return HttpResponseRedirect('/ResumeApp/create/')

        else:
            return render(request, 'ResumeApp/create_education.html', {'education_form': education_form})
    
    else:
        education_form = EducationForm()

    return render(request, 'ResumeApp/create_education.html', {'education_form': education_form})


# Download the resume as a PDF file
def download_resume(request):
    return render(request,"ResumeApp/resume_download.html")





from fpdf import FPDF
from django.http import HttpResponse

def convert_to_pdf(request):
    # Read the contents of the text file
    with open('resume.txt', 'r') as f:
        text = f.read()

    # Split the content into lines and define the section headings
    lines = text.split('\n')

    # Create a PDF object
    pdf = FPDF()

    # Set page margins
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    pdf.set_top_margin(10)

    # Add a page
    pdf.add_page()

    # Set font for the body text
    pdf.set_font('Times', '', 10)

   
    for line in lines:
        
        if line.strip() in ["Work Experience", "Education", "Skills", "Certificates", "Interests"]:
            # Set the font to bold for headings
            pdf.set_font('Times', 'B', 12)
            pdf.cell(0, 10, line, ln=True)

            
            pdf.set_draw_color(192, 192, 192) 
            pdf.line(15, pdf.get_y(), 200, pdf.get_y()) 
            pdf.ln(1)  

        
            pdf.set_font('Times', '', 10)

        else:
            
            pdf.multi_cell(0, 6, line)

    # Save the PDF file
    pdf_file = 'resume.pdf'
    pdf.output(pdf_file)

    # Return the PDF file as an attachment
    response = HttpResponse(open(pdf_file, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    return response

