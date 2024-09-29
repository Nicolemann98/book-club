from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.paginator import Paginator

from .models import Product, Category

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
            categories = request.GET['category']. split (',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)


        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(author__icontains=query)
            products = products.filter(queries)

        page_number = request.GET.get('page')

    current_sorting = f'{sort}_{direction}'

    paginator = Paginator(products, 24) # Show 24 products per page
    page_obj = paginator.get_page(page_number)

    context = {
        'products' : products, 
        'search_term' : query,
        'current_categories' : categories,
        'current_sorting' : current_sorting,
        "page_obj": page_obj
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product' : product,
    }

    return render(request, 'products/product_detail.html', context)