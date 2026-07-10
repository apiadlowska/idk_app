"""
Klasa Order - reprezentuje zamówienie (KOMPOZYCJA)
Poziom: Klasa 2 LO rozszerzona
"""

from datetime import datetime
from typing import List, Dict, Any

class Order:
    """
    Klasa reprezentująca zamówienie.
    KOMPOZYCJA: Zamówienie zawiera wiele produktów.
    """
    
    def __init__(self, order_id: int, seller_name: str, customer_name: str) -> None:
        """
        Inicjalizacja zamówienia
        
        Args:
            order_id (int): Unikalny ID zamówienia
            seller_name (str): Imię sprzedawcy
            customer_name (str): Imię klienta
        """
        self.order_id = order_id
        self.seller_name = seller_name
        self.customer_name = customer_name
        self.items: List[Dict[str, Any]] = []  # KOMPOZYCJA - lista produktów
        self.order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.total_value = 0.0
        self.status = "pending"  # pending, completed, cancelled
    
    def add_product(self, product, quantity: int) -> bool:
        """
        Dodaje produkt do zamówienia (KOMPOZYCJA)
        
        Args:
            product: Obiekt Product
            quantity (int): Ilość
            
        Returns:
            bool: Czy operacja się powiodła
        """
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
    
    def complete_order(self) -> None:
        """Zmienia status na ukończone"""
        self.status = "completed"
        print(f"✅ Zamówienie {self.order_id} ukończone!")
    
    def cancel_order(self) -> None:
        """Anuluje zamówienie"""
        self.status = "cancelled"
        self.total_value = 0
        print(f"❌ Zamówienie {self.order_id} anulowane!")
    
    def get_summary(self) -> str:
        """
        Zwraca podsumowanie zamówienia
        
        Returns:
            str: Sformatowany tekst
        """
        return f"Zamówienie #{self.order_id}: {self.customer_name} - {self.total_value:.2f} zł ({self.status})"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Konwertuje zamówienie na słownik (do JSON)
        
        Returns:
            Dict: Słownik z danymi zamówienia
        """
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
    def from_dict(data: Dict[str, Any]) -> 'Order':
        """
        Konwertuje słownik na zamówienie (z JSON)
        
        Args:
            data (Dict): Słownik z danymi
            
        Returns:
            Order: Nowy obiekt Order
        """
        order = Order(data["order_id"], data["seller_name"], data["customer_name"])
        order.items = data.get("items", [])
        order.order_date = data.get("order_date", "")
        order.total_value = data.get("total_value", 0.0)
        order.status = data.get("status", "pending")
        return order
