"""
Klasa Product - reprezentuje produkt
"""

class Product:
    """Klasa reprezentująca produkt firmy"""
    
    def __init__(self, product_id, name, description, price, stock_quantity):
        """
        Inicjalizacja produktu
        
        Args:
            product_id: Unikalny ID produktu
            name: Nazwa produktu
            description: Opis produktu
            price: Cena jednostkowa
            stock_quantity: Ilość w magazynie
        """
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.units_sold = 0
    
    def reduce_stock(self, quantity):
        """Zmniejsza stan magazynu"""
        if quantity > self.stock_quantity:
            print(f"❌ Brak wystarczającej ilości {self.name}! (dostępne: {self.stock_quantity})")
            return False
        
        self.stock_quantity -= quantity
        self.units_sold += quantity
        return True
    
    def increase_stock(self, quantity):
        """Zwiększa stan magazynu"""
        self.stock_quantity += quantity
        print(f"✅ Dodano {quantity} szt. produktu {self.name}")
    
    def get_total_value(self):
        """Zwraca wartość całego magazynu tego produktu"""
        return self.stock_quantity * self.price
    
    def to_dict(self):
        """Konwertuje na słownik"""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock_quantity": self.stock_quantity,
            "units_sold": self.units_sold
        }
    
    @staticmethod
    def from_dict(data):
        """Konwertuje ze słownika"""
        product = Product(
            data["product_id"],
            data["name"],
            data["description"],
            data["price"],
            data["stock_quantity"]
        )
        product.units_sold = data.get("units_sold", 0)
        return product
    
    def get_info(self):
        """Zwraca informacje o produkcie"""
        return f"{self.name}: {self.price:.2f} zł (dostępne: {self.stock_quantity})"
