from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_invoice_email(user, sale):

    html = render_to_string("invoices/invoice.html", {

        "sale": sale

    })

    email = EmailMessage(

        subject="POSIFY Invoice",

        body=html,

        to=[user.email]

    )

    email.content_subtype = "html"

    email.send()
    