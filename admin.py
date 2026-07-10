"""
Klasa Admin - dziedziczy po User
Poziom: Klasa 2 LO rozszerzona
"""

from typing import List, Dict, Any, Optional
from user import User

class Admin(User):
    """
    Klasa Admin - dziedziczy po User (DZIEDZICZENIE).
    Admin ma uprawnienia do zarządzania wszystkimi użytkownikami i danymi.
    """
    
    def __init__(self, user_id: int, name: str, email: str, password: str) -> None:
        """
        Inicjalizacja Admina
        
        Args:
            user_id (int): Unikalny ID
            name (str): Imię i nazwisko
            email (str): Email
            password (str): Hasło
        """
        super().__init__(user_id, name, email, "admin", password)
        self.permissions = [
            "view_users",
            "edit_users", 
            "delete_users",
            "manage_roles",
            "view_finances",
            "view_reports",
            "manage_products",
            "view_all_orders"
        ]
    
    def add_user(self, user_list: List[User], new_user: User) -> bool:
        """
        Dodaje nowego użytkownika
        
        Args:
            user_list (List[User]): Lista użytkowników
            new_user (User): Nowy użytkownik do dodania
            
        Returns:
            bool: Czy operacja się powiodła
        """
        if new_user.user_id not in [u.user_id for u in user_list]:
            user_list.append(new_user)
            print(f"✅ Admin {self.name} dodał użytkownika: {new_user.name}")
            return True
        else:
            print(f"❌ Użytkownik z ID {new_user.user_id} już istnieje!")
            return False
    
    def edit_user_role(self, user: User, new_role: str) -> bool:
        """
        Zmienia rolę użytkownika
        
        Args:
            user (User): Użytkownik
            new_role (str): Nowa rola
            
        Returns:
            bool: Czy operacja się powiodła
        """
        valid_roles = ["admin", "employee", "seller"]
        if new_role not in valid_roles:
            print(f"❌ Nieprawidłowa rola! Dostępne: {valid_roles}")
            return False
        
        old_role = user.role
        user.role = new_role
        print(f"✅ Admin {self.name} zmienił rolę {user.name} z '{old_role}' na '{new_role}'")
        return True
    
    def edit_user_data(self, user: User, **kwargs) -> bool:
        """
        Zmienia dane użytkownika
        
        Args:
            user (User): Użytkownik
            **kwargs: Atrybuty do zmiany (name, email, itp.)
            
        Returns:
            bool: Czy operacja się powiodła
        """
        for key, value in kwargs.items():
            if hasattr(user, key):
                old_value = getattr(user, key)
                setattr(user, key, value)
                print(f"✅ Admin {self.name} zmienił {key} dla {user.name} z '{old_value}' na '{value}'")
            else:
                print(f"⚠️ Atrybut {key} nie istnieje!")
                return False
        return True
    
    def deactivate_user(self, user: User) -> bool:
        """
        Deaktywuje użytkownika
        
        Args:
            user (User): Użytkownik do deaktywacji
            
        Returns:
            bool: Czy operacja się powiodła
        """
        if user.is_active:
            user.is_active = False
            print(f"✅ Admin {self.name} deaktywował użytkownika: {user.name}")
            return True
        else:
            print(f"⚠️ Użytkownik {user.name} jest już nieaktywny!")
            return False
    
    def activate_user(self, user: User) -> bool:
        """
        Aktywuje użytkownika
        
        Args:
            user (User): Użytkownik do aktywacji
            
        Returns:
            bool: Czy operacja się powiodła
        """
        if not user.is_active:
            user.is_active = True
            print(f"✅ Admin {self.name} aktywował użytkownika: {user.name}")
            return True
        else:
            print(f"⚠️ Użytkownik {user.name} jest już aktywny!")
            return False
    
    def reset_user_password(self, user: User, new_password: str) -> bool:
        """
        Resetuje hasło użytkownika
        
        Args:
            user (User): Użytkownik
            new_password (str): Nowe hasło
            
        Returns:
            bool: Czy operacja się powiodła
        """
        if len(new_password) < 4:
            print("❌ Hasło musi mieć co najmniej 4 znaki!")
            return False
        
        user.password = new_password
        print(f"✅ Admin {self.name} zresetował hasło dla {user.name}")
        return True
    
    def get_user_info(self, users: List[User]) -> str:
        """
        Zwraca informacje o wszystkich użytkownikach
        
        Args:
            users (List[User]): Lista użytkowników
            
        Returns:
            str: Sformatowana lista użytkowników
        """
        info = f"\n📋 Lista użytkowników ({len(users)}):\n"
        info += "=" * 60 + "\n"
        for user in users:
            info += f"{user.get_info()}\n"
        return info
    
    def to_dict(self) -> Dict[str, Any]:
        """Konwertuje na słownik"""
        data = super().to_dict()
        data["permissions"] = self.permissions
        return data
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Admin':
        """Konwertuje ze słownika"""
        admin = Admin(
            data["user_id"],
            data["name"],
            data["email"],
            data["password"]
        )
        admin.is_active = data.get("is_active", True)
        return admin
