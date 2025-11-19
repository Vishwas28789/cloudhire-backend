from typing import Optional

CLOUD_ROLES = [
    "cloud engineer",
    "cloud architect",
    "cloud support",
    "devops engineer",
    "devops",
    "cloud intern",
    "system administrator",
    "sysadmin",
    "it support",
    "tech support",
    "technical support",
    "noc engineer",
    "helpdesk",
    "help desk",
    "security analyst",
    "infrastructure engineer",
    "site reliability",
    "sre"
]

CODING_HEAVY_ROLES = [
    "java developer",
    "python developer",
    "software developer",
    "software engineer",
    "full stack",
    "full-stack",
    "backend developer",
    "backend engineer",
    "frontend developer",
    "frontend engineer",
    "web developer",
    "ai engineer",
    "ml engineer",
    "machine learning",
    "data scientist",
    "app developer",
    "mobile developer",
    "ios developer",
    "android developer"
]

ROLE_CLASSIFICATIONS = {
    "cloud architect": ["cloud architect", "principal cloud", "senior cloud architect"],
    "cloud engineer": ["cloud engineer", "aws engineer", "azure engineer", "gcp engineer"],
    "cloud support": ["cloud support", "cloud operations", "cloud specialist"],
    "devops": ["devops", "devops engineer", "devsecops"],
    "cloud intern": ["cloud intern", "cloud apprentice"],
    "sysadmin": ["system administrator", "sysadmin", "systems engineer"],
    "it support": ["it support", "it specialist", "it technician"],
    "tech support": ["tech support", "technical support", "customer support engineer"],
    "noc engineer": ["noc engineer", "network operations"],
    "helpdesk": ["helpdesk", "help desk", "service desk"],
    "security analyst": ["security analyst", "cybersecurity analyst", "infosec"]
}


def classify_job(title: str, description: str) -> Optional[str]:
    title_lower = title.lower()
    desc_lower = description.lower()
    combined = f"{title_lower} {desc_lower}"
    
    for coding_role in CODING_HEAVY_ROLES:
        if coding_role in title_lower:
            return None
    
    for classification, keywords in ROLE_CLASSIFICATIONS.items():
        for keyword in keywords:
            if keyword in title_lower:
                return classification
    
    for classification, keywords in ROLE_CLASSIFICATIONS.items():
        for keyword in keywords:
            if keyword in desc_lower:
                return classification
    
    return None


def is_excluded_role(title: str, description: str, excluded_roles: list = None) -> bool:
    if excluded_roles is None:
        excluded_roles = []
    
    title_lower = title.lower()
    desc_lower = description.lower()
    
    for coding_role in CODING_HEAVY_ROLES:
        if coding_role in title_lower:
            return True
    
    for excluded in excluded_roles:
        if excluded.lower() in title_lower or excluded.lower() in desc_lower:
            return True
    
    return False
