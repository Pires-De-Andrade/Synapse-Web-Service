from flask import Blueprint, jsonify, request
from synapse.services.appointment_service import AppointmentService
from synapse.api.dto import AppointmentCreateDTO, AppointmentResponseDTO, AppointmentCancelDTO

bp = Blueprint('appointments', __name__, url_prefix='/api/appointments')

def create_appointment_routes(appointment_service: AppointmentService):
    @bp.route('/', methods=['GET'])
    def get_all_appointments():
        appointments = appointment_service.get_all()
        return jsonify([a.to_dict() for a in appointments])

    @bp.route('/<int:appointment_id>', methods=['GET'])
    def get_appointment(appointment_id):
        a = appointment_service.get_by_id(appointment_id)
        if not a:
            return jsonify({'error': 'Consulta não encontrada'}), 404
        return jsonify(a.to_dict())

    @bp.route('/', methods=['POST'])
    def create_appointment():
        data = request.get_json()
        try:
            dto = AppointmentCreateDTO(**data)
        except Exception:
            return jsonify({'error': 'Dados inválidos'}), 400
        try:
            appt = appointment_service.schedule_appointment(
                dto.patient_id, dto.psychologist_id, dto.date, dto.time, dto.duration, dto.notes)
            resp = AppointmentResponseDTO(
                id=appt.id,
                patient_id=appt.patient_id,
                psychologist_id=appt.psychologist_id,
                date=appt.date.isoformat(),
                time=appt.time.isoformat(),
                duration=appt.duration,
                status=appt.status,
                notes=appt.notes,
            )
            return jsonify(resp.dict()), 201
        except Exception as e:
            if 'Conflito' in str(e):
                return jsonify({'error': str(e)}), 409
            return jsonify({'error': str(e)}), 400

    @bp.route('/<int:appointment_id>/cancel', methods=['PATCH'])
    def cancel_appointment(appointment_id):
        data = request.get_json() or {}
        try:
            dto = AppointmentCancelDTO(**data)
        except Exception:
            return jsonify({'error': 'Dados inválidos'}), 400
        try:
            appt = appointment_service.cancel_appointment(appointment_id, dto.cancellation_reason)
            return jsonify(appt.to_dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @bp.route('/<int:appointment_id>/complete', methods=['PATCH'])
    def complete_appointment(appointment_id):
        try:
            appt = appointment_service.complete_appointment(appointment_id)
            return jsonify(appt.to_dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @bp.route('/available-slots', methods=['POST'])
    def get_available_slots():
        data = request.get_json()
        psychologist_id = data.get('psychologist_id')
        date_str = data.get('date')
        if not psychologist_id or not date_str:
            return jsonify({'error': 'psychologist_id e date são obrigatórios'}), 400
        slots = appointment_service.get_available_slots(psychologist_id, date_str)
        return jsonify({'available_times': slots}), 200
    return bp
