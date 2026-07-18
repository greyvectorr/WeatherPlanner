"""
ActivityRiskAnalyzer - decides how risky a chosen activity is against a
Forecast, using fixed, explainable rules (see config.ACTIVITIES for the
thresholds), and can optionally ask Gemini to explain that result in
plain language.

Why rules decide the risk level instead of the AI:
  - It's testable without an API key.
  - It's auditable - every score can be traced back to specific numbers
    in the forecast, rather than trusting an LLM's judgement call.
  - The AI's job becomes communication, not decision-making, which is a
    safer division of responsibility for something safety-related.
"""
