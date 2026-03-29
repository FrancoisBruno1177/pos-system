from django import forms
from .models import Category, Supplier, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Category name"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Description"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        qs = Category.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A category with this name already exists.")
        return name


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "email", "phone", "address", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Supplier name"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Supplier email"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Supplier phone"
            }),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Supplier address"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        return email.lower().strip() if email else email


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "sku",
            "category",
            "supplier",
            "cost_price",
            "selling_price",
            "quantity",
            "low_stock_threshold",
            "description",
            "image",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Product name"
            }),
            "sku": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "SKU"
            }),
            "category": forms.Select(attrs={"class": "form-control"}),
            "supplier": forms.Select(attrs={"class": "form-control"}),
            "cost_price": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Cost price"
            }),
            "selling_price": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Selling price"
            }),
            "quantity": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Stock quantity"
            }),
            "low_stock_threshold": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Low stock threshold"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Product description"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_sku(self):
        sku = self.cleaned_data["sku"].strip().upper()
        qs = Product.objects.filter(sku__iexact=sku)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A product with this SKU already exists.")
        return sku

    def clean(self):
        cleaned_data = super().clean()
        cost_price = cleaned_data.get("cost_price")
        selling_price = cleaned_data.get("selling_price")
        quantity = cleaned_data.get("quantity")
        low_stock_threshold = cleaned_data.get("low_stock_threshold")

        if cost_price is not None and cost_price < 0:
            self.add_error("cost_price", "Cost price cannot be negative.")

        if selling_price is not None and selling_price <= 0:
            self.add_error("selling_price", "Selling price must be greater than zero.")

        if quantity is not None and quantity < 0:
            self.add_error("quantity", "Quantity cannot be negative.")

        if low_stock_threshold is not None and low_stock_threshold < 0:
            self.add_error("low_stock_threshold", "Low stock threshold cannot be negative.")

        return cleaned_data