from flask import Flask, render_template, request, jsonify, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "nutrisense-secret-key"

def nutrisense_response(user_message):
    msg = user_message.lower()
    last_topic = session.get("last_topic")
    bmi_step = session.get("bmi_step")

    # -------------------- Greeting by time --------------------
    greetings = ["hi", "hello", "hey"]
    if msg in greetings:
        session["last_topic"] = None
        now = datetime.now()
        hour = now.hour
        if hour < 12:
            greet_msg = "Good Morning! 🌞"
        elif hour < 17:
            greet_msg = "Good Afternoon! 🌤️"
        else:
            greet_msg = "Good Evening! 🌙"

        return (
            f"👋 {greet_msg} Welcome to **NutriSense**!\n\n"
            "I can help you with:\n"
            "• Protein intake\n"
            "• BMI calculation\n"
            "• Diet tips\n"
            "• Booking consultation 📅\n\n"
            "Click a button or type your question 😊"
        )

    # -------------------- BMI flow --------------------
    if "bmi" in msg:
        session["bmi_step"] = "height"
        return "📏 Please enter your **height in centimeters (cm)**."

    if bmi_step == "height":
        try:
            height = float(msg)
            session["height"] = height
            session["bmi_step"] = "weight"
            return "⚖️ Now enter your **weight in kilograms (kg)**."
        except:
            return "❌ Please enter a valid number for height (e.g., 165)."

    if bmi_step == "weight":
        try:
            weight = float(msg)
            height = session.get("height")
            bmi = round(weight / ((height / 100) ** 2), 1)

            if bmi < 18.5:
                status = "Underweight"
            elif bmi < 25:
                status = "Normal weight"
            elif bmi < 30:
                status = "Overweight"
            else:
                status = "Obese"

            session.pop("bmi_step", None)
            session.pop("height", None)
            return f"📊 **Your BMI is {bmi}**\n\n🩺 Category: **{status}**\n\nWould you like **protein advice** or **diet tips**?"
        except:
            return "❌ Please enter a valid number for weight (e.g., 60)."

    # -------------------- Protein --------------------
    if "protein" in msg:
        session["last_topic"] = "protein"
        return (
            "💪 Proteins help build muscles and repair body tissues.\n\n"
            "Would you like to know **how much protein you need**?"
        )

    if "how much" in msg and last_topic == "protein":
        return (
            "📊 Protein needs depend on body weight.\n\n"
            "Most adults need **0.8–1g protein per kg body weight per day**.\n"
            "Example: If you weigh 60kg → 48–60g protein daily."
        )

    # -------------------- Breakfast --------------------
    if "breakfast" in msg:
        return (
            "🍳 A healthy breakfast boosts energy and focus.\n\n"
            "Good options:\n• Eggs\n• Oats\n• Fruits with nuts\n• Milk or curd"
        )

    # -------------------- Water --------------------
    if "water" in msg:
        return "💧 Drinking water supports digestion and overall health. Aim for 2–3 liters per day."

    # -------------------- Myth --------------------
    if "myth" in msg:
        return "❌ Myth: Skipping meals helps weight loss.\n✅ Truth: Balanced meals improve metabolism."

    # -------------------- Diet Tips --------------------
    if "diet" in msg:
        return (
            "🥗 **Healthy Diet Tips**\n\n"
            "• Eat fruits & vegetables\n• Include protein in every meal\n"
            "• Avoid junk food\n• Drink enough water"
        )

    # -------------------- Booking --------------------
    if "booking" in msg:
        return "📅 Please select a **date (YYYY-MM-DD)** and time for your consultation."

    # -------------------- Help --------------------
    if "help" in msg:
        return (
            "🤖 You can ask about:\n\n"
            "• Protein\n• BMI\n• Breakfast\n• Water\n• Nutrition myths\n• Diet Tips\n• Booking"
        )

    # -------------------- Default --------------------
    return "🤔 I didn’t understand that. Click a button or type **help**."

# -------------------- Flask routes --------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    reply = nutrisense_response(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
