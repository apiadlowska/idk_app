"""
Klasa ReportGenerator - generuje raporty
Poziom: Klasa 2 LO rozszerzona
"""

from typing import List, Dict, Any
from datetime import datetime
import os

class ReportGenerator:
    """
    Klasa do generowania raportów tekstowych.
    Tworzy raporty zawierające informacje o firmie i pracownikach.
    """
    
    def __init__(self, reports_dir: str = "data/reports") -> None:
        """
        Inicjalizacja
        
        Args:
            reports_dir (str): Folder do zapisu raportów
        """
        self.reports_dir = reports_dir
        self._ensure_reports_directory()
    
    def _ensure_reports_directory(self) -> None:
        """Tworzy folder reports jeśli nie istnieje"""
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    def generate_company_report(self, company_data: Dict, users: List, products: List, orders: List, finances: Dict) -> str:
        """
        Generuje pełny raport o firmie
        
        Args:
            company_data (Dict): Dane firmy
            users (List): Lista użytkowników
            products (List): Lista produktów
            orders (List): Lista zamówień
            finances (Dict): Dane finansowe
            
        Returns:
            str: Tekst raportu
        """
        report = self._generate_header(company_data["company_name"])
        report += self._generate_company_section(company_data)
        report += self._generate_users_section(users)
        report += self._generate_products_section(products)
        report += self._generate_orders_section(orders)
        report += self._generate_finances_section(finances)
        report += self._generate_footer()
        
        return report
    
    def _generate_header(self, company_name: str) -> str:
        """Generuje nagłówek raportu"""
        header = "\n" + "=" * 80 + "\n"
        header += f"RAPORT FIRMY: {company_name.upper()}\n"
        header += f"Data wygenerowania: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += "=" * 80 + "\n\n"
        return header
    
    def _generate_company_section(self, company_data: Dict) -> str:
        """Generuje sekcję informacji o firmie"""
        section = "📊 INFORMACJE O FIRMIE\n"
        section += "-" * 80 + "\n"
        section += f"Nazwa firmy:        {company_data['company_name']}\n"
        section += f"Liczba pracowników: {company_data['total_users']}\n"
        section += f"Liczba produktów:   {company_data['total_products']}\n"
        section += f"Liczba zamówień:    {company_data['total_orders']}\n"
        section += "\n"
        return section
    
    def _generate_users_section(self, users: List) -> str:
        """Generuje sekcję użytkowników"""
        section = "👥 PRACOWNICY I UŻYTKOWNICY\n"
        section += "-" * 80 + "\n"
        
        if not users:
            section += "Brak użytkowników w systemie.\n\n"
            return section
        
        admins = [u for u in users if u.role == "admin"]
        sellers = [u for u in users if u.role == "seller"]
        employees = [u for u in users if u.role == "employee"]
        
        # Administratorzy
        if admins:
            section += "ADMINISTRATORZY:\n"
            for admin in admins:
                status = "✅ Aktywny" if admin.is_active else "❌ Nieaktywny"
                section += f"  • {admin.name} ({admin.email}) - {status}\n"
            section += "\n"
        
        # Sprzedawcy
        if sellers:
            section += "SPRZEDAWCY:\n"
            for seller in sellers:
                status = "✅ Aktywny" if seller.is_active else "❌ Nieaktywny"
                section += f"  • {seller.name} ({seller.email}) - {status}\n"
                section += f"    Sprzedaży: {seller.sales_count} | Wartość: {seller.total_sales_value:.2f} zł\n"
                section += f"    Pensja: {seller.salary:.2f} zł\n"
            section += "\n"
        
        # Pracownicy
        if employees:
            section += "PRACOWNICY:\n"
            for employee in employees:
                status = "✅ Aktywny" if employee.is_active else "❌ Nieaktywny"
                section += f"  • {employee.name} ({employee.email}) - {status}\n"
                section += f"    Pensja: {employee.salary:.2f} zł\n"
            section += "\n"
        
        return section
    
    def _generate_products_section(self, products: List) -> str:
        """Generuje sekcję produktów"""
        section = "📦 PRODUKTY\n"
        section += "-" * 80 + "\n"
        
        if not products:
            section += "Brak produktów w systemie.\n\n"
            return section
        
        total_stock_value = 0
        for product in products:
            stock_value = product.get_total_value()
            total_stock_value += stock_value
            section += f"  • {product.name}\n"
            section += f"    Cena: {product.price:.2f} zł\n"
            section += f"    Magazyn: {product.stock_quantity} szt.\n"
            section += f"    Sprzedano: {product.units_sold} szt.\n"
            section += f"    Wartość magazynu: {stock_value:.2f} zł\n\n"
        
        section += f"Całkowita wartość magazynu: {total_stock_value:.2f} zł\n\n"
        return section
    
    def _generate_orders_section(self, orders: List) -> str:
        """Generuje sekcję zamówień"""
        section = "📋 ZAMÓWIENIA\n"
        section += "-" * 80 + "\n"
        
        if not orders:
            section += "Brak zamówień w systemie.\n\n"
            return section
        
        completed_orders = [o for o in orders if o.status == "completed"]
        pending_orders = [o for o in orders if o.status == "pending"]
        cancelled_orders = [o for o in orders if o.status == "cancelled"]
        
        total_value = sum(o.total_value for o in orders)
        
        section += f"Razem zamówień: {len(orders)}\n"
        section += f"  • Ukończone: {len(completed_orders)}\n"
        section += f"  • Oczekujące: {len(pending_orders)}\n"
        section += f"  • Anulowane: {len(cancelled_orders)}\n"
        section += f"Całkowita wartość zamówień: {total_value:.2f} zł\n"
        section += "\n"
        
        if completed_orders:
            section += "Ostatnie ukończone zamówienia:\n"
            for order in completed_orders[-5:]:  # Ostatnie 5
                section += f"  • Zamówienie #{order.order_id}: {order.customer_name} - {order.total_value:.2f} zł ({order.order_date})\n"
            section += "\n"
        
        return section
    
    def _generate_finances_section(self, finances: Dict) -> str:
        """Generuje sekcję finansów"""
        section = "💰 FINANSE\n"
        section += "-" * 80 + "\n"
        section += f"Saldo firmy: {finances['balance']:.2f} {finances['currency']}\n"
        section += f"Całkowity przychód: {finances['total_revenue']:.2f} zł\n"
        section += f"Całkowite wydatki: {finances['total_expenses']:.2f} zł\n"
        section += "\n"
        return section
    
    def _generate_footer(self) -> str:
        """Generuje stopkę raportu"""
        footer = "=" * 80 + "\n"
        footer += "Raport został wygenerowany automatycznie przez System Zarządzania Firmą\n"
        footer += "=" * 80 + "\n\n"
        return footer
    
    def save_report(self, filename: str, content: str) -> bool:
        """
        Zapisuje raport do pliku
        
        Args:
            filename (str): Nazwa pliku
            content (str): Zawartość raportu
            
        Returns:
            bool: Czy zapis się powiódł
        """
        filepath = os.path.join(self.reports_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Raport zapisany do: {filepath}")
            return True
        except IOError as e:
            print(f"❌ Błąd zapisu raportu: {e}")
            return False
    
    def generate_and_save_report(self, company_data: Dict, users: List, products: List, orders: List, finances: Dict) -> bool:
        """
        Generuje i zapisuje raport
        
        Args:
            Wszystkie niezbędne dane
            
        Returns:
            bool: Czy operacja się powiodła
        """
        report = self.generate_company_report(company_data, users, products, orders, finances)
        filename = f"raport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        return self.save_report(filename, report)
