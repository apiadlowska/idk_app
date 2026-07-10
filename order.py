"""
Klasa Order - reprezentuje zamówienie (KOMPOZYCJA - zawiera Products)
"""

from datetime import datetime

class Order:
    """Klasa reprezentująca zamówienie"""
    
    def __init__(self, order_id, seller_name, customer_name):
        """
        Inicjalizacja zamówienia
        
        Args:
            order_id: Unikalny ID zamówienia
            seller_name: Imię sprzedawcy
            customer_name: Imię klienta
        """
        self.order_id = order_id
        self.seller_name = seller_name
        self.customer_name = customer_name
        self.items = []  # KOMPOZYCJA - lista produktów w zamówieniu
        self.order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.total_value = 0.0
        self.status = "pending"  # pending, completed, cancelled
    
    def add_product(self, product, quantity):
        """Dodaje produkt do zamówienia (KOMPOZYCJA)"""
        if quantity <= 0:
            print("❌ Ilość musi być większa od 0!")
            return False
        
        item = {
            "product_name": product.name,
            "product_id": product.product_id,
            "quantity": quantity,
            "unit_price": product.price,
            "total_price": quantity * product.price
        }
        
        self.items.append(item)
        self.total_value += item["total_price"]
        print(f"✅ Dodano {quantity}x {product.name} do zamówienia")
        return True
    
    def complete_order(self):
        """Zmienia status na ukończone"""
        self.status = "completed"
        print(f"✅ Zamówienie {self.order_id} ukończone!")
    
    def cancel_order(self):
        """Anuluje zamówienie"""
        self.status = "cancelled"
        self.total_value = 0
        print(f"❌ Zamówienie {self.order_id} anulowane!")
    
    def get_summary(self):
        """Zwraca podsumowanie zamówienia"""
        return f"Zamówienie #{self.order_id}: {self.customer_name} - {self.total_value:.2f} zł ({self.status})"
    
    def to_dict(self):
        """Konwertuje na słownik"""
        return {
            "order_id": self.order_id,
            "seller_name": self.seller_name,
            "customer_name": self.customer_name,
            "items": self.items,
            "order_date": self.order_date,
            "total_value": self.total_value,
            "status": self.status
        }
    
    @staticmethod
    def from_dict(data):
        """Konwertuje ze słownika"""
        order = Order(data["order_id"], data["seller_name"], data["customer_name"])
        order.items = data.get("items", [])
        order.order_date = data.get("order_date", "")
        order.total_value = data.get("total_value", 0.0)
        order.status = data.get("status", "pending")
        return order
