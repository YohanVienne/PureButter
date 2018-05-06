from django import forms

class ProductSearch(forms.Form):
    """ Search product forms """
    product = forms.CharField(max_length=30,
        widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'searchText',
            'value': '',
            'placeholder': 'Entrez un produit',
        }
    ))

class loginConnexion(forms.Form):
    """ Login acces """
    username = forms.CharField(label="Nom d'utilisateur", 
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'usernameInput',
                'value': '',
                'placeholder': 'ex: Paul',
            }
        ))
    password = forms.CharField(label="Mot de passe", 
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'passwordInput',
                'value': '',
                'placeholder': 'Mot de passe',
            }
        ))
