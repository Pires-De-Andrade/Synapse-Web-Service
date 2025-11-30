from flask import Blueprint, jsonify, request
from synapse.services.patient_service import PatientService
from synapse.business_model.patient import Patient

bp = Blueprint('patients', __name__, url_prefix='/api/patients')

def create_patient_routes(patient_service: PatientService):
    @bp.route('/', methods=['GET'])
    def get_all_patients():
        patients = patient_service.get_all()
        return jsonify([p.to_dict() for p in patients])

    @bp.route('/', methods=['POST'])
    def create_patient():
        data = request.get_json()
        try:
            patient = Patient(
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone'),
                cpf=data.get('cpf')
            )
            patient_service.patient_repository.add(patient)
            return jsonify(patient.to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @bp.route('/<int:patient_id>', methods=['GET'])
    def get_patient(patient_id):
        patient = patient_service.get_by_id(patient_id)
        if not patient:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        return jsonify(patient.to_dict())
    return bp
