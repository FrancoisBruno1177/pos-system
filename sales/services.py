from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def broadcast_sale(total):

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(

        "dashboard",

        {
            "type": "send_sales_update",
            "total": total
        }

    )

    