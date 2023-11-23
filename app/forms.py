from django import forms
from .models import Status, Category, Product
import hashlib
from django.utils import timezone
import requests
from testfp.settings import ONLINE_PRODUCTS_URL


class ProductForm(forms.ModelForm):
    name = forms.CharField(label='Product Name', max_length=100, widget=forms.TextInput(attrs={'class': "input", "placeholder": "Product Name"}))    
    price = forms.CharField(label='Product Price', max_length=100, widget=forms.NumberInput(attrs={'class': "input", "placeholder": "Product Price"}))    
    category = forms.ModelChoiceField(label='Product Category', queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'input'}))
    status = forms.ModelChoiceField(label='Product Status', queryset=Status.objects.all(), widget=forms.Select(attrs={'class': 'input'}))
    
    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'category',
            'status',
        ]


class GetOnlineProductForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "input", "placeholder": "Online Username"}))
    data = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        
        current_time_utc = timezone.now()
        current_time_local = current_time_utc.astimezone(timezone.get_current_timezone())
        formatted_date = current_time_local.strftime("%d-%m-%y")

        password_plain = f'bisacoding-{formatted_date}'.encode('utf-8')
        md5 = hashlib.md5()
        md5.update(password_plain)
        password_md5 = md5.hexdigest()

        try:
            response_products = requests.post(ONLINE_PRODUCTS_URL, data={
                'username': username,
                'password': password_md5
            })

            if response_products.status_code != 200:
                self.add_error('username', 'Username not identified!!')

            self.data = response_products.json().get('data')

        except Exception as e:
            self.add_error('username', 'Username not identified!!')
        
    def save(self):
        if self.data:
            category_dict = {category.name: category.id for category in Category.objects.all()}
            status_dict = {status.name: status.id for status in Status.objects.all()}

            new_products = []
            try:
                for item in self.data:
                    if item['kategori'] not in category_dict.keys():
                        category = Category(name=item['kategori'])
                        category.save()

                        category_dict[category.name] = category.id

                        category_id = category.id

                    else:
                        category_id = category_dict[item['kategori']]

                    if item['status'] not in status_dict.keys():
                        status = Status(name=item['status'])
                        status.save()

                        status_dict[status.name] = status.id

                        status_id = status.id
                    else:
                        status_id = status_dict[item['status']]

                    if not Product.objects.filter(
                        name=item['nama_produk'],
                        category_id=category_id
                    ).exists():
                        new_products.append(
                            Product(
                                name=item['nama_produk'],
                                price=item['harga'],
                                category_id=category_id,
                                status_id=status_id
                            )
                        )
                
                if new_products:
                    Product.objects.bulk_create(new_products)

                    return len(new_products)

            except Exception as e:
                return e

        return            