from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import json

app = Flask(__name__)

genai.configure(api_key="AIzaSyDxL8r82Jsx72FlUGyQm3z16t_D0HK0F-g")
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    topic = data.get("topic", "")
    platforms = data.get("platforms", [])
    tone = data.get("tone", "argëtues")
    lang = data.get("lang", "shqip")

    platform_instructions = {
        "Instagram": "2 postime Instagram me emoji dhe hashtags",
        "LinkedIn": "2 postime LinkedIn profesionale me hashtags",
        "TikTok": "2 caption TikTok energjike dhe të shkurtra me hashtags",
        "Facebook": "2 postime Facebook miqësore dhe të gjata me hashtags",
        "Twitter/X": "3 tweet të shkurtra nën 280 karaktere me hashtags",
        "YouTube": "1 title dhe 1 description të plotë për YouTube"
    }

    selected = [platform_instructions[p] for p in platforms if p in platform_instructions]
    instructions = "\n".join([f"- {s}" for s in selected])

    prompt = f"""Gjenero postime social media për: "{topic}"
Toni: {tone}
Gjuha: {lang}

Gjenero këto:
{instructions}

Kthe VETEM JSON, pa asnje tekst tjeter, pa backticks:
{{
  "posts": [
    {{
      "platform": "emri i platformes",
      "content": "teksti i postimit",
      "hashtags": "#tag1 #tag2"
    }}
  ]
}}"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip().replace("```json", "").replace("```", "")
        parsed = json.loads(text)
        return jsonify(parsed)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)