"""Mock payment processor + COD."""
import uuid
from datetime import datetime
from database.mongodb import get_db


class PaymentProcessor:
    METHODS = ["UPI", "Debit Card", "Credit Card", "Net Banking", "Cash on Delivery"]

    def __init__(self):
        self.db = get_db()

    def process(self, user_email, amount, method, order_id):
        """Simulate payment — always succeeds; COD marked pending."""
        status = "pending" if method == "Cash on Delivery" else "paid"
        txn = {
            "txn_id": f"TXN-{uuid.uuid4().hex[:10].upper()}",
            "user_email": user_email,
            "order_id": order_id,
            "amount": amount,
            "method": method,
            "status": status,
            "created_at": datetime.utcnow(),
        }
        self.db.payments.insert_one(txn)
        return txn

    def invoice(self, txn, order):
        lines = [
            "===== FoodRush Invoice =====",
            f"Txn:    {txn['txn_id']}",
            f"Order:  {order['_id']}",
            f"Date:   {txn['created_at'].strftime('%Y-%m-%d %H:%M')}",
            f"Method: {txn['method']}",
            f"Status: {txn['status'].upper()}",
            "-" * 30,
        ]
        for it in order["items"]:
            lines.append(f"{it['name']} x{it['qty']}  ₹{it['price']*it['qty']}")
        lines.append("-" * 30)
        lines.append(f"Subtotal:      ₹{order['subtotal']}")
        lines.append(f"Delivery:      ₹{order['delivery_fee']}")
        lines.append(f"GST (5%):      ₹{order['gst']}")
        lines.append(f"TOTAL:         ₹{order['total']}")
        return "\n".join(lines)
