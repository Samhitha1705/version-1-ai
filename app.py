from flask import Flask, render_template, request, jsonify, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "nutrisense-secret-key"

# --------------------
# Time-based greeting
# --------------------
def get_time_greeting():
    current_hour = datetime.now().hour

    if current_hour < 12:
        return "🌅 Good Morning"
    elif current_hour < 17:
        return "☀️ Good Afternoon"
    else:
        return "🌙 Good Evening"

# --------------------
# Chatbot response logic
# --------------------
def nutrisense_response(user_message):
    msg = user_message.lower().strip()
    last_topic = session.get("last_topic")
    booking_step = session.get("booking_step")
    bmi_step = session.get("bmi_step")

    # --------------------
    # BOOKING FLOW
    # --------------------
    if booking_step == "date":
        try:
            datetime.strptime(msg, "%Y-%m-%d")
            session["booking_date"] = msg
            session["booking_step"] = "time"
            return "⏰ Enter a **time (HH:MM in IST)** using the picker"
        except ValueError:
            return "❌ Invalid date. Please use the calendar picker."

    if booking_step == "time":
        date = session.get("booking_date")
        session.pop("booking_step", None)
        session.pop("booking_date", None)
        return (
            f"✅ **Appointment Confirmed**\n\n"
            f"📅 Date: {date}\n"
            f"⏰ Time: {msg} IST\n\n"
            "For assistance: support@nutrisense.com"
        )

    if "book" in msg or "consultation" in msg:
        session["booking_step"] = "date"
        return "📅 Please select a **date** using the calendar picker."

    # --------------------
    # BMI FLOW
    # --------------------
    if "bmi" in msg or "body mass index" in msg:
        session["bmi_step"] = "height"
        return "📏 Please enter your **height in centimeters (cm)**."

    if bmi_step == "height":
        try:
            height = float(msg)
            session["height"] = height
            session["bmi_step"] = "weight"
            return "⚖️ Now enter your **weight in kilograms (kg)**."
        except ValueError:
            return "❌ Please enter a valid number for height (e.g., 165)."

    if bmi_step == "weight":
        try:
            weight = float(msg)
            height = session.get("height")
            bmi = weight / ((height / 100) ** 2)
            bmi = round(bmi, 1)

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

            return (
                f"📊 **Your BMI is {bmi}**\n\n"
                f"🩺 Category: **{status}**\n\n"
                "Would you like **protein advice** or **diet tips**?"
            )
        except ValueError:
            return "❌ Please enter a valid number for weight (e.g., 60)."

    # --------------------
    # NORMAL CHAT LOGIC
    # --------------------
    greetings = ["hi", "hello", "hey"]
    if any(greet in msg for greet in greetings):
        session["last_topic"] = None
        greeting = get_time_greeting()

        return (
            f"{greeting}! 👋 Welcome to **NutriSense**!\n\n"
            "I can help you with:\n"
            "• Protein intake\n"
            "• BMI calculation\n"
            "• Diet tips\n"
            "• Booking consultation 📅\n\n"
            "Click a button or type your question 😊"
        )

    if "protein" in msg:
        session["last_topic"] = "protein"
        return (
            "💪 Proteins help build muscles and repair body tissues.\n\n"
            "Would you like to know **how much protein you need**?"
        )

    if ("how much" in msg or "need" in msg) and last_topic == "protein":
        return (
            "📊 Protein needs depend on body weight.\n\n"
            "Most adults need **0.8–1g protein per kg body weight per day**.\n"
            "Example: 60kg → 48–60g protein/day."
        )

    if "breakfast" in msg:
        return (
            "🍳 A healthy breakfast boosts energy and focus.\n\n"
            "Good options:\n• Eggs\n• Oats\n• Fruits with nuts\n• Milk or curd"
        )

    if "water" in msg:
        return "💧 Drinking water supports digestion.\n\nAim for 2–3 liters per day."

    if "diet" in msg:
        return (
            "🥗 **Healthy Diet Tips**\n\n"
            "• Eat fruits & vegetables\n"
            "• Include protein in every meal\n"
            "• Avoid junk food\n"
            "• Drink enough water"
        )

    if "myth" in msg:
        return (
            "❌ Myth: Skipping meals helps weight loss.\n\n"
            "✅ Truth: Balanced meals improve metabolism."
        )

    if "help" in msg:
        return (
            "🤖 You can ask about:\n\n"
            "• Protein\n• BMI\n• Breakfast\n• Water\n• Diet\n• Myth\n• Book consultation"
        )

    return (
        "🤔 I didn’t understand that.\n\n"
        "Try typing **help**.\n\n"
        "For support: support@nutrisense.com"
    )

# --------------------
# ROUTES
# --------------------
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
