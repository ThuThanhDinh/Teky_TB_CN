from django.shortcuts import render
from django.views.generic import CreateView
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
class CustomUserCreationForm(UserCreationForm):
    age = forms.IntegerField(label='Tuổi',min_value = 0, required=True)
    sex = forms.ChoiceField(label= 'Giới tính',choices=((0, "Nữ"), (1, "Nam"), (2, "Không xác định")), required=True)
    address = forms.CharField(label= 'Địa chỉ',max_length=225,required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('age', 'sex', 'address')


    def save(self, commit=True):
        user = super().save(commit = False)
        user.age = self.cleaned_data['age']
        user.sex = self.cleaned_data['sex']
        user.address = self.cleaned_data['address']
        if commit:
            user.save()
        return user
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
