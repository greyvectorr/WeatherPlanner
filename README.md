# 🌦️ Weather Risk & Outdoor Activity Planner

A Streamlit app that tells you whether it's safe to go outside — for a specific activity, at a specific place, at a specific time. Enter a location and pick an activity (football, jogging, farming, picnic, travelling, or an outdoor event), and the app fetches a live weather forecast, scores the risk hour by hour, asks Gemini to explain that risk in plain language, and hands you a recommended time, a packing checklist, and safety advice — all in one screen.

Built as a Python Advanced project, covering OOP, file handling, exception handling, and regular expressions on top of two real external APIs.

---

## ✨ Features

- **Live weather forecasting** via the Open-Meteo API (no API key required) — geocodes any place, name, and pulls a 3-day hourly + daily forecast.
- **Deterministic, explainable risk scoring** — every activity has its own weather-sensitivity profile (wind, rain, temperature, thunderstorms), and every risk level can be traced back to the exact numbers that produced it.
- **AI-generated explanations** via the Gemini API — turns the rule-based score into a plain-language, 2–3 sentence explanation of *why* it's safe, manageable, risky, or worth avoiding.
- **Best-time recommendation** — scans the day's daytime hours and finds the lowest-risk window.
- **Weather-aware packing checklist** — combines activity-specific basics with items triggered by the forecast (umbrella, sunscreen, windbreaker, extra water, warm layers).
- **Local persistence** — favourite locations and search history are saved to disk as JSON, and survive between sessions.
- **Never crashes** — every network call, malformed response, and bad input is caught and shown as a clear, friendly message instead of a stack trace.

---

## 🏗️ Architecture

```
weather_planner/
├── exceptions.py            # Custom exception hierarchy
├── config.py                 # Constants, activity risk profiles, WMO weather codes
├── validators.py              # Regex: clean location names, validate dates, extract numbers
├── weather_client.py          # WeatherClient  - talks to Open-Meteo
├── forecast.py                 # Forecast        - parses raw API JSON into a usable object
├── risk_analyzer.py            # ActivityRiskAnalyzer - rule-based scoring + Gemini explanation
├── recommendation_engine.py    # RecommendationEngine  - best time, packing list, safety advice
├── storage.py                  # JSON file handling - favourites & search history
├── app.py                       # Streamlit UI - wires everything together
├── requirements.txt
├── .streamlit/secrets.toml.example
└── data/                         # Created automatically - favourites.json, search_history.json
```

`app.py` is deliberately thin — it collects input and renders output, but contains no weather logic, scoring logic, or AI-prompting logic itself. Every actual decision is made by one of the four core classes.

### The four required classes

| Class | File | Responsibility |
|---|---|---|
| `WeatherClient` | `weather_client.py` | Geocodes a place name, fetches the raw forecast JSON. Talks to the network; nothing else does. |
| `Forecast` | `forecast.py` | Parses raw JSON into clean Python types (real `datetime` objects, not strings) with convenient hour-by-hour and day-by-day accessors. |
| `ActivityRiskAnalyzer` | `risk_analyzer.py` | Scores every hour of a forecast against an activity's weather thresholds, and can ask Gemini to explain the result. |
| `RecommendationEngine` | `recommendation_engine.py` | Turns a risk analysis into a best-time recommendation, a packing checklist, and safety advice. |

### Why the AI doesn't decide the risk level

The risk level (`SAFE` / `MANAGEABLE` / `RISKY` / `AVOID`) is computed entirely by `ActivityRiskAnalyzer`'s deterministic scoring rules — **not** by Gemini. Gemini's only job is to explain a score that's already been calculated. This was a deliberate design choice:

- **Testable without an API key.** The entire risk-assessment core works and is fully unit-testable with zero network access.
- **Auditable.** Every risk level can be traced back to specific numbers in the forecast (`"wind at 45 km/h exceeds the 40 km/h limit"`), not an LLM's unexplained judgement call.
- **Safer division of responsibility.** For anything safety-adjacent, having the AI communicate a computed result is a more defensible design than having it invent the classification from scratch.

If no Gemini API key is configured, or the AI call fails for any reason, the app falls back to a clear message and keeps showing the full rule-based assessment — the AI layer is additive, not load-bearing.

---

## 🧠 How risk scoring works

Each activity in `config.ACTIVITIES` has its own thresholds:

```python
"Football": {
    "max_wind_kmh": 40,
    "max_precip_probability": 60,
    "ideal_temp_c": (15, 30),
    "extreme_temp_c": (5, 38),
    ...
}
```

For every hour, `ActivityRiskAnalyzer.score_hour()` checks the forecast against these thresholds and builds up a numeric score:

| Condition | Points |
|---|---|
| Thunderstorm (WMO code 95/96/99) | +3 |
| Rain probability above the activity's limit | +2 |
| Rain probability above 60% of the limit | +1 |
| Wind speed above the activity's limit | +2 |
| Temperature outside the *extreme* range | +3 |
| Temperature outside the *ideal* (but not extreme) range | +1 |

The score maps to a risk level: **0 → SAFE**, **1–2 → MANAGEABLE**, **3–4 → RISKY**, **5+ → AVOID**.

The app reports the risk level of the **best hour** found in the daytime window (6 AM–8 PM), not an average — the point of the app is to recommend a good time, so "is this activity viable today?" should reflect the best realistic opportunity available, not get dragged down by, say, 3 AM.

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure your Gemini API key (optional but recommended)

Get a free key from [Google AI Studio](https://aistudio.google.com/apikey), then:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Open `.streamlit/secrets.toml` and paste your key in. **The app works without this step** — it just shows the rule-based assessment without an AI explanation until a key is configured.

### 3. Run it

```bash
streamlit run app.py
```

This opens the app in your browser at `http://localhost:8501`. No weather API key is needed — Open-Meteo is free for non-commercial use with no authentication.

---

## 📋 Example

**Football in Lagos, Nigeria — today, with a calm morning and a hot, rainy afternoon:**

```
Risk level: SAFE (score 0)
Best time: Saturday, 06:00 AM — mainly clear, 22°C.

Packing checklist:
  Football boots, Shin guards, Water bottle, Team kit,
  Umbrella or rain jacket, Sunscreen (high UV expected),
  Windbreaker, Extra water / electrolytes (high heat expected)

Safety advice:
  - Try to avoid being out around 02:00 PM - conditions are noticeably worse then.
  - Watch out: 68% chance of rain, above the 60% comfort limit.
  - Watch out: temperature of 33°C is outside the ideal comfort range.
```

Note the packing list pulls in rain and heat gear even though the *best* time is dry and mild — it's built from the day's **worst** hour, on the logic that it's better to have packed for conditions that could show up than to be caught out by them.

---

## 🐍 Python Concepts in Practice

| Concept | Where |
|---|---|
| **File handling** | `storage.py` — favourites and search history persist as JSON, with automatic recovery from a missing or corrupted file. |
| **Exception handling** | A full custom hierarchy (`WeatherAppError` → `LocationNotFoundError`, `WeatherDataError`, `NetworkError`, `APIResponseError`, `AIServiceError`). Every network call, in both `WeatherClient` and `ActivityRiskAnalyzer._call_gemini()`, is wrapped in `try`/`except` and converted into a specific, catchable error type — never a raw `requests` exception or an unhandled `KeyError`. |
| **Regular expressions** | `validators.py` — cleaning free-typed location names, format-checking `YYYY-MM-DD` date input before a full `datetime` parse, extracting numeric figures from the AI's generated text, and pulling a risk keyword out of Gemini's free-form response. |
| **OOP** | Four purpose-built classes (`WeatherClient`, `Forecast`, `ActivityRiskAnalyzer`, `RecommendationEngine`), each owning one responsibility, composed together in `app.py`. |

---

## 🧪 Testing

Since this app depends on two external network APIs, its core logic is tested with mocked responses rather than live calls — this means the whole test suite runs offline and doesn't need a real Gemini key.

`test_weather_client.py` covers `WeatherClient` against every documented failure mode: a missing location, a network timeout, a dropped connection, a non-200 status, malformed JSON, and a response missing expected fields. Run it with:

```bash
python test_weather_client.py
```

The rest of the app (`Forecast` parsing, `ActivityRiskAnalyzer` scoring, `RecommendationEngine` output, `storage.py`'s corrupted-file recovery, and the full Streamlit interaction flow) was verified during development using realistic sample data and Streamlit's own `AppTest` framework, which runs the app's actual script end-to-end without needing a browser.

---

## ⚠️ Known Limitations

- Forecasts are limited to 3 days ahead (Open-Meteo's short-range forecast window as configured here).
- Risk thresholds in `config.ACTIVITIES` are reasonable general-purpose defaults, not official safety standards — worth tuning as a group if you want them to reflect a specific context more precisely.
- The AI explanation is generated fresh on every search; there's no caching, so repeated identical searches will re-call Gemini each time.

---

## 📄 License

**MIT License**

Copyright (c) 2026 GreyVectorr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
