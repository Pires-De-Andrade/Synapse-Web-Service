from flask import Blueprint, jsonify
from synapse.services.clinic_service import ClinicService

bp = Blueprint('clinics', __name__, url_prefix='/api/clinics')

def create_clinic_routes(clinic_service: ClinicService):
    @bp.route('/', methods=['GET'])
    def get_all_clinics():
        clinics = clinic_service.get_all()
        return jsonify([c.to_dict() for c in clinics])

    @bp.route('/<int:clinic_id>', methods=['GET'])
    def get_clinic(clinic_id):
        clinic = clinic_service.get_by_id(clinic_id)
        if not clinic:
            return jsonify({'error': 'Clínica não encontrada'}), 404
        return jsonify(clinic.to_dict())
    return bp
