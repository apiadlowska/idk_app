"""
Klasa Company - zarządza całą firmą
Poziom: Klasa 2 LO rozszerzona
"""

from typing import List, Optional, Dict
from user import User
from admin import Admin
from employee import Employee
from product import Product
from order import Order
from data_manager import DataManager

class Company:
    """
    Klasa zarządzająca całą firmą.
    Odpowiada za zarządzanie użytkownikami, produktami, zamówieniami i finansami.
    """
    
    def __init__(self, company_name: str) -> None:
        """
        Inicjalizacja firmy
        
        Args:
            company_name (str): Nazwa firmy
        """
        self.company_name = company_name
        self.users: List[User] = []
        self.products: List[Product] = []
        self.orders: List[Order] = []
        self.data_manager = DataManager()
        self.current_user: Optional[User] = None
        self._order_counter = 0
        
        self._load_all_data()
    
    def _load_all_data(self) -> None:
        """Wczytuje wszystkie dane z JSON"""
        print("🔄 Wczytywanie danych...")
        
        # Wczytanie użytkowników
        users_data = self.data_manager.load_users()
        for user_data in users_data:
            if user_data["role"] == "admin":
                user = Admin.from_dict(user_data)
            else:
                user = Employee.from_dict(user_data)
            self.users.append(user)
        
        # Wczytanie produktów
        products_data = self.data_manager.load_products()
        for product_data in products_data:
            self.products.append(Product.from_dict(product_data))
        
        # Wczytanie zamówień
        orders_data = self.data_manager.load_orders()
        for order_data in orders_data:
            self.orders.append(Order.from_dict(order_data))
    
    def save_all_data(self) -> None:
        """Zapisuje wszystkie dane do JSON"""
        print("💾 Zapisywanie danych...")
        self.data_manager.save_users(self.users)
        self.data_manager.save_products(self.products)
        self.data_manager.save_orders(self.orders)
    
    # LOGOWANIE
    def login(self, email: str, password: str) -> bool:
        """
        Loguje użytkownika
        
        Args:
            email (str): Email
            password (str): Hasło
            
        Returns:
            bool: Czy logowanie się powiodło
        """
        for user in self.users:
            if user.email == email and user.password == password and user.is_active:
                self.current_user = user
                print(f"✅ Zalogowano jako: {user.name} ({user.role})")
                return True
        
        print("❌ Błędne dane logowania lub użytkownik nieaktywny")
        return False
    
    def logout(self) -> None:
        """Wylogowuje bieżącego użytkownika"""
        if self.current_user:
            print(f"👋 Wylogowano użytkownika: {self.current_user.name}")
            self.current_user = None
    
    # ZARZĄDZANIE UŻYTKOWNIKAMI
    def add_user(self, user: User) -> bool:
        """Dodaje nowego użytkownika"""
        if self._is_admin_logged_in():
            self.users.append(user)
            print(f"✅ Dodano użytkownika: {user.name}")
            return True
        return False
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Zwraca użytkownika po emailu"""
        for user in self.users:
            if user.email == email:
                return user
        return None
    
    def get_all_users(self) -> List[User]:
        """Zwraca listę wszystkich użytkowników"""
        return self.users
    
    # ZARZĄDZANIE PRODUKTAMI
    def add_product(self, product: Product) -> bool:
        """Dodaje nowy produkt"""
        if self._is_admin_logged_in():
            self.products.append(product)
            print(f"✅ Dodano produkt: {product.name}")
            return True
        return False
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Zwraca produkt po ID"""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
    
    def get_all_products(self) -> List[Product]:
        """Zwraca listę wszystkich produktów"""
        return self.products
    
    # ZAMÓWIENIA
    def create_order(self, customer_name: str) -> Optional[Order]:
        """
        Tworzy nowe zamówienie
        
        Args:
            customer_name (str): Imię klienta
            
        Returns:
            Order: Nowe zamówienie lub None
        """
        if not self._is_seller_logged_in():
            print("❌ Tylko sprzedawcy mogą tworzyć zamówienia!")
            return None
        
        self._order_counter += 1
        order = Order(self._order_counter, self.current_user.name, customer_name)
        self.orders.append(order)
        print(f"✅ Utworzono zamówienie #{self._order_counter}")
        return order
    
    def sell_product(self, order: Order, product: Product, quantity: int) -> bool:
        """
        Dodaje produkt do zamówienia i zmniejsza magazyn
        
        Args:
            order (Order): Zamówienie
            product (Product): Produkt
            quantity (int): Ilość
            
        Returns:
            bool: Czy sprzedaż się powiodła
        """
        if not product.reduce_stock(quantity):
            return False
        
        order.add_product(product, quantity)
        
        # Aktualizacja finansów
        sale_value = quantity * product.price
        self.data_manager.update_balance(sale_value, f"Sprzedaż: {product.name}")
        
        # Aktualizacja statystyk pracownika
        if isinstance(self.current_user, Employee):
            self.current_user.make_sale(product.name, quantity, product.price)
        
        return True
    
    def complete_order(self, order_id: int) -> bool:
        """Zamyka zamówienie"""
        for order in self.orders:
            if order.order_id == order_id:
                order.complete_order()
                return True
        return False
    
    # WSPARCIE ADMINISTRATORA
    def _is_admin_logged_in(self) -> bool:
        """Sprawdza czy zalogowany jest admin"""
        if self.current_user and isinstance(self.current_user, Admin):
            return True
        print("❌ Wymagane uprawnienia administratora!")
        return False
    
    def _is_seller_logged_in(self) -> bool:
        """Sprawdza czy zalogowany jest sprzedawca"""
        if self.current_user and isinstance(self.current_user, Employee):
            if self.current_user.can_sell():
                return True
        print("❌ Brak uprawnień do sprzedaży!")
        return False
    
    def get_company_info(self) -> Dict:
        """Zwraca informacje o firmie"""
        finances = self.data_manager.load_finances()
        return {
            "company_name": self.company_name,
            "total_users": len(self.users),
            "total_products": len(self.products),
            "total_orders": len(self.orders),
            "balance": finances["balance"],
            "total_revenue": finances["total_revenue"]
        }
