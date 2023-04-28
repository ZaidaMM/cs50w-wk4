from django import forms
from .models import Category

class NewListingForm(forms.Form):
    title = forms.CharField(     
        label="New Listing", 
        required=True,
        widget=forms.TextInput(attrs={
          "placeholder": "Title", 
          "class":"form-control"
        }))
    description = forms.CharField(      
        label="Description", 
        required=True,
        widget=forms.Textarea(attrs={
          "cols":10, 
          "rows":3, 
          "placeholder": "Description", 
          "class":"form-control"
        }))
    starting_bid = forms.DecimalField(       
        label="Price £",
        required=True,
        widget=forms.TimeInput(attrs={
          "placeholder": "Price",
          "class":"form-control"
        }))
    image_url = forms.CharField(
        
        label="Image URL", 
        required=False,
        widget=forms.TextInput(attrs={
          "placeholder": "Image URL", 
          "class":"form-control"
        }))
    category = forms.ModelChoiceField(        
        queryset=Category.objects.all(),
        empty_label="Choose a Category",
        widget=forms.Select(attrs={"class":"form-control"})
    )
