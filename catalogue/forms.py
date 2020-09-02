from django import forms
from .models import Product

class ProductEditForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = ('name', 'price')

class ProductSearchForm(forms.ModelForm):
  name = forms.CharField(label="商品名", required=False)
  price_min = forms.IntegerField(label="最低価格",min_value=1, required=False)
  price_max = forms.IntegerField(label="最高価格", min_value=1, required=False)

  class Meta:
    model = Product
    fields = ('category',)

  def filter_products(self, products):
    if not self.is_valid():
      return products

    name = form.cleaned_data.get('name')
    price_min = form.cleaned_data.get('price_min')
    price_max = form.cleaned_data.get('price_max')
    category_id = form.cleaned_data.get('category')
    if name:
      products = products.filter(name__contains=name)
    if price_min:
      products = products.filter(price__gte=price_min)
    if price_max:
      price_max = products.filter(price__lte=price_max)
    if category_id:
      products = products.filter(category_id=category_id)
    return products

