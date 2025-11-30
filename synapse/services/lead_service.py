from synapse.repositories.implementations.inmemory_lead_repository import InMemoryLeadRepository
from synapse.business_model.lead import Lead
from datetime import datetime

class LeadService:
    def __init__(self, lead_repository: InMemoryLeadRepository):
        self.lead_repository = lead_repository

    def get_all(self):
        return self.lead_repository.all()

    def get_by_id(self, lead_id: int):
        return self.lead_repository.get(lead_id)

    def create_lead(self, name, email, phone, source, notes=None):
        lead = Lead(name=name, email=email, phone=phone, source=source, notes=notes)
        self.lead_repository.add(lead)
        return lead

    def mark_contacted(self, lead_id, notes=None):
        lead = self.get_by_id(lead_id)
        if not lead:
            raise Exception('Lead não encontrado')
        lead.mark_as_contacted(notes)
        self.lead_repository.update(lead)
        return lead

    def mark_lost(self, lead_id, reason=None):
        lead = self.get_by_id(lead_id)
        if not lead:
            raise Exception('Lead não encontrado')
        lead.mark_as_lost(reason)
        self.lead_repository.update(lead)
        return lead

    def convert_to_patient(self, lead_id, patient_id):
        lead = self.get_by_id(lead_id)
        if not lead:
            raise Exception('Lead não encontrado')
        lead.convert_to_patient(patient_id)
        self.lead_repository.update(lead)
        return lead
