# from django import forms
# import requests
# from maker_orders.models import User, Order
# from django.core.exceptions import ValidationError
# requests.get('https://yandex.ru')
# #
# # class UserCreateForm(forms.ModelForm):
# #
# #     class Meta:
# #         model = User
# #         fields = ['first_name', 'second_name', 'mail', 'phone_number']
# #
# #         widgets = {
# #             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
# #             'second_name': forms.TextInput(attrs={'class': 'form-control'}),
# #             'mail': forms.TextInput(attrs={'class': 'form-control'}),
# #             'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
# #         }
# #
# #     def clean_phone_number(self):
# #         phone = self.cleaned_data['phone_number']
# #         if User.objects.filter(phone_number=phone).count():
# #             raise ValidationError(f'Номер {phone} уже зарегистрирован')
# #         return phone
#
#
# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['id_product', 'region', 'city', 'street',
#                   'house', 'search_request', 'size', 'flat', 'private_house']
#
#         widgets = {
#             'id_product': forms.TextInput(attrs={'class': 'form-control'}),
#             'region': forms.TextInput(attrs={'class': 'form-control'}),
#             'city': forms.TextInput(attrs={'class': 'form-control'}),
#             'street': forms.TextInput(attrs={'class': 'form-control'}),
#             'house': forms.TextInput(attrs={'class': 'form-control'}),
#             'search_request': forms.TextInput(attrs={'class': 'form-control'}),
#             'size': forms.TextInput(attrs={'class': 'form-control'}),
#             'flat': forms.TextInput(attrs={'class': 'form-control'}),
#             # 'private_house': forms.CheckboxInput(attrs={'class': 'form-control'}),
#         }
#
#
# class LikeCreateForm(forms.Form):
#     pass
#
#
# #
# # class AskQuestionsForm(forms.Form):
# #     search_request = forms.CharField(max_length=255)
# #     product_id = forms.CharField(max_length=255)
# #     question = forms.CharField(max_lengh=2500)
#
#
#     # def save()
#
# # class OrderForm(forms.Form):
# #     id_product = forms.CharField(max_length=50)
# #     region = forms.CharFiels(max_length=255)
# #     city = forms.CharField(max_length=255)
# #     street = forms.CharField(max_length=255)
# #     house = forms.CharField(max_length=255)
# #     search_request = forms.CharField(max_length=255)
# #     size = forms.CharField(max_length=255)
# #     flat = forms.CharField()
# #     private_house = forms.CharField(max_length=255)
# #
# #
# #     def save(self):
# #