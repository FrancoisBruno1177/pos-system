import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from inventory.models import Product, StockMovement
from .forms import SaleCheckoutForm
from .models import Sale, SaleItem


def sales_access_required(user):
    return user.is_authenticated and (
        user.is_superuser or user.role in ["SUPER_ADMIN", "ADMIN", "MANAGER", "CASHIER"]
    )


def sales_manage_required(user):
    return user.is_authenticated and (
        user.is_superuser or user.role in ["SUPER_ADMIN", "ADMIN", "CASHIER"]
    )


def get_sales_back_context(user):
    if user.is_superuser or user.role == "SUPER_ADMIN":
        return {
            "back_url": reverse("superadmin_dashboard"),
            "back_label": "Back to Super Admin Dashboard",
        }
    if user.role == "ADMIN":
        return {
            "back_url": reverse("admin_dashboard"),
            "back_label": "Back to Admin Dashboard",
        }
    if user.role == "MANAGER":
        return {
            "back_url": reverse("manager_dashboard"),
            "back_label": "Back to Manager Dashboard",
        }
    return {
        "back_url": reverse("sales_cashier_dashboard"),
        "back_label": "Back to Cashier Dashboard",
    }


@login_required
def cashier_dashboard(request):
    if not sales_access_required(request.user):
        messages.error(request, "You are not allowed to access the cashier dashboard.")
        return redirect("dashboard")

    today = timezone.localdate()
    today_sales = Sale.objects.filter(created_at__date=today)

    today_revenue = today_sales.aggregate(total=Sum("total_amount"))["total"] or Decimal("0.00")
    total_transactions = today_sales.count()
    available_products = Product.objects.filter(is_active=True, quantity__gt=0).count()
    low_stock_count = Product.objects.filter(is_active=True, quantity__lte=5).count()

    context = {
        "today_revenue": today_revenue,
        "total_transactions": total_transactions,
        "available_products": available_products,
        "low_stock_count": low_stock_count,
        "recent_sales": today_sales.order_by("-created_at")[:8],
    }
    return render(request, "sales/cashier_dashboard.html", context)


@login_required
def pos_view(request):
    if not sales_manage_required(request.user):
        messages.error(request, "You are not allowed to create sales.")
        return redirect("dashboard")

    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()

    products = Product.objects.filter(is_active=True, quantity__gt=0).select_related("category")

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(description__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        "products": products.order_by("name"),
        "query": query,
        "category_id": category_id,
        "checkout_form": SaleCheckoutForm(),
        **get_sales_back_context(request.user),
    }
    return render(request, "sales/pos.html", context)


@login_required
@transaction.atomic
def create_sale(request):
    if not sales_manage_required(request.user):
        messages.error(request, "You are not allowed to create sales.")
        return redirect("dashboard")

    if request.method != "POST":
        return redirect("pos_view")

    checkout_form = SaleCheckoutForm(request.POST)
    cart_json = request.POST.get("cart_data", "[]")

    try:
        cart_data = json.loads(cart_json)
    except json.JSONDecodeError:
        messages.error(request, "Invalid cart data.")
        return redirect("pos_view")

    if not checkout_form.is_valid():
        messages.error(request, "Please correct the checkout form.")
        return redirect("pos_view")

    if not cart_data:
        messages.error(request, "Your cart is empty.")
        return redirect("pos_view")

    validated_items = []
    subtotal = Decimal("0.00")

    for item in cart_data:
        product_id = item.get("product_id")
        quantity = item.get("quantity")

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            messages.error(request, "Invalid quantity in cart.")
            return redirect("pos_view")

        if quantity <= 0:
            messages.error(request, "Quantity must be greater than zero.")
            return redirect("pos_view")

        product = (
            Product.objects
            .select_for_update()
            .filter(pk=product_id, is_active=True)
            .first()
        )

        if not product:
            messages.error(request, "A product in your cart no longer exists.")
            return redirect("pos_view")

        if product.quantity < quantity:
            messages.error(request, f"Insufficient stock for {product.name}.")
            return redirect("pos_view")

        unit_price = Decimal(product.selling_price)
        line_total = Decimal(quantity) * unit_price
        subtotal += line_total

        validated_items.append({
            "product": product,
            "quantity": quantity,
            "unit_price": unit_price,
            "line_total": line_total,
        })

    tax_amount = Decimal("0.00")
    total_amount = subtotal + tax_amount
    amount_paid = checkout_form.cleaned_data["amount_paid"]

    if amount_paid < total_amount:
        messages.error(request, "Amount paid is less than total sale amount.")
        return redirect("pos_view")

    change_amount = amount_paid - total_amount

    sale = Sale.objects.create(
        cashier=request.user,
        customer_name=checkout_form.cleaned_data["customer_name"],
        payment_method=checkout_form.cleaned_data["payment_method"],
        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount,
        amount_paid=amount_paid,
        change_amount=change_amount,
    )

    for item in validated_items:
        product = item["product"]
        previous_quantity = product.quantity
        new_quantity = previous_quantity - item["quantity"]

        SaleItem.objects.create(
            sale=sale,
            product=product,
            product_name=product.name,
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            line_total=item["line_total"],
        )

        product.quantity = new_quantity
        product.save(update_fields=["quantity"])

        StockMovement.objects.create(
            product=product,
            movement_type="SALE",
            quantity=item["quantity"],
            previous_quantity=previous_quantity,
            new_quantity=new_quantity,
            reference=f"SALE #{sale.id}",
            note="Stock deducted from completed sale.",
            created_by=request.user,
        )

    messages.success(request, "Sale completed successfully.")
    return redirect("sale_receipt", pk=sale.pk)


@login_required
def sale_list(request):
    if not sales_access_required(request.user):
        messages.error(request, "You are not allowed to access sales.")
        return redirect("dashboard")

    query = request.GET.get("q", "").strip()
    sales = Sale.objects.select_related("cashier").prefetch_related("items").all()

    if query:
        filtered_sales = sales.filter(
            Q(customer_name__icontains=query) |
            Q(cashier__email__icontains=query)
        )

        if query.isdigit():
            filtered_sales = filtered_sales | sales.filter(id=int(query))

        sales = filtered_sales

    context = {
        "sales": sales.order_by("-created_at").distinct(),
        "query": query,
        **get_sales_back_context(request.user),
    }
    return render(request, "sales/sale_list.html", context)


@login_required
def sale_detail(request, pk):
    if not sales_access_required(request.user):
        messages.error(request, "You are not allowed to view this sale.")
        return redirect("dashboard")

    sale = get_object_or_404(
        Sale.objects.select_related("cashier").prefetch_related("items__product"),
        pk=pk,
    )

    context = {
        "sale": sale,
        **get_sales_back_context(request.user),
    }
    return render(request, "sales/sale_detail.html", context)


@login_required
def sale_receipt(request, pk):
    if not sales_access_required(request.user):
        messages.error(request, "You are not allowed to view this receipt.")
        return redirect("dashboard")

    sale = get_object_or_404(
        Sale.objects.select_related("cashier").prefetch_related("items"),
        pk=pk,
    )

    context = {
        "sale": sale,
        **get_sales_back_context(request.user),
    }
    return render(request, "sales/receipt.html", context)