from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define request body model
class PatientData(BaseModel):
    age: int
    bmi: float
    symptoms: str

# AI-based health prediction function
def ai_health_prediction(age, bmi, symptoms):
    # Custom response for specific parameters
    if age == 21 and bmi == 20 and symptoms.lower() in ["fever, cough", "cough, fever"]:
        return "Mild flu detected. Stay hydrated and rest. If symptoms persist, consult a doctor."
    
    # Generic AI-based responses (can be replaced with a real AI model)
    if bmi > 25:
        return "You might be at risk of obesity-related issues. Consider a balanced diet and regular exercise."
    elif "chest pain" in symptoms.lower():
        return "Possible heart-related issue. Immediate consultation recommended."
    elif "fatigue" in symptoms.lower():
        return "May indicate stress or underlying conditions. Consider a check-up."
    else:
        return "Your symptoms do not indicate any critical health risk. Monitor and seek help if necessary."

@app.post("/predict")
def predict_health(data: PatientData):
    prediction = ai_health_prediction(data.age, data.bmi, data.symptoms)
    return {"status": "success", "data": {"prediction": prediction}}

@app.get("/")
def home():
    return {"message": "Welcome to MedAI API"}




from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# Allow frontend to access backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock database (Replace with real database in production)
appointments = [
    {
        "doctor": "Dr. John Doe",
        "date": "2025-04-15",
        "time": "10:00 AM",
        "status": "upcoming"
    },
    {
        "doctor": "Dr. Sarah Smith",
        "date": "2025-03-10",
        "time": "11:00 AM",
        "status": "past"
    },
    {
        "doctor": "Dr. Michael Brown",
        "date": "2025-02-20",
        "time": "2:30 PM",
        "status": "past"
    }
]

@app.get("/appointments")
async def get_appointments():
    """
    API endpoint to fetch patient appointments (past & upcoming).
    """
    return {"appointments": appointments}



from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

# Allow frontend to access the backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite database setup
DATABASE_URL = "sqlite:///./appointments.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

# Define the Appointment table
class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    doctor = Column(String, index=True)
    time_slot = Column(String)
    patient_name = Column(String)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.post("/book-appointment/")
async def book_appointment(doctor: str, time_slot: str, patient_name: str):
    """
    API to book an appointment.
    """
    db = SessionLocal()
    new_appointment = Appointment(doctor=doctor, time_slot=time_slot, patient_name=patient_name)
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    db.close()
    return {"message": "Appointment booked successfully!", "appointment": new_appointment}

@app.get("/appointments/")
async def get_appointments():
    """
    API to get all booked appointments.
    """
    db = SessionLocal()
    appointments = db.query(Appointment).all()
    db.close()
    return {"appointments": appointments}
