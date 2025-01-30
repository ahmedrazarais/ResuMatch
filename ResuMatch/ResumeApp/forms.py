from django import forms

class ResumeForm(forms.Form):
    full_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'w-full h-10 p-4 border border-purple-300 rounded-md '}))
    gmail = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full h-10 p-4 border border-purple-300 rounded-md'}))
    contact_no = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'w-full h-10 p-4 border border-purple-300 rounded-md'}))
    objective = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full p-4 border border-purple-300 rounded-md', 'rows': 3}))
    skills = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full p-4 border border-purple-300 rounded-md', 'rows': 3}))
    certificates = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full p-4 border border-purple-300 rounded-md', 'rows': 3}))
    interests = forms.CharField(required=False , widget=forms.Textarea(attrs={'class': 'w-full p-4 border border-purple-300 rounded-md', 'rows': 3}))

class WorkExperienceForm(forms.Form):
    company_name = forms.CharField(required=True ,max_length=255, widget=forms.TextInput(attrs={'class': 'w-full h-10 p-4 border border-purple-300 rounded-md'}))
    position = forms.CharField(required=True , max_length=255, widget=forms.TextInput(attrs={'class': 'w-full h-10 p-4 border border-purple-300 rounded-md'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'w-full h-10 p-4 border border-purple-300 rounded-md', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'w-full h-10 p-4 border border-purple-300 rounded-md', 'type': 'date'}), required=False)
    is_current = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'h-5 w-5 p-1'}))
    job_description = forms.CharField(required=False ,widget=forms.Textarea(attrs={'class': 'w-full  p-4 border border-purple-300 rounded-md', 'rows': 3}))

class EducationForm(forms.Form):
    institute_name = forms.CharField(required=True , max_length=255, widget=forms.TextInput(attrs={'class': 'w-full h-10 p-4 border border-purple-300 rounded-md'}))
    degree = forms.CharField(required=True , max_length=255, widget=forms.TextInput(attrs={'class': 'w-full h-10 p-4 border border-purple-300 rounded-md'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'w-full h-10 p-4 border border-purple-300 rounded-md', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'w-full h-10 p-4 border border-purple-300 rounded-md', 'type': 'date'}), required=False)
    is_current = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'h-5 w-5 p-1'}))


