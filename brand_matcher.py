import json
import re
from typing import Dict, List, Set
from config import Config

class BrandMatcher:
    def __init__(self):
        self.brands = self._load_brands()
        self.brand_patterns = self._compile_patterns()
    
    def _load_brands(self) -> Dict[str, List[str]]:
        try:
            with open(Config.BRANDS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Brands file {Config.BRANDS_FILE} not found")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in {Config.BRANDS_FILE}")
    
    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        patterns = {}
        
        for category, brand_list in self.brands.items():
            for brand in brand_list:
                escaped_brand = re.escape(brand.lower())
                pattern = re.compile(r'\b' + escaped_brand + r'\b', re.IGNORECASE)
                patterns[brand.lower()] = pattern
        
        return patterns
    
    def find_brands_in_text(self, text: str) -> Set[str]:
        found_brands = set()
        text_lower = text.lower()
        
        for brand, pattern in self.brand_patterns.items():
            if pattern.search(text_lower):
                found_brands.add(brand)
        
        return found_brands
    
    def extract_brand_mentions(self, texts: List[str]) -> Dict[str, List[str]]:
        brand_mentions = {}
        
        for text in texts:
            if not text or len(text.strip()) < 3:
                continue
                
            found_brands = self.find_brands_in_text(text)
            
            for brand in found_brands:
                if brand not in brand_mentions:
                    brand_mentions[brand] = []
                brand_mentions[brand].append(text)
        
        return brand_mentions
    
    def get_all_brands(self) -> List[str]:
        all_brands = []
        for brand_list in self.brands.values():
            all_brands.extend([brand.lower() for brand in brand_list])
        return sorted(set(all_brands))
    
    def get_brand_category(self, brand: str) -> str:
        brand_lower = brand.lower()
        for category, brand_list in self.brands.items():
            if brand_lower in [b.lower() for b in brand_list]:
                return category
        return "unknown"