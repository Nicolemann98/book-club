from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.db.models.functions import Lower
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Product, Category
from .forms import ProductForm

from datetime import timedelta

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and searches """

    products = Product.objects.all()

    query = None
    categories = None
    sort = None
    direction = None
    page_number = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            if sortkey == 'category':
                sortkey = 'category__name'

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(author__icontains=query)
            products = products.filter(queries)

        if 'newer-than' in request.GET:
            days_old = int(request.GET['newer-than'])
            days_ago = timezone.now() - timedelta(days=days_old)

            products = products.filter(creation_date__gt=days_ago)

        if 'deals' in request.GET:
            products = products.filter(
                old_price__isnull=False,
                price__lt=F('old_price')
            )

        if 'clearance' in request.GET:
            products = products.filter(is_clearance=True)

        page_number = request.GET.get('page')

    current_sorting = f'{sort}_{direction}'

    paginator = Paginator(products, 24)  # Show 24 products per page
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        "page_obj": page_obj
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to add product. Please ensure the form is valid.'
            )
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to update product. Please ensure the form is valid.'
            )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
