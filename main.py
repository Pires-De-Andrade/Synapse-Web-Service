from flask import Flask, jsonify, render_template
from synapse.services.seed_loader import SeedLoader
from synapse.repositories.implementations.inmemory_patient_repository import InMemoryPatientRepository
from synapse.repositories.implementations.inmemory_psychologist_repository import InMemoryPsychologistRepository
from synapse.repositories.implementations.inmemory_appointment_repository import InMemoryAppointmentRepository
from synapse.repositories.implementations.inmemory_user_repository import InMemoryUserRepository
from synapse.repositories.implementations.inmemory_clinic_repository import InMemoryClinicRepository
from synapse.repositories.implementations.inmemory_lead_repository import InMemoryLeadRepository
from synapse.repositories.implementations.inmemory_availability_repository import InMemoryAvailabilityRepository
from synapse.services.auth_service import AuthService
from synapse.controllers.auth_controller import create_auth_routes
from synapse.services.patient_service import PatientService
from synapse.controllers.patient_controller import create_patient_routes
from synapse.services.psychologist_service import PsychologistService
from synapse.controllers.psychologist_controller import create_psychologist_routes
from synapse.services.appointment_service import AppointmentService
from synapse.controllers.appointment_controller import create_appointment_routes
from synapse.services.clinic_service import ClinicService
from synapse.controllers.clinic_controller import create_clinic_routes
from synapse.services.lead_service import LeadService
from synapse.controllers.lead_controller import create_lead_routes

app = Flask(__name__, 
            template_folder='synapse/views/templates',
            static_folder='synapse/views/static',
            static_url_path='/static')

# Carregar seeds iniciais
data = SeedLoader.load()
patient_repo = InMemoryPatientRepository(data['patients'])
psychologist_repo = InMemoryPsychologistRepository(data['psychologists'])
availability_repo = InMemoryAvailabilityRepository(data['availabilities'])
appointment_repo = InMemoryAppointmentRepository(data['appointments'])
user_repo = InMemoryUserRepository(data['users'])
clinic_repo = InMemoryClinicRepository(data['clinics'])
lead_repo = InMemoryLeadRepository(data['leads'])

# Service de autenticação
auth_service = AuthService(user_repo)
app.register_blueprint(create_auth_routes(auth_service))

# Service e rotas de pacientes
patient_service = PatientService(patient_repo)
app.register_blueprint(create_patient_routes(patient_service))

# Service e rotas de psicólogos
psychologist_service = PsychologistService(psychologist_repo)
app.register_blueprint(create_psychologist_routes(psychologist_service))

# Service e rotas de consultas
appointment_service = AppointmentService(
    appointment_repo, patient_repo, psychologist_repo, availability_repo)
app.register_blueprint(create_appointment_routes(appointment_service))

# Service e rotas de clínicas
clinic_service = ClinicService(clinic_repo)
app.register_blueprint(create_clinic_routes(clinic_service))

# Service e rotas de leads
lead_service = LeadService(lead_repo)
app.register_blueprint(create_lead_routes(lead_service))

# Rotas de Views (Frontend)
@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/patient/booking", methods=["GET"])
def patient_booking():
    return render_template('patient_booking.html')

@app.route("/psychologist/login", methods=["GET"])
def psychologist_login():
    return render_template('psychologist_login.html')

@app.route("/psychologist/dashboard", methods=["GET"])
def psychologist_dashboard():
    return render_template('psychologist_dashboard.html')

@app.route("/clinic/login", methods=["GET"])
def clinic_login():
    return render_template('clinic_login.html')

@app.route("/clinic/dashboard", methods=["GET"])
def clinic_dashboard():
    return render_template('clinic_dashboard.html')

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK", "message": "Synapse backend up"})

if __name__ == "__main__":
    app.run(debug=True)
