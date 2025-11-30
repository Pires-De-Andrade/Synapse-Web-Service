# Documentação de Endpoints - Synapse API

## Auth
### POST /api/auth/login
- **Request Body:**
```json
{
  "email": "dra.ana@clinica.com",
  "password": "senha123"
}
```
- **Response:**
```json
{
  "token": "abc.def.ghi",
  "user": {
    "id": 1,
    "name": "Dra. Ana Silva",
    "user_type": "psychologist"
  }
}
```
- **Erros:**
  - 401: Credenciais inválidas

## Patients
### POST /api/patients
- **Request Body:**
```json
{
  "name": "João Pedro Santos",
  "email": "joao@email.com",
  "phone": "(11) 98765-4321",
  "cpf": "123.456.789-00"
}
```
- **Response:**
```json
{
  "id": 1,
  "name": "João Pedro Santos",
  "email": "joao@email.com",
  "phone": "(11) 98765-4321",
  "cpf": "123.456.789-00"
}
```
- **Erros:**
  - 400: Dados inválidos/email duplicado

### GET /api/patients/{id}
- **Response:**
```json
{
  "id": 1,
  "name": "João Pedro Santos",
  "email": "joao@email.com",
  "phone": "(11) 98765-4321",
  "cpf": "123.456.789-00"
}
```
- **Erros:**
  - 404: Paciente não encontrado

## Psychologists
### POST /api/psychologists
- **Request Body:**
```json
{
  "user_id": 1,
  "name": "Dra. Ana Silva",
  "crp": "06/12345",
  "specialty": "TCC",
  "themes": ["Ansiedade", "Depressão"],
  "hourly_rate": 150.0
}
```
- **Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Dra. Ana Silva",
  "crp": "06/12345",
  "specialty": "TCC",
  "themes": ["Ansiedade", "Depressão"],
  "hourly_rate": 150.0,
  "is_active": true
}
```
- **Erros:**
  - 400: Dados inválidos/CRP duplicado

## Appointments
### POST /api/appointments
- **Request Body:**
```json
{
  "patient_id": 1,
  "psychologist_id": 1,
  "date": "2025-12-08",
  "time": "14:00",
  "duration": 60,
  "notes": "Primeira consulta"
}
```
- **Response:**
```json
{
  "id": 1,
  "patient_id": 1,
  "psychologist_id": 1,
  "date": "2025-12-08",
  "time": "14:00",
  "duration": 60,
  "status": "scheduled",
  "notes": "Primeira consulta"
}
```
- **Erros:**
  - 400: Dados inválidos
  - 409: Conflito de horário

## Availabilities
- **POST /api/availabilities**: Cadastrar disponibilidade
- **GET /api/availabilities/{id}**: Consultar
- **GET /api/psychologists/{id}/availabilities**: Listar do profissional
- **PATCH /api/availabilities/{id}/activate/deactivate**

## Leads
- **POST /api/leads**: Gerar lead
- **GET /api/leads/{id}**: Consultar
- **GET /api/leads**: Listar todos
- **PATCH /api/leads/{id}/contacted**: Contatado
- **PATCH /api/leads/{id}/convert**: Converter para paciente
- **PATCH /api/leads/{id}/lost**: Perdeu

## Métricas e Utilidades
- **GET /api/metrics**: Dashboard da clínica. Retorna dados genéricos: nº de leads, consultas do dia, psicólogos ativos, taxa de conversão, etc.

## Observações
- Todas as respostas em JSON puro.
- Para detalhes de body/response/exemplo: veja /api/docs ou exemplos embutidos no código.
- A autenticação estará seedada (usuários prontos) para acesso imediato.
- Códigos de erro padrão: 200, 201, 400, 401, 404, 409, 500.
