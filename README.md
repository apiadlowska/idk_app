# 🏢 System Zarządzania Firmą - IDK Company

Projekt na ocenę z informatyki - Klasa 2 LO Rozszerzona

## 📋 Opis projektu

System zarządzania firmą pozwalający na:
- Logowanie się użytkowników (Admin, Sprzedawca, Pracownik)
- Zarządzanie pracownikami i ich uprawnieniami
- Zarządzanie produktami i magazynem
- Obsługę zamówień i sprzedaży
- Śledzenie finansów firmy
- Generowanie raportów

## 📁 Struktura projektu

```
idk_app/
├── main.py                  # Punkt wejścia aplikacji
├── ui.py                    # Interfejs użytkownika
├── user.py                  # Klasa bazowa User
├── admin.py                 # Klasa Admin (DZIEDZICZENIE)
├── employee.py              # Klasa Employee (DZIEDZICZENIE)
├── product.py               # Klasa Product
├── order.py                 # Klasa Order (KOMPOZYCJA)
├── company.py               # Klasa Company - zarządzanie
├── data_manager.py          # Obsługa JSON
├── report_generator.py      # Generowanie raportów
├── README.md                # Ten plik
└── data/                    # Folder z plikami JSON
    ├── users.json
    ├── products.json
    ├── orders.json
    ├── finances.json
    └── reports/             # Folder z raportami
```

## 🎯 Spełnione wymagania

### ✅ Ocena 2
- [x] Logowanie do programu (Admin, Sprzedawca, Pracownik)
- [x] Prosty interfejs tekstowy (cmdline)

### ✅ Ocena 3
- [x] Admin może zmieniać dane użytkowników
- [x] Admin może zarządzać uprawnieniami

### ✅ Ocena 4
- [x] Użyto **DZIEDZICZENIA** (Admin i Employee dziedziczą po User)
- [x] Użyto **KOMPOZYCJI** (Order zawiera Products)

### ✅ Ocena 5
- [x] System zawiera 3 produkty (Laptop, Smartphone, Tablet)
- [x] Sprzedawcy mogą zamawać i sprzedawać produkty
- [x] Plik z finansami firmy (`finances.json`)

### ✅ Ocena 6
- [x] Raport tekstowy zawierający:
  - Dane o firmie
  - Listę pracowników
  - Stan produktów
  - Historię zamówień
  - Informacje finansowe

## 💾 Format danych

**Wszystkie dane są zapisywane w formacie JSON** (nie Pickle, CSV, Database, Text)

### users.json
```json
[
  {
    "user_id": 1,
    "name": "Anna Admin",
    "email": "anna@idk.pl",
    "role": "admin",
    "password": "admin123",
    "is_active": true,
    "permissions": [...]
  }
]
```

### finances.json
```json
{
  "company_name": "IDK Company",
  "balance": 50000.0,
  "currency": "PLN",
  "total_revenue": 0.0,
  "total_expenses": 0.0
}
```

## 🚀 Jak uruchomić

```bash
python main.py
```

## 👤 Domyślni użytkownicy

| Email | Hasło | Rola |
|-------|-------|------|
| anna@idk.pl | admin123 | Admin |
| piotr@idk.pl | seller123 | Sprzedawca |
| maria@idk.pl | seller123 | Sprzedawca |

## 📚 Techniczne szczegóły

### Dziedziczenie
- `User` - klasa bazowa
  - `Admin(User)` - dziedziczy, dodaje uprawnienia admina
  - `Employee(User)` - dziedziczy, dodaje uprawnienia pracownika

### Kompozycja
- `Order` - zawiera listę `items` (produkty)
- Każde zamówienie zawiera wiele produktów

### Type Hints
- Wszystkie funkcje mają adnotacje typów (klasa 2 LO rozszerzona)

### Obsługa JSON
- `DataManager` - klasa do zarządzania JSON
- Wszystkie obiekty mają metody `to_dict()` i `from_dict()`

## 📝 Notatki

- Kod podzielony na **osobne pliki**
- Każda klasa w oddzielnym pliku
- Wszystkie dane w **formacie JSON**
- Bezpieczeństwo: hasła przechowywane w JSON (w rzeczywistej aplikacji byłyby hashowane)

---

**Opracował/a:** Student Klasy 2 LO  
**Data:** 2024  
**Projekt:** System Zarządzania Firmą
