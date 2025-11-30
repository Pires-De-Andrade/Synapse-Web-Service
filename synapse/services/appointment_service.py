from synapse.repositories.implementations.inmemory_appointment_repository import InMemoryAppointmentRepository
from synapse.repositories.implementations.inmemory_patient_repository import InMemoryPatientRepository
from synapse.repositories.implementations.inmemory_psychologist_repository import InMemoryPsychologistRepository
from synapse.repositories.implementations.inmemory_availability_repository import InMemoryAvailabilityRepository
from synapse.business_model.appointment import Appointment
from datetime import datetime, date, time as dtime, timedelta

class AppointmentService:
    def __init__(self, appointment_repository: InMemoryAppointmentRepository,
                 patient_repository: InMemoryPatientRepository,
                 psychologist_repository: InMemoryPsychologistRepository,
                 availability_repository: InMemoryAvailabilityRepository):
        self.appointment_repository = appointment_repository
        self.patient_repository = patient_repository
        self.psychologist_repository = psychologist_repository
        self.availability_repository = availability_repository

    def get_all(self):
        return self.appointment_repository.all()

    def get_by_id(self, appointment_id: int):
        return self.appointment_repository.get(appointment_id)

    def get_available_slots(self, psychologist_id: int, date_str: str, duration: int = 60):
        """Retorna lista de horários disponíveis para um psicólogo em uma data específica"""
        try:
            appt_date = date.fromisoformat(date_str)
        except:
            return []
        
        # Buscar disponibilidades do psicólogo para o dia da semana
        day_of_week = appt_date.weekday()
        availabilities = self.availability_repository.by_psychologist(psychologist_id)
        day_availabilities = [a for a in availabilities if a.day_of_week == day_of_week and a.is_active]
        
        if not day_availabilities:
            return []
        
        # Buscar appointments já agendados para essa data
        existing_appointments = self.appointment_repository.all()
        booked_times = set()
        for ap in existing_appointments:
            if (ap.psychologist_id == psychologist_id 
                and ap.date == appt_date 
                and ap.status != 'cancelled'):
                # Normalizar o horário para comparação
                if isinstance(ap.time, str):
                    booked_time = dtime.fromisoformat(ap.time)
                else:
                    booked_time = ap.time
                booked_times.add(booked_time.strftime('%H:%M'))
        
        # Gerar slots disponíveis
        available_slots = []
        for ava in day_availabilities:
            current_time = ava.start_time
            while current_time < ava.end_time:
                # Calcular fim do slot
                slot_end = (datetime.combine(date.today(), current_time) + timedelta(minutes=duration)).time()
                current_time_str = current_time.strftime('%H:%M')
                
                # Verificar se o slot cabe na janela e não está ocupado
                if slot_end <= ava.end_time and current_time_str not in booked_times:
                    available_slots.append(current_time_str)
                
                # Próximo slot (incrementa de 15 em 15 minutos)
                current_time = (datetime.combine(date.today(), current_time) + timedelta(minutes=15)).time()
        
        return sorted(available_slots)

    def schedule_appointment(self, patient_id, psychologist_id, date_str, time_str, duration=60, notes=None):
        # 1. Validar existência
        patient = self.patient_repository.get(patient_id)
        psy = self.psychologist_repository.get(psychologist_id)
        if not patient:
            raise Exception('Paciente não encontrado')
        if not psy or not psy.is_active:
            raise Exception('Psicólogo inativo ou não encontrado')
        # 2. Converter datas
        try:
            appt_date = date.fromisoformat(date_str)
            appt_time = dtime.fromisoformat(time_str)
        except Exception:
            raise Exception('Data ou hora em formato inválido')
        # 3. Checar disponibilidade (existem slots?)
        avas = self.availability_repository.by_psychologist(psychologist_id)
        ava_day = [a for a in avas if a.day_of_week == appt_date.weekday() and a.is_active]
        if not ava_day:
            raise Exception('Psicólogo não possui disponibilidade neste dia')
        slot_ok = any(a.start_time <= appt_time < a.end_time for a in ava_day)
        if not slot_ok:
            raise Exception('Horário fora da faixa de disponibilidade')
        # 4. Checar conflitos
        existing = self.appointment_repository.all()
        for ap in existing:
            if (ap.psychologist_id == psychologist_id and ap.date == appt_date and ap.time == appt_time and ap.status != 'cancelled'):
                raise Exception('Conflito: já existe consulta nesse horário')
        # 5. Criar e salvar
        appt = Appointment(patient_id, psychologist_id, appt_date, appt_time, duration, notes)
        self.appointment_repository.add(appt)
        return appt

    def cancel_appointment(self, appointment_id:int, reason: str = None):
        appt = self.get_by_id(appointment_id)
        if not appt:
            raise Exception('Consulta não encontrada')
        if appt.status in ['cancelled', 'completed']:
            raise Exception('Consulta não pode ser cancelada')
        appt.cancel(reason)
        self.appointment_repository.update(appt)
        return appt

    def complete_appointment(self, appointment_id:int):
        appt = self.get_by_id(appointment_id)
        if not appt:
            raise Exception('Consulta não encontrada')
        if appt.status not in ['scheduled', 'confirmed']:
            raise Exception('Consulta não pode ser concluída nesse status')
        appt.complete()
        self.appointment_repository.update(appt)
        return appt
