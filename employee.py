"""
Klasa Employee - dziedziczy po User
Poziom: Klasa 2 LO rozszerzona
"""

from typing import Dict, Any
from user import User

class Employee(User):
    """
    Klasa Employee - dziedziczy po User (DZIEDZICZENIE).
    Pracownik może sprzedawać produkty (jeśli ma uprawnienia).
    """
    
    def __init__(self, user_id: int, name: str, email: str, role: str, password: str, salary: float = 0.0) -> None:
        """
        Inicjalizacja pracownika
        
        Args:
            user_id (int): Unikalny ID
            name (str): Imię i nazwisko
            email (str): Email
            role (str): "employee" lub "seller"
            password (str): Hasło
            salary (float): Pensja
        """
        super().__init__(user_id, name, email, role, password)
        self.salary = salary
        self.sales_count = 0
        self.total_sales_value = 0.0
        self.hire_date = "2024"
        
        # Uprawnienia zależnie od roli
        if role == "seller":
            self.permissions = ["sell_products", "view_own_sales", "view_products"]
        elif role == "employee":
            self.permissions = ["view_products", "view_own_info"]
        else:
            self.permissions = []
    
    def can_sell(self) -> bool:
        """
        Sprawdza czy pracownik może sprzedawać
        
        Returns:
            bool: Czy ma uprawnienia do sprzedaży
        """
        return "sell_products" in self.permissions
    
    def make_sale(self, product_name: str, quantity: int, unit_price: float) -> bool:
        """
        Rejestruje sprzedaż
        
        Args:
            product_name (str): Nazwa produktu
            quantity (int): Ilość
            unit_price (float): Cena jednostkowa
            
        Returns:
            bool: Czy sprzedaż się powiodła
        """
        if not self.can_sell():
            print(f"❌ {self.name} nie ma uprawnień do sprzedaży!")
            return False
        
        if quantity <= 0:
            print("❌ Ilość musi być większa od 0!")
            return False
        
        sale_value = quantity * unit_price
        self.sales_count += 1
        self.total_sales_value += sale_value
        print(f"✅ {self.name} sprzedał {quantity}x {product_name} za {sale_value:.2f} zł")
        return True
    
    def get_performance(self) -> Dict[str, Any]:
        """
        Zwraca statystyki sprzedaży
        
        Returns:
            Dict: Słownik ze statystykami
        """
        average_sale = self.total_sales_value / self.sales_count if self.sales_count > 0 else 0
        return {
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "sales_count": self.sales_count,
            "total_sales_value": total_sales_value,
            "average_sale": average_sale,
            "salary": self.salary
        }
    
    def get_info(self) -> str:
        """
        Zwraca informacje o pracowniku
        
        Returns:
            str: Sformatowany tekst
        """
        base_info = super().get_info()
        sales_info = f" | Sprzedaż: {self.sales_count} ({self.total_sales_value:.2f} zł)"
        return base_info + sales_info
    
    def to_dict(self) -> Dict[str, Any]:
        """Konwertuje na słownik"""
        data = super().to_dict()
        data["salary"] = self.salary
        data["sales_count"] = self.sales_count
        data["total_sales_value"] = self.total_sales_value
        data["permissions"] = self.permissions
        data["hire_date"] = self.hire_date
        return data
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Employee':
        """Konwertuje ze słownika"""
        employee = Employee(
            data["user_id"],
            data["name"],
            data["email"],
            data["role"],
            data["password"],
            data.get("salary", 0.0)
        )
        employee.is_active = data.get("is_active", True)
        employee.sales_count = data.get("sales_count", 0)
        employee.total_sales_value = data.get("total_sales_value", 0.0)
        employee.hire_date = data.get("hire_date", "2024")
        return employee
