from django.template.response import TemplateResponse
from django.http import HttpResponse
from .models import Product
from .forms import ProductEditForm
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def product_list(request):
  products = Product.objects.order_by('name')
  paginator = Paginator(products, 5)
  page = request.GET.get('page', 1)
  try:
      products = paginator.page(page)
  except (EmptyPage, PageNotAnInteger):
      products = paginator.page(1)
  return TemplateResponse(request, 'catalogue/product_list.html',
                            {'products': products})


def product_detail(request, product_id):
  try:
    product = Product.objects.get(id=product_id)
  except Product.DoesNotExist:
    raise Http404
  return TemplateResponse(request, 'catalogue/product_detail.html', { 'product': product })

def product_edit(request, product_id):
  try:
    product = Product.objects.get(id = product_id)
  except Product.DoesNotExist:
    raise Http404

  if request.method == 'POST':
    form = ProductEditForm(request.POST, instance=product)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('product_detail', args=(product.id,)))

  else:
    form = ProductEditForm()

  return TemplateResponse(request, 'catalogue/product_edit.html', { 'form': form, 'product': product })


def product_delete(request, product_id):
  try:
    product = Product.objects.get(id=product_id)
  except Product.DoesNotExist:
    raise Http404

  if request.method == 'POST':
    product.delete()
    return HttpResponseRedirect(reverse('product_list'))
  else:
    return TemplateResponse(request, 'catalogue/product_delete.html', { 'product': product })
