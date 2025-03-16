from flask import Flask, request, jsonify
import openai
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("path_to_your_firebase_credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# OpenAI API Key (Replace with your own)
openai.api_key = "your_openai_api_key"

app = Flask(__name__)

# Load doctor details from Firebase
def get_doctors():
    doctors_ref = db.collection("doctors").stream()
    doctors = {}
    for doc in doctors_ref:
        doc_data = doc.to_dict()
        doctors[doc.id] = doc_data
    return doctors

# Load doctor slots from Firebase
def get_available_slots(doctor_id):
    slots_ref = db.collection("doctor_slots").document(doctor_id).get()
    if slots_ref.exists:
        return slots_ref.to_dict().get("slots", [])
    return []

@app.route("/chat", methods=["POST"])
def chatbot():
    data = request.json
    user_input = data.get("message", "").lower()

    # Fetch doctor details
    doctors = get_doctors()
    
    # Simple rule-based chatbot logic
    response = "I'm sorry, I didn't understand that."

    if "doctor" in user_input:
        response = "Here are the available doctors:\n"
        for doc_id, info in doctors.items():
            response += f"- {info['name']} ({info['specialization']})\n"

    elif "slot" in user_input:
        doctor_name = user_input.replace("slot for", "").strip()
        for doc_id, info in doctors.items():
            if doctor_name.lower() in info["name"].lower():
                slots = get_available_slots(doc_id)
                response = f"Available slots for {info['name']}:\n" + "\n".join(slots) if slots else "No slots available."
                break

    else:
        # Generate AI response (Optional)
        ai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        response = ai_response["choices"][0]["message"]["content"]

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
