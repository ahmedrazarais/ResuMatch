from django import forms

class UploadFilesForm(forms.Form):
    resume = forms.FileField(
        label="Upload Resume",
        widget=forms.ClearableFileInput(attrs={
            'class': 'block w-full px-4 py-2 border-2 border-purple-600 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500 text-gray-700 bg-white'
        })
    )
    job_ad = forms.FileField(
        label="Upload Job Ad",
        widget=forms.ClearableFileInput(attrs={
            'class': 'block w-full px-4 py-2 border-2 border-purple-600 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500 text-gray-700 bg-white'
        })
    )
