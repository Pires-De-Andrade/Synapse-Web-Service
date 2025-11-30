from synapse.repositories.implementations.inmemory_patient_repository import InMemoryPatientRepository

class PatientService:
    def __init__(self, patient_repository: InMemoryPatientRepository):
        self.patient_repository = patient_repository

    def get_all(self):
        return self.patient_repository.all()

    def get_by_id(self, patient_id: int):
        return self.patient_repository.get(patient_id)
