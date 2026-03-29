from decimal import Decimal

from django import forms


class SaleCheckoutForm(forms.Form):
    customer_name = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Customer name (optional)",
            }
        ),
    )

    payment_method = forms.ChoiceField(
        choices=(
            ("CASH", "Cash"),
            ("MOBILE_MONEY", "Mobile Money"),
            ("CARD", "Card"),
        ),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    amount_paid = forms.DecimalField(
        min_value=Decimal("0.00"),
        decimal_places=2,
        max_digits=12,
        initial=Decimal("0.00"),
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Amount paid",
            }
        ),
    )