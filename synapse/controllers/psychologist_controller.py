from flask import Blueprint, jsonify
from synapse.services.psychologist_service import PsychologistService

bp = Blueprint('psychologists', __name__, url_prefix='/api/psychologists')

def create_psychologist_routes(psychologist_service: PsychologistService):
    @bp.route('/', methods=['GET'])
    def get_all_psychologists():
        psys = psychologist_service.get_all()
        return jsonify([p.to_dict() for p in psys])

    @bp.route('/<int:psychologist_id>', methods=['GET'])
    def get_psychologist(psychologist_id):
        psy = psychologist_service.get_by_id(psychologist_id)
        if not psy:
            return jsonify({'error': 'Psicólogo não encontrado'}), 404
        return jsonify(psy.to_dict())
    return bp
