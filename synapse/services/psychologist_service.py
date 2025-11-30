from synapse.repositories.implementations.inmemory_psychologist_repository import InMemoryPsychologistRepository

class PsychologistService:
    def __init__(self, psychologist_repository: InMemoryPsychologistRepository):
        self.psychologist_repository = psychologist_repository

    def get_all(self):
        return self.psychologist_repository.all()

    def get_by_id(self, psychologist_id: int):
        return self.psychologist_repository.get(psychologist_id)
