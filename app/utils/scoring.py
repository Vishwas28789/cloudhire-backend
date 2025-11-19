from typing import Dict, Any, Optional, List


def calculate_job_score(
    job_title: str,
    job_description: str,
    job_classification: Optional[str],
    job_location: str,
    job_country: Optional[str],
    has_visa: bool,
    salary_min: Optional[int],
    salary_max: Optional[int],
    user_role_preferences: List[str],
    user_country_preferences: List[str],
    user_min_salary: Optional[int],
    user_visa_required: bool
) -> Dict[str, Any]:
    
    score = 0
    breakdown = {}
    
    role_match_score = 0
    if job_classification and user_role_preferences:
        for pref in user_role_preferences:
            if pref.lower() in job_classification.lower():
                role_match_score = 30
                break
        if role_match_score == 0:
            for pref in user_role_preferences:
                if pref.lower() in job_title.lower():
                    role_match_score = 20
                    break
    else:
        role_match_score = 15
    breakdown["role_match"] = role_match_score
    score += role_match_score
    
    cloud_keywords = ["cloud", "aws", "azure", "gcp", "kubernetes", "docker", "terraform"]
    cloud_count = sum(1 for kw in cloud_keywords if kw in job_description.lower())
    cloud_score = min(cloud_count * 3, 20)
    breakdown["cloud_match"] = cloud_score
    score += cloud_score
    
    visa_score = 0
    if user_visa_required:
        if has_visa:
            visa_score = 25
        else:
            visa_score = 0
    else:
        visa_score = 15
    breakdown["visa_match"] = visa_score
    score += visa_score
    
    salary_score = 0
    if salary_min and user_min_salary:
        if salary_min >= user_min_salary:
            salary_score = 15
        elif salary_min >= user_min_salary * 0.8:
            salary_score = 10
        else:
            salary_score = 5
    else:
        salary_score = 10
    breakdown["salary_match"] = salary_score
    score += salary_score
    
    location_score = 0
    if job_country and user_country_preferences:
        for pref in user_country_preferences:
            if pref.lower() in job_country.lower() or pref.lower() in job_location.lower():
                location_score = 15
                break
    else:
        location_score = 5
    breakdown["location_match"] = location_score
    score += location_score
    
    jd_quality_score = 0
    desc_length = len(job_description)
    if desc_length > 1000:
        jd_quality_score = 10
    elif desc_length > 500:
        jd_quality_score = 7
    else:
        jd_quality_score = 4
    breakdown["jd_quality"] = jd_quality_score
    score += jd_quality_score
    
    final_score = min(score, 100)
    
    return {
        "score": final_score,
        "breakdown": breakdown
    }
