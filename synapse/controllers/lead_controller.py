from flask import Blueprint, jsonify, request
from synapse.services.lead_service import LeadService
from synapse.api.dto import LeadCreateDTO, LeadResponseDTO, LeadConvertDTO

bp = Blueprint('leads', __name__, url_prefix='/api/leads')

def create_lead_routes(lead_service: LeadService):
    @bp.route('/', methods=['GET'])
    def get_all_leads():
        leads = lead_service.get_all()
        return jsonify([l.to_dict() for l in leads])

    @bp.route('/<int:lead_id>', methods=['GET'])
    def get_lead(lead_id):
        lead = lead_service.get_by_id(lead_id)
        if not lead:
            return jsonify({'error': 'Lead não encontrado'}), 404
        return jsonify(lead.to_dict())

    @bp.route('/', methods=['POST'])
    def create_lead():
        data = request.get_json()
        try:
            dto = LeadCreateDTO(**data)
        except Exception:
            return jsonify({'error': 'Dados inválidos'}), 400
        lead = lead_service.create_lead(dto.name, dto.email, dto.phone, dto.source, dto.notes)
        resp = LeadResponseDTO(
            id=lead.id,
            name=lead.name,
            email=lead.email,
            phone=lead.phone,
            source=lead.source,
            status=lead.status,
            notes=lead.notes,
            created_at=lead.created_at.isoformat(),
            converted_at=lead.converted_at.isoformat() if lead.converted_at else None,
            converted_to_patient_id=lead.converted_to_patient_id
        )
        return jsonify(resp.dict()), 201

    @bp.route('/<int:lead_id>/contacted', methods=['PATCH'])
    def contacted_lead(lead_id):
        data = request.get_json() or {}
        notes = data.get("notes")
        try:
            lead = lead_service.mark_contacted(lead_id, notes)
            return jsonify(lead.to_dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @bp.route('/<int:lead_id>/lost', methods=['PATCH'])
    def lost_lead(lead_id):
        data = request.get_json() or {}
        reason = data.get("reason")
        try:
            lead = lead_service.mark_lost(lead_id, reason)
            return jsonify(lead.to_dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @bp.route('/<int:lead_id>/convert', methods=['PATCH'])
    def convert_lead(lead_id):
        data = request.get_json() or {}
        try:
            dto = LeadConvertDTO(**data)
            lead = lead_service.convert_to_patient(lead_id, dto.patient_id)
            return jsonify(lead.to_dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    return bp
