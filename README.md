# Synapse - Sistema de Assistência para Clínicas Psicológicas

## Visão Geral

O Synapse é um sistema acadêmico para gestão de consultas psicológicas, estruturado em camadas (Domain, Repository, Service, API) e focado em POO, boas práticas de software e padrões como Repository e Dependency Injection. Atende pacientes, psicólogos e clínicas em três interfaces.

## Arquitetura do Projeto
- **Camadas:**
  - **business_model:** Entidades de domínio (POO puro, regras de negócio)
  - **repositories:** Abstração e implementação da camada de persistência (arquivos JSON ou listas em memória)
  - **services:** Lógica de negócio, orquestração de agendamentos, notificações e agente IA simulado
  - **controllers:** Recebem requisições, orquestram lógica
  - **api:** Rotas, definição de DTOs e validações (Pydantic)
  - **config/views/tests:** Config, frontend (posterior), testes

- **Padrões:** Repository Pattern, Dependency Injection, Observer (notificações), Factory/Strategy (algoritmos AI simulado)

## Tecnologias
- Python 3.10+
- Flask (API REST)
- Pydantic (validação de dados)
- Dados persistidos via JSON ou listas em memória
- Sem Docker, sem BD relacional real, sem IA real

## Principais Endpoints (exemplo)
- POST /api/appointments - Criar agendamento
- GET /api/appointments/{id} - Consultar agendamento
- PATCH /api/appointments/{id}/cancel - Cancelar
- POST /api/auth/login - Autenticação (seed users)
- [Ver API_DOCS.md para lista completa]

## Fluxos Principais
- Cliente faz requisição → API Route → Controller → Service (lógica/validação) → Repository (dados) → Service → Controller → JSON resposta

## Seed Data
- O sistema é iniciado com usuários, psicólogos, clínicas, pacientes e leads prontos no JSON para acessar todas as rotas sem cadastrar nada manualmente.

## Plano de Implementação
1. Estrutura de pastas e contratos
2. Persistência (repos, seed data)
3. Services (agendamento, notificações, AI fake)
4. API (rotas/controllers)
5. Testes
6. Frontend (HTML/CSS puro, posteriormente)

## Setup Rápido

1. **Instale as dependências:**

```bash
python -m venv venv
source venv/bin/activate # Ou .\venv\Scripts\activate no Windows
pip install flask pydantic bcrypt
```

2. **Execute o backend:**

```bash
python main.py
```

3. **Acesse:** Use os logins já presentes no seed para acessar as funcionalidades (ver seeds em `synapse/seeds/`).

## Documentação
- [ARCHITECTURE.md](./ARCHITECTURE.md): Decisões arquiteturais
- [API_DOCS.md](./API_DOCS.md): Endpoints detalhados

---
Projeto acadêmico - uso universitário e instrução.