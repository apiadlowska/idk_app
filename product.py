"""
Klasa Product - reprezentuje produkt firmy
Poziom: Klasa 2 LO rozszerzona
"""

from typing import Dict, Any

class Product:
    """
    Klasa reprezentująca produkt.
    Zawiera informacje o produkcie, cenie i magazynie.
    """
    
    def __init__(self, product_id: int, name: str, description: str, price: float, stock_quantity: int) -> None:
        """
        Inicjalizacja produktu
        
        Args:
            product_id (int): Unikalny ID produktu
            name (str): Nazwa produktu
            description (str): Opis produktu
            price (float): Cena jednostkowa
            stock_quantity (int): Ilość w magazynie
        """
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.units_sold = 0
    
    def reduce_stock(self, quantity: int) -> bool:
        """
        Zmniejsza stan magazynu
        
        Args:
            quantity (int): Ilość do zmniejszenia
            
        Returns:
            bool: Czy operacja się powiodła
        """
        if quantity > self.stock_quantity:
            print(f"❌ Brak wystarczającej ilości {self.name}! (dostępne: {self.stock_quantity})")
            return False
        
        self.stock_quantity -= quantity
        self.units_sold += quantity
        print(f"✅ Zmniejszono magazyn {self.name} o {quantity} szt.")
        return True
    
    def increase_stock(self, quantity: int) -> None:
        """
        Zwiększa stan magazynu
        
        Args:
            quantity (int): Ilość do dodania
        """
        self.stock_quantity += quantity
        print(f"✅ Dodano {quantity} szt. produktu {self.name}")
    
    def get_total_value(self) -> float:
        """
        Zwraca wartość całego magazynu tego produktu
        
        Returns:
            float: Wartość magazynu
        """
        return self.stock_quantity * self.price
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Konwertuje produkt na słownik (do JSON)
        
        Returns:
            Dict: Słownik z danymi produktu
        """
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock_quantity": self.stock_quantity,
            "units_sold": self.units_sold
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Product':
        """
        Konwertuje słownik na produkt (z JSON)
        
        Args:
            data (Dict): Słownik z danymi
            
        Returns:
            Product: Nowy obiekt Product
        """
        product = Product(
            data["product_id"],
            data["name"],
            data["description"],
            data["price"],
            data["stock_quantity"]
        )
        product.units_sold = data.get("units_sold", 0)
        return product
    
    def get_info(self) -> str:
        """
        Zwraca informacje o produkcie
        
        Returns:
            str: Sformatowany tekst
        """
        return f"{self.name}: {self.price:.2f} zł (dostępne: {self.stock_quantity} szt., sprzedano: {self.units_sold} szt.)"
