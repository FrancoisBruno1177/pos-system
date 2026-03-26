from django.template.loader import render_to_string


def generate_receipt(sale):

    return render_to_string("sales/receipt.html", {

        "sale": sale

    })
    