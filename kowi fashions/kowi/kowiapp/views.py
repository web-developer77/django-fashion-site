from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomerSignupForm, EmployeeSignupForm
from allauth.account.views import SignupView

def index(request):
    return render(request, 'index.html', {'title':'index'})

class MySignupView(SignupView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    redirect_field_name = 'next'
    view_name = 'my_signup'
    success_url = None

    def get_context_name(self, **kwargs):
        ret = super(mySignupView, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret

my_signup = mySignupView.as_view()
