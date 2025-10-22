"""
Brand Manager - Handles vehicle brand logos and data
"""
import os
from PyQt6.QtGui import QPixmap

class BrandManager:
    """Manages vehicle brands and their logos"""
    
    BRANDS = [
        # Αυτοκίνητα - Ευρωπαϊκές
        "Abarth", "Alfa Romeo", "Aston Martin", "Audi", "Bentley", "BMW", 
        "Bugatti", "Citroën", "Dacia", "Ferrari", "Fiat", "Jaguar", "Lancia", 
        "Land Rover", "Lotus", "Maserati", "McLaren", "Mercedes-Benz", "Mini", 
        "Opel", "Peugeot", "Porsche", "Renault", "Rolls-Royce", "Rover", "Saab", 
        "Seat", "Skoda", "Smart", "Volkswagen", "Volvo",
        
        # Αυτοκίνητα - Αμερικανικές
        "Buick", "Cadillac", "Chevrolet", "Chrysler", "Dodge", "Ford", "GMC", 
        "Hummer", "Jeep", "Lincoln", "Pontiac", "Ram", "Tesla",
        
        # Αυτοκίνητα - Ασιατικές
        "Acura", "Daihatsu", "Datsun", "Honda", "Hyundai", "Infiniti", "Isuzu", 
        "Kia", "Lexus", "Mazda", "Mitsubishi", "Nissan", "Subaru", "Suzuki", "Toyota",
        
        # Αυτοκίνητα - Κινέζικες & Άλλες
        "BYD", "Chery",
        
        # Φορτηγά - Ευρωπαϊκά
        "DAF", "Iveco", "MAN", "Scania",
        
        # Φορτηγά - Αμερικανικά
        "Kenworth", "Mack", "Peterbilt",
        
        # Φορτηγά - Ασιατικά
        "Hino",
        
        # Μηχανές - Ιαπωνικές
        "Honda Motorcycles", "Kawasaki", "Suzuki Motorcycles", "Yamaha",
        
        # Μηχανές - Ευρωπαϊκές
        "Aprilia", "Ducati", "Husqvarna", "KTM", 
        "Piaggio", "Triumph", "Vespa", "Vespa", "SYM",
        
        # Μηχανές - Αμερικανικές
        "Harley-Davidson",
                
        # Λεωφορεία & Coaches
        "Irizar", "Setra", "Solaris", "Temsa", "Van Hool",
        
        # Γεωργικά & Κατασκευαστικά
        "Caterpillar", "JCB", "Deutz-Fahr", "Fendt", "John Deere",         
    ]
    
    @staticmethod
    def get_all_brands():
        """Get list of all brands"""
        return sorted(BrandManager.BRANDS)
    
    @staticmethod
    def get_brand_logo(brand_name):
        """Get brand logo pixmap"""
        if not brand_name:
            return BrandManager.get_default_logo()
        
        # Normalize brand name (uppercase, no spaces)
        normalized = brand_name.upper().replace(" ", "").replace("-", "")
        
        # Try exact match first
        logo_path = f"resources/brand/{brand_name}.png"
        if os.path.exists(logo_path):
            return QPixmap(logo_path)
        
        # Try normalized match
        logo_path = f"resources/brand/{normalized}.png"
        if os.path.exists(logo_path):
            return QPixmap(logo_path)
        
        # Try lowercase
        logo_path = f"resources/brand/{brand_name.lower()}.png"
        if os.path.exists(logo_path):
            return QPixmap(logo_path)
        
        # Return default
        return BrandManager.get_default_logo()
    
    @staticmethod
    def get_default_logo():
        """Get default car logo"""
        default_path = "resources/brand/default.png"
        if os.path.exists(default_path):
            return QPixmap(default_path)
        return QPixmap(64, 64)  # Empty pixmap
    
    @staticmethod
    def has_logo(brand_name):
        """Check if brand has a logo"""
        if not brand_name:
            return False
        
        normalized = brand_name.upper().replace(" ", "").replace("-", "")
        
        return (
            os.path.exists(f"resources/brand/{brand_name}.png") or
            os.path.exists(f"resources/brand/{normalized}.png") or
            os.path.exists(f"resources/brand/{brand_name.lower()}.png")
        )
