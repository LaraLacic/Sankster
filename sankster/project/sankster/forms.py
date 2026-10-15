from django import forms
from .models import MenuItem, OrderItem, CustomUser

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price']

class OrderItemForm(forms.ModelForm): 
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']

    menu_item = forms.ModelChoiceField(queryset=MenuItem.objects.all())
    quantity = forms.IntegerField(min_value=1, initial=1)

class EditStaffForm(forms.ModelForm):
    class Meta: 
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'is_active']
        widgets = {
            'role': forms.Select(choices=CustomUser.ROLE_CHOICES),
        }

class CreateStaffForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user