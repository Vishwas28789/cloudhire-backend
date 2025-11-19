from typing import List, Tuple

VISA_KEYWORDS = [
    "visa sponsorship",
    "visa sponsor",
    "work permit",
    "work authorization",
    "relocation",
    "relocation assistance",
    "relocation package",
    "h1b",
    "h-1b",
    "sponsorship available",
    "will sponsor",
    "can sponsor",
    "provides sponsorship"
]


def detect_visa_sponsorship(description: str) -> Tuple[bool, List[str]]:
    desc_lower = description.lower()
    found_keywords = []
    
    for keyword in VISA_KEYWORDS:
        if keyword in desc_lower:
            found_keywords.append(keyword)
    
    has_visa = len(found_keywords) > 0
    
    return has_visa, found_keywords
