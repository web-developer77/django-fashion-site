from allauth.account.forms import SignupForm
from django import forms
gen = (
    ('M','Male'),
    ('F','Female'),
    ('O','Prefer not to say'),
)
skin = (
    ('1','Fair'),
    ('2','Olive'),
    ('3','Brown'),
    ('4','Black'),
)
hair = (
    ('black','black'),
    ('brown','brown'),
    ('Blond','Blonde'),
    ('Red','Red'),
    ('White/Gray','White/Gray'),
)
class CustomerSignupForm(SignupForm):
    gender = forms.ChoiceField(required=True,label='Gender',choices=gen)
    skintone = forms.ChoiceField(required=False,choices=skin,label='Skin Tone')
    height = forms.CharField(required=False,max_length=75,label='Height in CM')
    weight = forms.CharField(required=False,max_length=75,label='Weight in KG')
    haircolors = forms.ChoiceField(required=False,choices=hair,label='Hair Color')
    mobno = forms.IntegerField(required=False,label='Mobile Number')
    age = forms.IntegerField(required=False,label='Age')

    def signup(self,request,user):
        user.gender = self.cleaned_data['gender']
        user.skintone = self.cleaned_data['skintone']
        user.height = self.cleaned_data['height']
        user.weight = self.cleaned_data['weight']
        user.haircolors = self.cleaned_data['haircolors']
        user.mobno = self.cleaned_data['mobno']
        user.age = self.cleaned_data['age']
        user.is_customer = True
        user.save()
        return user

class EmployeeSignupForm(SignupForm):
    gender = forms.ChoiceField(required=True,label='Gender',choices=gen)
    mobno = forms.IntegerField(required=False,label='Mobile Number')
    age = forms.IntegerField(required=False,label='Age')

    def signup(self,request,user):
        user.gender = self.cleaned_data['gender']
        user.mobno = self.cleaned_data['mobno']
        user.age = self.cleaned_data['age']
        user.is_employee = True
        user.save()
        return user