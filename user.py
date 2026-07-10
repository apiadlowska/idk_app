"""
Klasa User - klasa bazowa dla wszystkich użytkowników
Poziom: Klasa 2 LO rozszerzona
"""

from typing import Dict, Any

class User:
    """
    Klasa reprezentująca użytkownika systemu.
    Jest klasą bazową dla Admin i Employee (DZIEDZICZENIE).
    """
    
    def __init__(self, user_id: int, name: str, email: str, role: str, password: str) -> None:
        """
        Inicjalizacja użytkownika
        
        Args:
            user_id (int): Unikalny ID użytkownika
            name (str): Imię i nazwisko
            email (str): Email
            role (str): Rola (admin, employee, seller)
            password (str): Hasło
        """
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.password = password
        self.is_active = True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Konwertuje użytkownika na słownik (do zapisu JSON)
        
        Returns:
            Dict: Słownik z danymi użytkownika
        """
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "password": self.password,
            "is_active": self.is_active
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'User':
        """
        Konwertuje słownik na użytkownika (z odczytu JSON)
        
        Args:
            data (Dict): Słownik z danymi
            
        Returns:
            User: Nowy obiekt User
        """
        user = User(
            data["user_id"],
            data["name"],
            data["email"],
            data["role"],
            data["password"]
        )
        user.is_active = data.get("is_active", True)
        return user
    
    def get_info(self) -> str:
        """
        Zwraca informacje o użytkowniku
        
        Returns:
            str: Sformatowany tekst z danymi
        """
        status = "✅ Aktywny" if self.is_active else "❌ Nieaktywny"
        return f"{self.name} ({self.role}) - {self.email} [{status}]"
    
    def change_password(self, old_password: str, new_password: str) -> bool:
        """
        Zmienia hasło użytkownika
        
        Args:
            old_password (str): Stare hasło
            new_password (str): Nowe hasło
            
        Returns:
            bool: Czy zmiana się powiodła
        """
        if self.password == old_password:
            self.password = new_password
            print(f"✅ Zmieniono hasło dla {self.name}")
            return True
        else:
            print("❌ Stare hasło jest nieprawidłowe!")
            return False
