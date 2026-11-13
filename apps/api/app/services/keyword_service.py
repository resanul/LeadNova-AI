from typing import Dict, Any, List


def generate_keyword_intelligence(city_name: str, niche_name: str) -> Dict[str, Any]:
    """
    Generates structured keyword intelligence for local service arbitrage:
    - Primary keywords
    - Secondary keywords
    - Emergency intent keywords
    - Commercial intent keywords
    - Long-tail keywords
    - CPC estimates & ranking difficulty
    """
    clean_city = city_name.strip()
    clean_niche = niche_name.strip().lower()

    primary_keywords = [
        f"{clean_niche} in {clean_city}",
        f"{clean_city} {clean_niche}",
        f"best {clean_niche} {clean_city}",
    ]

    emergency_keywords = [
        f"emergency {clean_niche} {clean_city}",
        f"24/7 {clean_niche} near me",
        f"urgent {clean_niche} service {clean_city}",
        f"same day {clean_niche} {clean_city}",
    ]

    commercial_keywords = [
        f"{clean_niche} cost {clean_city}",
        f"licensed {clean_niche} contractor {clean_city}",
        f"affordable {clean_niche} {clean_city}",
        f"hire {clean_niche} in {clean_city}",
    ]

    long_tail_keywords = [
        f"how much does {clean_niche} cost in {clean_city}",
        f"top rated {clean_niche} companies in {clean_city}",
        f"reliable local {clean_niche} experts near {clean_city}",
    ]

    # Benchmark CPC indicators based on service urgency
    cpc_benchmarks = {
        "water damage restoration": 45.0,
        "emergency plumbing": 35.0,
        "roof repair": 28.0,
        "roof replacement": 55.0,
        "hvac repair": 25.0,
        "emergency ac repair": 30.0,
        "mold remediation": 40.0,
        "emergency tree removal": 32.0,
        "electrical repair": 22.0,
        "fire damage restoration": 65.0,
    }
    est_cpc = cpc_benchmarks.get(clean_niche, 20.0)

    return {
        "city": clean_city,
        "niche": niche_name,
        "primary_keywords": primary_keywords,
        "emergency_keywords": emergency_keywords,
        "commercial_keywords": commercial_keywords,
        "long_tail_keywords": long_tail_keywords,
        "estimated_monthly_searches": 450,
        "estimated_cpc_usd": est_cpc,
        "ranking_difficulty_score": 42.0,  # 0-100 difficulty
        "search_intent": "high_commercial_emergency",
        "seasonality": "year_round_with_peak_weather_events",
    }
