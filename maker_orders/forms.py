from django import forms
from maker_orders.models import User

#
# class UserForm(forms.Form):
#     first_name = forms.CharField(max_length=50)
#     second_name = forms.CharField(max_length=50)
#     mail = forms.CharField(max_length=50)
#     phone_number = forms.CharField(max_length=12)
#
#     def save(self):
#         new_user = User.objects.create(first_name=self.cleaned_data['first_name'],
#                                        second_name=self.cleaned_data['first_name'],
#                                        mail=self.cleaned_data['mail'],
#                                        phone_number=self.cleaned_data['phone_number'],
#                                        )
#         return new_user
#
#
# class AskQuestionsForm(forms.Form):
#     search_request = forms.CharField(max_length=255)
#     product_id = forms.CharField(max_length=255)
#     question = forms.CharField(max_lengh=2500)


    # def save()


