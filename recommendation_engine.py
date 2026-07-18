"""
RecommendationEngine - takes an ActivityRiskAnalyzer result and turns it
into things a user can actually act on: a recommended time, a packing
checklist, and plain-language safety advice.
"""
from config import ACTIVITIES


class RecommendationEngine:
    """Builds actionable recommendations from a risk analysis result."""
    
    def __init__(self, activity, analysis):
        """
        Args:
            activity: The activity name, e.g. "Football" (must be a key
                in config.ACTIVITIES).
            analysis: The dict returned by ActivityRiskAnalyzer.analyze_day().
        """
        
        self.activity = activity
        self.analysis = analysis
        self.profile = ACTIVITIES[activity]
        
    
    def best_time_recommendation(self):
        """Describe the best time window found for this activity today.

        Returns:
            A human-readable sentence naming the best time and why.
        """
        
        best_entry, best_score, best_reasons = self.analysis["best_hour"]
        time_str = best_entry["time"].strftime("%A, %I:%M %p")
        # In the context of time formatting, %A represents the full weekday 
        # name (e.g., "Sunday"), while %I indicates the hour in 12-hour format
        # (e.g., "01"). %M shows the minutes, and %p indicates the AM/PM 
        # designation (e.g., "AM" or "PM").
        description = best_entry["weather_description"].lower()
        
        if best_score == 0:
            return (
                f"{time_str} looks ideal - {description}, "
                f"{best_entry['temperature']}\u00b0C."
            )
        return (
            f"{time_str} is your best available window, though not perfect"
            f"{description}, {best_entry['temperature']}\u00b0C."
        )
        
        
    def packing_checklist(self):
        """Build a packing list: activity basics plus weather-driven extras.

        The weather-driven items are based on the WORST hour in the day's
        window rather than the best one - if conditions could deteriorate
        during the activity, it's better to have packed for that than to
        be caught out.

        Returns:
            A list of item strings.
        """
        
        checklist = list(self.profile["base_packing"])
        worst_entry = self.analysis["worst_hour"][0]
        already_packed = " ".join(checklist).lower()
        
        if worst_entry["precip_probability"] > 40:
            checklist.append("Umbrella or Rain Jacket")
        if worst_entry["uv_index"] >= 6 and "sunscreen" not in already_packed:
            checklist.append("Sunscreen (since high UV is expected)")
        if worst_entry["wind_speed"] > 30:
            checklist.append("Windbreaker")
        if worst_entry["temperature"] >= 32:
            checklist.append("Extra water (since high heat is expected)")
        if worst_entry["temperature"] <= 12:
            checklist.append("Warm layers (cool temperatures expected)")
            
        return checklist
    
    
    def safety_advice(self):
        """Produce plain-language safety advice for the day.

        Returns:
            A list of advice strings. Always has at least one entry, even
            when conditions are fine, so the UI never shows an empty section.
        """
        
        advice = []
        worst_entry, worst_score, worst_reasons = self.analysis["worst_hour"]
        
        if worst_score >= 3:
            time_str = worst_entry["time"].strftime("%I:%M %p")
            advice.append(
                f"Try to avoid being out around {time_str} - conditions are "
                f"noticeably worse then."
            )
            
        for reason in worst_reasons:
            advice.append(f"Watch Out: {reason}.")
            
        if not advice:
            advice.append("No significant weather concerns for this activity today.")
            
        return advice
    