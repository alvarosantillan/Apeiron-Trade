from uuid import uuid4


class MercadoPagoClient:
    def create_checkout(self, user_id: str, plan_code: str) -> dict:
        checkout_id = str(uuid4())
        return {
            "checkoutId": checkout_id,
            "checkoutUrl": f"https://sandbox.mercadopago.local/checkout/{checkout_id}",
            "provider": "mercadopago",
            "externalReference": f"{user_id}:{plan_code}:{checkout_id}",
        }


mp_client = MercadoPagoClient()
