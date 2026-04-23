import os
import google.generativeai as genai


def get_activity_suggestions(city: str, weather_days: list) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"teaser": None, "full": None}

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

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
        teaser = full_text.split(".")[0] + "."

        return {"teaser": teaser, "full": full_text}
    except Exception:
        return {"teaser": None, "full": None}
