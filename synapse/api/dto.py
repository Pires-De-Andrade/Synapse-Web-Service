from pydantic import BaseModel, EmailStr
from typing import Optional

class AuthLoginDTO(BaseModel):
    email: EmailStr
    password: str

class AuthResponseDTO(BaseModel):
    token: str
    user_id: int
    name: str
    user_type: str

class AppointmentCreateDTO(BaseModel):
    patient_id: int
    psychologist_id: int
    date: str   # yyyy-mm-dd
    time: str   # HH:MM
    duration: int = 60
    notes: Optional[str] = None

class AppointmentResponseDTO(BaseModel):
    id: int
    patient_id: int
    psychologist_id: int
    date: str
    time: str
    duration: int
    status: str
    notes: Optional[str] = None

class AppointmentCancelDTO(BaseModel):
    cancellation_reason: Optional[str] = None

class LeadCreateDTO(BaseModel):
    name: str
    email: EmailStr
    phone: str
    source: str
    notes: Optional[str] = None

class LeadResponseDTO(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    source: str
    status: str
    notes: Optional[str] = None
    created_at: str
    converted_at: Optional[str] = None
    converted_to_patient_id: Optional[int] = None

class LeadConvertDTO(BaseModel):
    patient_id: int
