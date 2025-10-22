import json
import os

class Translator:
    def __init__(self):
        self.current_language = "el"
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Load translation files"""
        for lang in ["el", "en"]:
            file_path = f"resources/translations/{lang}.json"
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.translations[lang] = json.load(f)
    
    def set_language(self, language):
        """Set current language"""
        if language in self.translations:
            self.current_language = language
    
    def get(self, key_path):
        """Get translation by key path (e.g., 'vehicles.search')"""
        keys = key_path.split('.')
        value = self.translations.get(self.current_language, {})
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, key_path)
            else:
                return key_path
        
        return value

# Global translator instance
translator = Translator()
