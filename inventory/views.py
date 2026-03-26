from django.shortcuts import render, redirect
from .models import Product, Supplier, Branch
from django.shortcuts import get_object_or_404

def products(request):
    products = Product.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        cost_price = request.POST.get("cost_price")
        selling_price = request.POST.get("selling_price")

        if all([name, price, quantity, cost_price, selling_price]):
           image = request.FILES.get("image")

           Product.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                cost_price=cost_price,
                selling_price=selling_price,
                image=image,
                branch=Branch.objects.first()
            )

    return render(request, "inventory/products.html", {
        "products": products
    })

def suppliers(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")

        Supplier.objects.create(name=name, phone=phone)

        return redirect("suppliers")

    suppliers = Supplier.objects.all()
    return render(request, "inventory/suppliers.html", {"suppliers": suppliers})



def inventory_dashboard(request):
    products = Product.objects.all()

    total_products = products.count()
    low_stock = products.filter(stock__lt=5)

    return render(request, "inventory/dashboard.html", {
        "products": products,
        "total_products": total_products,
        "low_stock": low_stock
    })



def product_list(request):
    products = Product.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        cost_price = request.POST.get("cost_price")
        selling_price = request.POST.get("selling_price")

        if all([name, price, quantity, cost_price, selling_price]):
           image = request.FILES.get("image")

           Product.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                cost_price=cost_price,
                selling_price=selling_price,
                image=image,
                branch=Branch.objects.first()
            )
        return redirect("product_list")  

    return render(request, "inventory/products.html", {
        "products": products
    })



def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect("product_list")



def supplier_list(request):
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")

        if name and phone:
            Supplier.objects.create(name=name, phone=phone)

    return render(request, "inventory/suppliers.html", {
        "suppliers": suppliers
    })



def inventory_home(request):
    products_count = Product.objects.count()
    suppliers_count = Supplier.objects.count()

    return render(request, "inventory/home.html", {
        "products_count": products_count,
        "suppliers_count": suppliers_count
    })

