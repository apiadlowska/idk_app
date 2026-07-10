"""
Klasa DataManager - obsługuje zapis i odczyt JSON
Poziom: Klasa 2 LO rozszerzona
"""

import json
import os
from typing import List, Dict, Any

class DataManager:
    """
    Menedżer danych - obsługuje wszystkie operacje na plikach JSON.
    Zapewnia bezpieczeństwo danych i łatwy dostęp do nich.
    """
    
    def __init__(self, data_dir: str = "data") -> None:
        """
        Inicjalizacja DataManager
        
        Args:
            data_dir (str): Ścieżka do folderu z danymi
        """
        self.data_dir = data_dir
        self._ensure_data_directory()
        self._init_default_files()
    
    def _ensure_data_directory(self) -> None:
        """Tworzy folder data jeśli nie istnieje"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"📁 Utworzono folder: {self.data_dir}")
    
    def _init_default_files(self) -> None:
        """Inicjalizuje domyślne pliki JSON jeśli nie istnieją"""
        default_files = {
            "users.json": [],
            "products.json": [],
            "orders.json": [],
            "finances.json": {
                "company_name": "IDK Company",
                "balance": 50000.0,
                "currency": "PLN",
                "total_revenue": 0.0,
                "total_expenses": 0.0
            }
        }
        
        for filename, default_data in default_files.items():
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(default_data, f, ensure_ascii=False, indent=2)
    
    def _read_json(self, filename: str) -> Any:
        """
        Wczytuje dane z pliku JSON
        
        Args:
            filename (str): Nazwa pliku
            
        Returns:
            Any: Zawartość pliku JSON
        """
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Plik {filepath} nie istnieje")
            return []
        except json.JSONDecodeError:
            print(f"❌ Błąd odczytu JSON w pliku {filename}")
            return []
    
    def _write_json(self, filename: str, data: Any) -> bool:
        """
        Zapisuje dane do pliku JSON
        
        Args:
            filename (str): Nazwa pliku
            data (Any): Dane do zapisania
            
        Returns:
            bool: Czy zapis się powiódł
        """
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"❌ Błąd zapisu do {filename}: {e}")
            return False
    
    # UŻYTKOWNICY
    def save_users(self, users: List) -> bool:
        """Zapisuje użytkowników do JSON"""
        users_data = [user.to_dict() for user in users]
        if self._write_json("users.json", users_data):
            print(f"💾 Zapisano {len(users)} użytkowników")
            return True
        return False
    
    def load_users(self) -> List[Dict]:
        """Wczytuje użytkowników z JSON"""
        data = self._read_json("users.json")
        print(f"📖 Wczytano {len(data)} użytkowników")
        return data
    
    # PRODUKTY
    def save_products(self, products: List) -> bool:
        """Zapisuje produkty do JSON"""
        products_data = [product.to_dict() for product in products]
        if self._write_json("products.json", products_data):
            print(f"💾 Zapisano {len(products)} produktów")
            return True
        return False
    
    def load_products(self) -> List[Dict]:
        """Wczytuje produkty z JSON"""
        data = self._read_json("products.json")
        print(f"📖 Wczytano {len(data)} produktów")
        return data
    
    # ZAMÓWIENIA
    def save_orders(self, orders: List) -> bool:
        """Zapisuje zamówienia do JSON"""
        orders_data = [order.to_dict() for order in orders]
        if self._write_json("orders.json", orders_data):
            print(f"💾 Zapisano {len(orders)} zamówień")
            return True
        return False
    
    def load_orders(self) -> List[Dict]:
        """Wczytuje zamówienia z JSON"""
        data = self._read_json("orders.json")
        print(f"📖 Wczytano {len(data)} zamówień")
        return data
    
    # FINANSE
    def save_finances(self, finances_data: Dict) -> bool:
        """Zapisuje stan finansów do JSON"""
        if self._write_json("finances.json", finances_data):
            print(f"💾 Zapisano finanse")
            return True
        return False
    
    def load_finances(self) -> Dict:
        """Wczytuje stan finansów z JSON"""
        data = self._read_json("finances.json")
        return data
    
    def update_balance(self, amount: float, description: str = "") -> bool:
        """
        Aktualizuje saldo firmy
        
        Args:
            amount (float): Kwota (dodatnia/ujemna)
            description (str): Opis operacji
            
        Returns:
            bool: Czy operacja się powiodła
        """
        finances = self.load_finances()
        finances["balance"] += amount
        
        if amount > 0:
            finances["total_revenue"] += amount
        else:
            finances["total_expenses"] += abs(amount)
        
        return self.save_finances(finances)
