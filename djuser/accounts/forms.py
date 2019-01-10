from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField,PasswordChangeForm
from django.contrib.auth import authenticate
from .models import User
# SOME_CHOICES=(
#     ('is_doctor','Doctor'),
#     ('is_medical','Medical'),
#     ('is_laboratorist','Laboratorist'),
#     ('is_operator','Operator'),
#     )

class UserLoginForm(forms.Form):
    email = forms.CharField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))


    def clean(self,*args,**kwargs):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        # the_user = authenticate(name=name,password=password)
        # if not the_user:
        #     raise forms.ValidationError('invalid credentials')
        user_obj=User.objects.filter(email=email).first()
        if not user_obj:
            raise forms.ValidationError('invalid Email')
        else:
            if not user_obj.check_password(password):
                raise forms.ValidationError('invalid Password')
        
        # return super(UserLoginForm,self).clean(*args, **kwargs)

    # def clean_username(self):
    #     name=self.cleaned_data.get('name')
    #     user_qs=User.objects.filter(name=name).exist()
    #     if not user_qs:
    #         raise forms.ValidationError('invalid credentials')
    #     return name


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    email = forms.CharField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    name = forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    is_laboratorist= forms.BooleanField(label='Is_laboratorist',required=False)
    is_doctor=forms.BooleanField(label='Is_doctor',required=False)
    is_medical=forms.BooleanField(label='Is_medical',required=False)
    is_operator=forms.BooleanField(label='Is_operator',required=False)
    is_admin=forms.BooleanField(label='Is_admin',required=False)
   

    class Meta:
        model = User
        fields = ('email', 'name', 'is_operator','is_doctor', 'is_medical','is_laboratorist', 'is_admin')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # password = ReadOnlyPasswordHashField()
    email = forms.CharField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    name = forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'name')

    # def clean_password(self):
    #     # Regardless of what the user provides, return the initial value.
    #     # This is done here, rather than on the field, because the
    #     # field does not have access to the initial value
    #     return self.initial["password"]