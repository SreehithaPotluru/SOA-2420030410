import re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = {
    "login", "verify", "verification", "account", "update", "secure",
    "banking", "password", "confirm", "wallet", "signin", "bonus",
    "gift", "free", "urgent", "suspended", "recover"
}

def extract_features(url: str) -> dict:
    value = url.strip()
    parsed = urlparse(value if "://" in value else "http://" + value)
    host = parsed.netloc.lower().split("@")[-1].split(":")[0]
    path = (parsed.path + " " + parsed.query).lower()
    full = value.lower()
    return {
        "url_length": len(value),
        "dot_count": value.count("."),
        "hyphen_count": value.count("-"),
        "at_count": value.count("@"),
        "question_count": value.count("?"),
        "equal_count": value.count("="),
        "digit_count": sum(ch.isdigit() for ch in value),
        "has_https": int(full.startswith("https://")),
        "has_ip": int(bool(re.match(r"^(?:https?://)?(?:\d{1,3}\.){3}\d{1,3}", full))),
        "subdomain_count": max(0, len(host.split(".")) - 2),
        "suspicious_word_count": sum(word in full for word in SUSPICIOUS_WORDS),
        "has_punycode": int("xn--" in host),
        "has_shortener_hint": int(any(x in host for x in ["bit.ly", "tinyurl", "t.co", "goo.gl", "ow.ly"])),
        "host": host,
    }

def analyze_url(url: str) -> dict:
    if not url or not url.strip():
        raise ValueError("Please enter a URL.")
    value = url.strip()
    if len(value) > 2048:
        raise ValueError("URL is too long.")
    f = extract_features(value)
    reasons = []
    score = 0
    if not f["has_https"]:
        score += 12
        reasons.append("The URL does not use HTTPS.")
    if f["has_ip"]:
        score += 25
        reasons.append("The address uses an IP address instead of a normal domain.")
    if f["at_count"]:
        score += 20
        reasons.append("The URL contains an @ symbol, which can obscure the destination.")
    if f["suspicious_word_count"]:
        score += min(30, 8 * f["suspicious_word_count"])
        reasons.append("The URL contains words commonly used in deceptive links.")
    if f["url_length"] > 100:
        score += 10
        reasons.append("The URL is unusually long.")
    if f["subdomain_count"] >= 3:
        score += 10
        reasons.append("The domain has several subdomain levels.")
    if f["has_punycode"]:
        score += 15
        reasons.append("The domain contains punycode, which can be used in lookalike domains.")
    if f["has_shortener_hint"]:
        score += 10
        reasons.append("The URL appears to use a link-shortening service.")
    score = min(score, 100)
    level = "High" if score >= 60 else "Medium" if score >= 30 else "Low"
    prediction = "Potentially phishing" if score >= 30 else "Likely legitimate"
    if not reasons:
        reasons.append("No obvious suspicious patterns were detected by the basic checks.")
    return {
        "url": value,
        "prediction": prediction,
        "risk_score": score,
        "risk_level": level,
        "reasons": reasons,
        "features": {k: v for k, v in f.items() if k != "host"},
        "note": "This is a heuristic screening result, not a guarantee. Verify links independently."
    }
