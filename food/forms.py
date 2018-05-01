from django import forms

class ProductSearch(forms.Form):
    """ Search product forms """
    product = forms.CharField(max_length=30,
        widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'searchText',
            'placeholder': 'Entrez un produit',
        }
    ))
    