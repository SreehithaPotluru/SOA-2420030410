def choose_response(analysis: dict) -> dict:
    score = int(analysis.get("risk_score", 0))
    if score >= 60:
        action = "BLOCK_AND_ALERT"
        message = "High risk: do not open this link. Report it to your security team."
    elif score >= 30:
        action = "WARN_USER"
        message = "Suspicious link: avoid entering passwords or personal information."
    else:
        action = "ALLOW_WITH_CAUTION"
        message = "No strong warning signs were detected. Stay cautious."
    return {
        "action": action,
        "message": message,
        "blocked": score >= 60,
        "simulated": True
    }
