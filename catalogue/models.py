from django.db import models

class Category(models.Model):
  name = models.CharField('カテゴリー名', max_length=32)

  def __str__(self):
    return self.name

class Product(models.Model):
  category = models.ForeignKey(Category, null=True, blank=False, on_delete=models.SET_NULL)
  name = models.CharField('名前', max_length=128)
  price = models.PositiveIntegerField('値段')

  def __str__(self):
    return self.name