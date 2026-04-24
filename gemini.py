import os
import google.generativeai as genai

_model = None


def _get_model():
    global _model
    if _model is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return None
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel("gemini-2.5-flash")
    return _model


def get_activity_suggestions(city: str, weather_days: list) -> dict:
    model = _get_model()
    if model is None:
        return {"teaser": None, "full": None}

    try:
        weather_summary = "\n".join([
            f"- {day['date']}: {day['sky']}, {day['temp']}°C"
            for day in weather_days
        ])

        prompt = f"""Du er en reiseekspert. Basert på værmeldingen nedenfor for {city}, gi 3-5 konkrete aktivitetsforslag på norsk.

Vær:
{weather_summary}

Start svaret med én kort setning som oppsummerer hva slags opplevelser reisende kan forvente (dette brukes som forhåndsvisning). Deretter gi de utfyllende forslagene som en numrert liste. Ikke bruk overskrifter. Svar kun på norsk."""

        response = model.generate_content(prompt)
        full_text = response.text.strip()
        teaser = full_text.split(".\n")[0] + "." if ".\n" in full_text else full_text.split(".")[0] + "."

        return {"teaser": teaser, "full": full_text}
    except Exception as e:
        print(f"[gemini] get_activity_suggestions failed: {e}")
        return {"teaser": None, "full": None}
