"""
Configuration file for vehicle types, fuel types, and colors
"""

class Config:
    """Static configuration for dropdowns and constants"""
    
    @staticmethod
    def get_vehicle_types():
        """Get list of vehicle types"""
        return [
            "Επιβατικό",
            "Φορτηγό",
            "Μοτοσικλέτα",
            "Λεωφορείο",
            "Φορτηγάκι",
            "SUV",
            "Van",
            "Minibus",
            "Γεωργικό",
            "Κατασκευαστικό"
        ]
    
    @staticmethod
    def get_fuel_types():
        """Get list of fuel types"""
        return [
            "Βενζίνη",
            "Πετρέλαιο",
            "Υγραέριο (LPG)",
            "Φυσικό Αέριο (CNG)",
            "Ηλεκτρικό",
            "Υβριδικό (Βενζίνη)",
            "Υβριδικό (Πετρέλαιο)",
            "Plug-in Hybrid"
        ]
    
    @staticmethod
    def get_colors():
        """Get list of colors"""
        return [
            "Άσπρο",
            "Λευκό",
            "Μαύρο",
            "Γκρι",
            "Ασημί",
            "Κόκκινο",
            "Μπλε",
            "Πράσινο",
            "Κίτρινο",
            "Πορτοκαλί",
            "Καφέ",
            "Μπεζ",
            "Χρυσό",
            "Μπορντό",
            "Άλλο"
        ]
