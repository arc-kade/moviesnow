from django import forms
from actors.models import Actors


class ActorForm(forms.ModelForm):
    class Meta:
        model=Actors
        fields=["name","country","dob","about","portrait"]
        labels = {
            "name":"Actor name",
            "country":"Country",
            "about": "About",
            "dob":"Date of Birth",
            "portrait": "Photo",
        }

        widgets ={
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Actor name"
            }),
            "country": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Actor Nationality"
            }),
            "about": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Write a short biography",
                "rows":5,
            }),
            "dob": forms.DateInput(
                attrs={"class": "form-control", type:"date"},
                format="%Y-%m-$d"
            ),
            "portrait": forms.ClearableFileInput(attrs={
                "class":"form-control",
                "accept":"image/*",
            }),
        }