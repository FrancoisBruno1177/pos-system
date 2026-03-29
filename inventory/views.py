from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, SupplierForm, ProductForm
from .models import Category, Supplier, Product


def inventory_access_required(user):
    return user.is_authenticated and (
        user.is_superuser or user.role in ["SUPER_ADMIN", "ADMIN", "MANAGER"]
    )


@login_required
def inventory_dashboard(request):
    if not inventory_access_required(request.user):
        messages.error(request, "You are not allowed to access inventory.")
        return redirect("dashboard")

    products = Product.objects.select_related("category", "supplier").all()
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    low_stock_products = products.filter(quantity__lte=F("low_stock_threshold"))

    context = {
        "total_products": products.count(),
        "active_products": products.filter(is_active=True).count(),
        "total_categories": categories.count(),
        "total_suppliers": suppliers.count(),
        "low_stock_count": low_stock_products.count(),
        "low_stock_products": low_stock_products[:5],
    }
    return render(request, "inventory/dashboard.html", context)


@login_required
def product_list(request):
    if not inventory_access_required(request.user):
        messages.error(request, "You are not allowed to access products.")
        return redirect("dashboard")

    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()
    supplier_id = request.GET.get("supplier", "").strip()
    stock_filter = request.GET.get("stock", "").strip()

    products = Product.objects.select_related("category", "supplier").all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(description__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    if supplier_id:
        products = products.filter(supplier_id=supplier_id)

    if stock_filter == "low":
        products = products.filter(quantity__lte=F("low_stock_threshold"))
    elif stock_filter == "in":
        products = products.filter(quantity__gt=0)
    elif stock_filter == "out":
        products = products.filter(quantity=0)

    context = {
        "products": products,
        "categories": Category.objects.filter(is_active=True),
        "suppliers": Supplier.objects.filter(is_active=True),
        "query": query,
        "selected_category": category_id,
        "selected_supplier": supplier_id,
        "stock_filter": stock_filter,
    }
    return render(request, "inventory/product_list.html", context)


@login_required
def product_create(request):
    if not inventory_access_required(request.user):
        messages.error(request, "You are not allowed to create products.")
        return redirect("dashboard")

    form = ProductForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        product.created_by = request.user
        product.save()

        messages.success(request, "Product created successfully.")
        return redirect("product_list")

    return render(request, "inventory/product_form.html", {
        "form": form,
        "page_title": "Create Product"
    })


@login_required
def product_detail(request, pk):
    if not inventory_access_required(request.user):
        messages.error(request, "You are not allowed to view products.")
        return redirect("dashboard")

    product = get_object_or_404(
        Product.objects.select_related("category", "supplier", "created_by"),
        pk=pk
    )

    return render(request, "inventory/product_detail.html", {
        "product": product
    })


@login_required
def product_update(request, pk):
    if not inventory_access_required(request.user):
        messages.error(request, "You are not allowed to edit products.")
        return redirect("dashboard")

    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Product updated successfully.")
        return redirect("product_list")

    return render(request, "inventory/product_form.html", {
        "form": form,
        "page_title": "Edit Product",
        "product": product
    })


@login_required
def product_delete(request, pk):
    if not inventory_access_required(request.user):
        messages.error(request, "You are not allowed to delete products.")
        return redirect("dashboard")

    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect("product_list")

    return render(request, "inventory/product_confirm_delete.html", {
        "product": product
    })


@login_required
def category_list(request):
    if not inventory_access_required(request.user):
        messages.error(request, "You are not allowed to access categories.")
        return redirect("dashboard")

    categories = Category.objects.all()

    return render(request, "inventory/category_list.html", {
        "categories": categories,
        "total_categories": categories.count(),
        "active_categories": categories.filter(is_active=True).count(),
    })


@login_required
def category_create(request):
    if not inventory_access_required(request.user):
        messages.error(request, "You are not allowed to create categories.")
        return redirect("dashboard")

    form = CategoryForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category created successfully.")
        return redirect("category_list")

    return render(request, "inventory/category_form.html", {
        "form": form,
        "page_title": "Create Category"
    })


@login_required
def category_update(request, pk):
    if not inventory_access_required(request.user):
        messages.error(request, "You are not allowed to edit categories.")
        return redirect("dashboard")

    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category updated successfully.")
        return redirect("category_list")

    return render(request, "inventory/category_form.html", {
        "form": form,
        "page_title": "Edit Category",
        "category": category
    })


@login_required
def category_delete(request, pk):
    if not inventory_access_required(request.user):
        messages.error(request, "You are not allowed to delete categories.")
        return redirect("dashboard")

    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect("category_list")

    return render(request, "inventory/category_confirm_delete.html", {
        "category": category
    })


@login_required
def supplier_list(request):
    if not inventory_access_required(request.user):
        messages.error(request, "You are not allowed to access suppliers.")
        return redirect("dashboard")

    suppliers = Supplier.objects.all()

    return render(request, "inventory/supplier_list.html", {
        "suppliers": suppliers,
        "total_suppliers": suppliers.count(),
        "active_suppliers": suppliers.filter(is_active=True).count(),
    })


@login_required
def supplier_create(request):
    if not inventory_access_required(request.user):
        messages.error(request, "You are not allowed to create suppliers.")
        return redirect("dashboard")

    form = SupplierForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Supplier created successfully.")
        return redirect("supplier_list")

    return render(request, "inventory/supplier_form.html", {
        "form": form,
        "page_title": "Create Supplier"
    })


@login_required
def supplier_update(request, pk):
    if not inventory_access_required(request.user):
        messages.error(request, "You are not allowed to edit suppliers.")
        return redirect("dashboard")

    supplier = get_object_or_404(Supplier, pk=pk)
    form = SupplierForm(request.POST or None, instance=supplier)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Supplier updated successfully.")
        return redirect("supplier_list")

    return render(request, "inventory/supplier_form.html", {
        "form": form,
        "page_title": "Edit Supplier",
        "supplier": supplier
    })


@login_required
def supplier_delete(request, pk):
    if not inventory_access_required(request.user):
        messages.error(request, "You are not allowed to delete suppliers.")
        return redirect("dashboard")

    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == "POST":
        supplier.delete()
        messages.success(request, "Supplier deleted successfully.")
        return redirect("supplier_list")

    return render(request, "inventory/supplier_confirm_delete.html", {
        "supplier": supplier
    })