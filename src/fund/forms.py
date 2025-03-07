from django import forms


class CSVUploadForm(forms.Form):
    csv_upload = forms.FileField()
