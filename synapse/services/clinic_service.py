from synapse.repositories.implementations.inmemory_clinic_repository import InMemoryClinicRepository

class ClinicService:
    def __init__(self, clinic_repository: InMemoryClinicRepository):
        self.clinic_repository = clinic_repository

    def get_all(self):
        return self.clinic_repository.all()

    def get_by_id(self, clinic_id: int):
        return self.clinic_repository.get(clinic_id)
