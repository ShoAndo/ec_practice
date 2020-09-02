from django.test import TestCase
from django.urls import reverse
from catalogue.models import Category, Product
from catalogue.forms import ProductSearchForm

class TestProductSearchForm(TestCase):
  def test_filter_product_name(self):
    Product.objects.create(name='冷凍パスタ', price=800)
    Product.objects.create(name='冷凍餃子', price=100)
    Product.objects.create(name='煮込みグラタン', price=700)

    form = ProductSearchForm({'name': '冷凍'})
    actual = form.filter_products(Product.object.order_by('name'))
    self.assertEqual(actual[0].name, '冷凍パスタ')
    self.assertEqual(actual[1].name, '冷凍餃子')

  def test_filter_products_price_max(self):
    Product.objects.create(name='煮込みグラタン', price=700)
    Product.objects.create(name='ドリア', price=701)

    form = ProductSearchForm({'price_max': 700})
    actual = form.filter_products(Product.objects.all())
    self.assertEqual(len(actual), 1)
    self.assertEqual(actual[0].name, '煮込みグラタン')

  def test_filter_products_category(self):
    category = Category.objects.create(id=1, name='食品')
    Product.objects.create(name='煮込みグラタン', price=700, category=category)
    Product.objects.create(name='おしゃれスカジャン', price=8900)

    form = ProductSearchForm({'category': 1})
    actual = form.filter_products(Product.objects.all())
    self.assertEqual(len(actual), 1)
    self.assertEqual(actual[0].name, '煮込みグラタン')

  def test_filter_invalid(self):
    Product.objects.create(name='おしゃれスカジャン', price=8900)
    Product.objects.create(name='煮込みグラタン', price=700)

    form = ProductSearchForm({'price_max': '無効'})
    actual = form.filter_products(Product.objects.order_by('name'))
    self.assertEqual(len(actual), 2)
    self.assertEqual(actual[0].name, 'おしゃれグラタン' )
    self.assertEqual(actual[0].name, '煮込みグラタン')
