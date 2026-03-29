from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, F
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, SupplierForm, ProductForm, StockMovementForm
from .models import Category, Supplier, Product, StockMovement


def inventory_access_required(user):
    return user.is_authenticated and (
        user.is_superuser or user.role in ["SUPER_ADMIN", "ADMIN", "MANAGER"]
    )


def inventory_manage_required(user):
    return user.is_authenticated and (
        user.is_superuser or user.role in ["SUPER_ADMIN", "ADMIN"]
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
    recent_movements = StockMovement.objects.select_related("product", "created_by")[:8]

    context = {
        "total_products": products.count(),
        "active_products": products.filter(is_active=True).count(),
        "total_categories": categories.count(),
        "total_suppliers": suppliers.count(),
        "low_stock_count": low_stock_products.count(),
        "low_stock_products": low_stock_products[:5],
        "recent_movements": recent_movements,
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
        "products": products.order_by("name"),
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
    if not inventory_manage_required(request.user):
        messages.error(request, "You are not allowed to create products.")
        return redirect("dashboard")

    form = ProductForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        product.created_by = request.user
        product.save()

        if product.quantity > 0:
            StockMovement.objects.create(
                product=product,
                movement_type="IN",
                quantity=product.quantity,
                previous_quantity=0,
                new_quantity=product.quantity,
                reference="INITIAL STOCK",
                note="Initial stock on product creation.",
                created_by=request.user,
            )

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

    recent_movements = product.stock_movements.select_related("created_by")[:10]

    return render(request, "inventory/product_detail.html", {
        "product": product,
        "recent_movements": recent_movements,
    })


@login_required
def product_update(request, pk):
    if not inventory_manage_required(request.user):
        messages.error(request, "You are not allowed to edit products.")
        return redirect("dashboard")

    product = get_object_or_404(Product, pk=pk)
    old_quantity = product.quantity
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if request.method == "POST" and form.is_valid():
        updated_product = form.save(commit=False)
        new_quantity = updated_product.quantity
        updated_product.save()

        if new_quantity != old_quantity:
            difference = new_quantity - old_quantity
            movement_type = "IN" if difference > 0 else "OUT"

            StockMovement.objects.create(
                product=updated_product,
                movement_type=movement_type,
                quantity=abs(difference),
                previous_quantity=old_quantity,
                new_quantity=new_quantity,
                reference="PRODUCT UPDATE",
                note="Quantity changed from product edit form.",
                created_by=request.user,
            )

        messages.success(request, "Product updated successfully.")
        return redirect("product_list")

    return render(request, "inventory/product_form.html", {
        "form": form,
        "page_title": "Edit Product",
        "product": product
    })


@login_required
def product_delete(request, pk):
    if not inventory_manage_required(request.user):
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
    if not inventory_manage_required(request.user):
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
    if not inventory_manage_required(request.user):
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
    if not inventory_manage_required(request.user):
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
    if not inventory_manage_required(request.user):
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
    if not inventory_manage_required(request.user):
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
    if not inventory_manage_required(request.user):
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


@login_required
def stock_movement_list(request):
    if not inventory_access_required(request.user):
        messages.error(request, "You are not allowed to access stock history.")
        return redirect("dashboard")

    query = request.GET.get("q", "").strip()
    movement_type = request.GET.get("type", "").strip()

    movements = StockMovement.objects.select_related("product", "created_by").all()

    if query:
        movements = movements.filter(
            Q(product__name__icontains=query) |
            Q(product__sku__icontains=query) |
            Q(reference__icontains=query) |
            Q(note__icontains=query)
        )

    if movement_type:
        movements = movements.filter(movement_type=movement_type)

    context = {
        "movements": movements,
        "query": query,
        "selected_type": movement_type,
        "movement_types": StockMovement.MOVEMENT_TYPES,
    }
    return render(request, "inventory/stock_movement_list.html", context)


@login_required
@transaction.atomic
def stock_adjustment_create(request, pk):
    if not inventory_manage_required(request.user):
        messages.error(request, "You are not allowed to adjust stock.")
        return redirect("dashboard")

    product = get_object_or_404(Product, pk=pk)
    form = StockMovementForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        movement_type = form.cleaned_data["movement_type"]
        quantity = form.cleaned_data["quantity"]
        reference = form.cleaned_data["reference"]
        note = form.cleaned_data["note"]

        previous_quantity = product.quantity
        new_quantity = previous_quantity

        if movement_type in ["IN", "RETURN"]:
            new_quantity = previous_quantity + quantity
        elif movement_type == "OUT":
            if quantity > previous_quantity:
                messages.error(request, "Cannot remove more stock than available.")
                return render(request, "inventory/stock_adjustment_form.html", {
                    "form": form,
                    "product": product,
                })
            new_quantity = previous_quantity - quantity
        elif movement_type == "ADJUSTMENT":
            new_quantity = quantity
            quantity = abs(new_quantity - previous_quantity)

        product.quantity = new_quantity
        product.save(update_fields=["quantity"])

        StockMovement.objects.create(
            product=product,
            movement_type=movement_type,
            quantity=quantity,
            previous_quantity=previous_quantity,
            new_quantity=new_quantity,
            reference=reference,
            note=note,
            created_by=request.user,
        )

        messages.success(request, "Stock adjusted successfully.")
        return redirect("product_detail", pk=product.pk)

    return render(request, "inventory/stock_adjustment_form.html", {
        "form": form,
        "product": product,
    })