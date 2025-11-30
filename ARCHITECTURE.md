# Arquitetura do Synapse

## 1. Visão Geral
O Synapse utiliza arquitetura em camadas alinhada a POO e padrões de engenharia de software. Cada camada possui uma única responsabilidade (SRP) e depende de abstrações (Dependency Inversion Principle).

## 2. Estrutura de Pastas
- synapse/
  - **business_model/**  
    Modelos do domínio: Patient, Psychologist, Clinic, User, Appointment, Availability, Lead, etc.
  - **repositories/**  
    |-- interfaces/ (AbstractRepository, etc.)
    |-- implementations/ (InMemoryPatientRepository, ...)
  - **services/**  
    Orquestradores da lógica de negócio. Ex: AppointmentService, NotificationService, AIAgentService
  - **controllers/**
    Recebem e tratam requisições HTTP, coordenam services e resposta à API
  - **api/**
    Rotas, DTOs (Pydantic), middlewares
  - **config/**
    Configurações globais (settings.py)
  - **views/**
    Temas e componentes HTML/CSS (pós-backend)
  - **tests/**
    Testes unitários/integrados
  - main.py  
    Ponto de entrada da aplicação

## 3. Padrões de Projeto Aplicados
- **Repository Pattern** (repositories/): abstração e troca de estratégias de persistência
- **Dependency Injection** (services/): menor acoplamento
- **Factory Pattern** (from_dict, seed loader): instância de entidades a partir de dados externos
- **Observer Pattern** (services/notification_service.py): notificações/log simulados
- **Strategy Pattern** (services/ai_agent_service.py): heurísticas flexíveis para slotting de agendas

## 4. Justificativas Técnicas
- Modularidade e isolamento: erro em uma camada não compromete outra
- Testabilidade: fácil aplicar mocks e injetar dependências
- POO explícita: classes, composição sobre herança
- Fácil troca do backend de dados (in-memory, JSON)

## 5. Fluxo Macro
Client → Flask Route → Controller → Service (lógica/validação) → Repository (persistência memória/JSON) → Service → Controller → JSON

## 6. Seed Data
Registros prontos para acessar e testar todas as funcionalidades desde a inicialização do sistema. Ex: usuários/senhas, pacientes, agendas, leads, etc.

## 7. Sem dependência de docker/BD real
Projeto todo executável localmente via Python.

## 4.1 Exemplo de Fluxo Completo (Agendamento de Consulta)

1. Usuário paciente escolhe psicólogo e data via frontend.
2. Requisição enviada para POST /api/appointments.
3. Controller recebe, valida entrada via DTO Pydantic.
4. Service de agendamento verifica:
   - Paciente e psicólogo existem
   - Disponibilidade existe (usando Availability)
   - Não há conflitos (consultando AppointmentRepository)
5. Service consulta AIAgentService para sugerir/encontrar horário ideal, aplicando heurísticas específicas via Strategy Pattern:
   - Ex: prioriza manhãs se houver; evita horários consecutivos ou finais de semana.
6. Se disponível, cria e salva Appointment.
7. Notificação ao psicólogo (simulada via NotificationService)
8. Service retorna resposta à controller, que devolve JSON para frontend.

## 4.2 Agente IA Simulado
O AIAgentService aplica regras determinísticas (não IA real) para sugerir horários:

Exemplo de implementação:
```python
class AIAgentService:
    def suggest_appointment_time(self, psychologist_id, preferences=None):
        slots = self.repository.get_available_slots(psychologist_id)
        best_slot = self._apply_strategy(slots, preferences)
        return best_slot
    def _apply_strategy(self, slots, preferences):
        # Example: Prefer mornings, avoid adjacent slots
        for slot in slots:
            if preferences and preferences.get("prefer_morning") and slot.hour < 12:
                return slot
        return slots[0] if slots else None
```
- AppointmentService pode receber diferentes "strategies" para escolha dos horários, personalizando o comportamento do agente fake/conselheiro.
- Essa abordagem demonstra o uso do Strategy Pattern, permitindo trocar regras sem mexer no serviço principal.
