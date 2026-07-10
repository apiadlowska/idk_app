"""
Klasa UserInterface - prosty interfejs użytkownika
Poziom: Klasa 2 LO rozszerzona
"""

from company import Company
from admin import Admin
from employee import Employee
from product import Product
from typing import Optional

class UserInterface:
    """
    Prosty interfejs tekstowy do interakcji z systemem.
    Menu dla administratora i pracowników.
    """
    
    def __init__(self) -> None:
        """Inicjalizacja interfejsu"""
        self.company = Company("IDK Company")
        self._init_default_data()
    
    def _init_default_data(self) -> None:
        """Inicjalizuje domyślne dane jeśli baza jest pusta"""
        if not self.company.users:
            # Dodaj domyślnych użytkowników
            admin = Admin(1, "Anna Admin", "anna@idk.pl", "admin123")
            seller1 = Employee(2, "Piotr Sprzedawca", "piotr@idk.pl", "seller", "seller123", 3000.0)
            seller2 = Employee(3, "Maria Sprzedawca", "maria@idk.pl", "seller", "seller123", 3000.0)
            
            self.company.users.append(admin)
            self.company.users.append(seller1)
            self.company.users.append(seller2)
        
        if not self.company.products:
            # Dodaj domyślne produkty
            laptop = Product(1, "Laptop Dell", "Laptop 15 cali, Intel i7", 3500.0, 10)
            phone = Product(2, "Smartphone Samsung", "Galaxy S24, 256GB", 2500.0, 15)
            tablet = Product(3, "Tablet Apple", "iPad Pro 12.9, 256GB", 4500.0, 8)
            
            self.company.products.append(laptop)
            self.company.products.append(phone)
            self.company.products.append(tablet)
        
        # Zapisz domyślne dane
        self.company.save_all_data()
    
    def run(self) -> None:
        """Uruchamia główne menu"""
        self._display_welcome()
        
        while True:
            if not self.company.current_user:
                self._login_menu()
            else:
                if isinstance(self.company.current_user, Admin):
                    self._admin_menu()
                else:
                    self._employee_menu()
    
    def _display_welcome(self) -> None:
        """Wyświetla ekran powitalny"""
        print("\n" + "=" * 60)
        print("🏢 SYSTEM ZARZĄDZANIA FIRMĄ - IDK COMPANY")
        print("=" * 60)
        print("Projektu na ocenę z informatyki (klasa 2 LO rozszerzona)")
        print("=" * 60 + "\n")
    
    def _login_menu(self) -> None:
        """Menu logowania"""
        print("\n📝 LOGOWANIE")
        print("-" * 60)
        print("1. Zaloguj się")
        print("2. Wyjście")
        print("-" * 60)
        
        choice = input("Wybierz opcję: ").strip()
        
        if choice == "1":
            email = input("Email: ").strip()
            password = input("Hasło: ").strip()
            
            if not self.company.login(email, password):
                input("Naciśnij Enter, aby kontynuować...")
        
        elif choice == "2":
            print("👋 Do widzenia!")
            exit()
    
    def _admin_menu(self) -> None:
        """Menu administratora"""
        print(f"\n👤 Zalogowany: {self.company.current_user.name} (ADMIN)")
        print("-" * 60)
        print("1. Zarządzaj użytkownikami")
        print("2. Zarządzaj produktami")
        print("3. Przejrzyj zamówienia")
        print("4. Generuj raport")
        print("5. Wyloguj się")
        print("-" * 60)
        
        choice = input("Wybierz opcję: ").strip()
        
        if choice == "1":
            self._manage_users_menu()
        elif choice == "2":
            self._manage_products_menu()
        elif choice == "3":
            self._view_orders()
        elif choice == "4":
            self._generate_report()
        elif choice == "5":
            self.company.logout()
    
    def _employee_menu(self) -> None:
        """Menu pracownika/sprzedawcy"""
        print(f"\n👤 Zalogowany: {self.company.current_user.name} ({self.company.current_user.role.upper()})")
        print("-" * 60)
        print("1. Przejrzyj produkty")
        print("2. Sprzedaj produkty")
        print("3. Moje sprzedaże")
        print("4. Wyloguj się")
        print("-" * 60)
        
        choice = input("Wybierz opcję: ").strip()
        
        if choice == "1":
            self._view_products()
        elif choice == "2":
            self._sell_products()
        elif choice == "3":
            self._view_my_sales()
        elif choice == "4":
            self.company.logout()
    
    def _manage_users_menu(self) -> None:
        """Menu zarządzania użytkownikami"""
        print("\n📋 ZARZĄDZANIE UŻYTKOWNIKAMI")
        print("-" * 60)
        print("1. Wyświetl wszystkich użytkowników")
        print("2. Dodaj nowego użytkownika")
        print("3. Zmień rolę użytkownika")
        print("4. Deaktywuj użytkownika")
        print("5. Aktywuj użytkownika")
        print("6. Powrót")
        print("-" * 60)
        
        choice = input("Wybierz opcję: ").strip()
        
        if choice == "1":
            users = self.company.get_all_users()
            print("\n")
            for user in users:
                print(f"  {user.get_info()}")
            print()
        
        elif choice == "2":
            try:
                user_id = int(input("ID użytkownika: "))
                name = input("Imię i nazwisko: ")
                email = input("Email: ")
                role = input("Rola (admin/seller/employee): ").strip().lower()
                password = input("Hasło: ")
                salary = float(input("Pensja (0 dla admina): ")) if role != "admin" else 0
                
                if role == "admin":
                    user = Admin(user_id, name, email, password)
                else:
                    user = Employee(user_id, name, email, role, password, salary)
                
                self.company.add_user(user)
            except ValueError:
                print("❌ Błędne dane!")
        
        elif choice == "3":
            email = input("Email użytkownika: ")
            user = self.company.get_user_by_email(email)
            if user:
                new_role = input("Nowa rola (admin/seller/employee): ").strip().lower()
                if isinstance(self.company.current_user, Admin):
                    self.company.current_user.edit_user_role(user, new_role)
            else:
                print("❌ Użytkownik nie znaleziony!")
        
        elif choice == "4":
            email = input("Email użytkownika: ")
            user = self.company.get_user_by_email(email)
            if user:
                if isinstance(self.company.current_user, Admin):
                    self.company.current_user.deactivate_user(user)
            else:
                print("❌ Użytkownik nie znaleziony!")
        
        elif choice == "5":
            email = input("Email użytkownika: ")
            user = self.company.get_user_by_email(email)
            if user:
                if isinstance(self.company.current_user, Admin):
                    self.company.current_user.activate_user(user)
            else:
                print("❌ Użytkownik nie znaleziony!")
        
        self.company.save_all_data()
        input("Naciśnij Enter, aby kontynuować...")
    
    def _manage_products_menu(self) -> None:
        """Menu zarządzania produktami"""
        print("\n📦 ZARZĄDZANIE PRODUKTAMI")
        print("-" * 60)
        print("1. Wyświetl wszystkie produkty")
        print("2. Dodaj nowy produkt")
        print("3. Zwiększ magazyn")
        print("4. Powrót")
        print("-" * 60)
        
        choice = input("Wybierz opcję: ").strip()
        
        if choice == "1":
            self._view_products()
        
        elif choice == "2":
            try:
                product_id = int(input("ID produktu: "))
                name = input("Nazwa: ")
                description = input("Opis: ")
                price = float(input("Cena: "))
                quantity = int(input("Ilość w magazynie: "))
                
                product = Product(product_id, name, description, price, quantity)
                self.company.add_product(product)
            except ValueError:
                print("❌ Błędne dane!")
        
        elif choice == "3":
            try:
                product_id = int(input("ID produktu: "))
                product = self.company.get_product_by_id(product_id)
                if product:
                    quantity = int(input("Ilość do dodania: "))
                    product.increase_stock(quantity)
                else:
                    print("❌ Produkt nie znaleziony!")
            except ValueError:
                print("❌ Błędne dane!")
        
        self.company.save_all_data()
        input("Naciśnij Enter, aby kontynuować...")
    
    def _view_products(self) -> None:
        """Wyświetla produkty"""
        print("\n📦 PRODUKTY")
        print("-" * 60)
        products = self.company.get_all_products()
        if products:
            for product in products:
                print(f"  {product.get_info()}")
        else:
            print("  Brak produktów w systemie")
        print()
    
    def _sell_products(self) -> None:
        """Menu sprzedaży produktów"""
        if not self.company.current_user or not isinstance(self.company.current_user, Employee):
            print("❌ Brak uprawnień!")
            return
        
        if not self.company.current_user.can_sell():
            print("❌ Nie masz uprawnień do sprzedaży!")
            return
        
        print("\n🛒 SPRZEDAŻ PRODUKTÓW")
        print("-" * 60)
        
        self._view_products()
        
        try:
            customer_name = input("Imię klienta: ")
            order = self.company.create_order(customer_name)
            
            if order:
                while True:
                    product_id = int(input("ID produktu (0 = koniec): "))
                    if product_id == 0:
                        break
                    
                    product = self.company.get_product_by_id(product_id)
                    if product:
                        quantity = int(input("Ilość: "))
                        self.company.sell_product(order, product, quantity)
                    else:
                        print("❌ Produkt nie znaleziony!")
                
                order.complete_order()
                print(f"\n✅ {order.get_summary()}")
        
        except ValueError:
            print("❌ Błędne dane!")
        
        self.company.save_all_data()
        input("Naciśnij Enter, aby kontynuować...")
    
    def _view_orders(self) -> None:
        """Wyświetla zamówienia"""
        print("\n📋 ZAMÓWIENIA")
        print("-" * 60)
        orders = self.company.orders
        if orders:
            for order in orders:
                print(f"  {order.get_summary()}")
        else:
            print("  Brak zamówień w systemie")
        print()
        input("Naciśnij Enter, aby kontynuować...")
    
    def _view_my_sales(self) -> None:
        """Wyświetla moje sprzedaże"""
        if not isinstance(self.company.current_user, Employee):
            print("❌ Ta opcja jest dostępna tylko dla pracowników!")
            return
        
        print("\n💼 MOJE SPRZEDAŻE")
        print("-" * 60)
        perf = self.company.current_user.get_performance()
        print(f"Liczba sprzedaży: {perf['sales_count']}")
        print(f"Wartość sprzedaży: {perf['total_sales_value']:.2f} zł")
        print(f"Średnia sprzedaż: {perf['average_sale']:.2f} zł")
        print()
        input("Naciśnij Enter, aby kontynuować...")
    
    def _generate_report(self) -> None:
        """Generuje raport"""
        from report_generator import ReportGenerator
        
        print("\n📊 GENEROWANIE RAPORTU")
        print("-" * 60)
        
        generator = ReportGenerator()
        company_data = self.company.get_company_info()
        finances = self.company.data_manager.load_finances()
        
        if generator.generate_and_save_report(
            company_data,
            self.company.users,
            self.company.products,
            self.company.orders,
            finances
        ):
            print("✅ Raport został wygenerowany!")
        else:
            print("❌ Błąd przy generowaniu raportu!")
        
        input("Naciśnij Enter, aby kontynuować...")


def main():
    """Punkt wejścia aplikacji"""
    ui = UserInterface()
    ui.run()


if __name__ == "__main__":
    main()
