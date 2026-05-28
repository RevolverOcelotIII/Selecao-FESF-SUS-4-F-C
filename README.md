# MedManager ERP - Plataforma de Operações Hospitalares

**MedManager** é um protótipo e Proof of Concept (PoC) de um ERP hospitalar de alta performance e customizável. O projeto demonstra uma abordagem robusta para otimizar operações hospitalares, fluxos clínicos e gestão de recursos através de uma arquitetura **Model-Driven** totalmente dinâmica.

---

## 📦 Estratégia de Entrega e Repositórios (Barema)

Para atender estritamente aos critérios de nomenclatura e organização do **Edital N.º 01/2026 (Anexo IV - Barema)**, este projeto foi replicado em múltiplos repositórios. 

**Nota Importante:** Todos os repositórios listados abaixo contêm o **exato mesmo código-fonte** da aplicação Full Stack integrada. A única diferença entre eles é o arquivo `README.md`, que foi adaptado individualmente para destacar os requisitos específicos de cada item de avaliação:

1.  **Seleção FESF-SUS – 1 F.C**: Foco na demonstração da **API Python (FastAPI)** **Interface React (Next.js)** com gerenciamento de estados utilizando **Zustand**.
2.  **Seleção FESF-SUS – 2 F.C**: Foco na orquestração **Docker** e implementação de segurança **OAuth2**.
3.  **Seleção FESF-SUS – 3 F.C**: Foco na explicação do uso de **Redis** para caches no projeto.
4.  **Seleção FESF-SUS – 4 F.C**: Foco na suíte de testes automatizados (**Unit & Integration Tests**).
---
### Descrição de requisitos do Seleção FESF-SUS – 4 F.C:

**1. Testes de Backend (Pytest)**

  A suíte de testes do backend foi desenvolvida para garantir a integridade das regras de negócio hospitalares e a segurança dos endpoints.

   * Infraestrutura e Isolamento (`backend/app/tests/conftest.py`):
       * Implementa uma estratégia de Banco de Dados de Teste Dedicado em PostgreSQL, garantindo compatibilidade total com tipos de dados
         complexos (Enums, BigInt).
       * Utiliza fixtures para criar contextos de usuários com diferentes níveis de acesso (`admin_user`, `doctor_user`, `attendant_user`), permitindo
         testar o RBAC de forma integrada.
       * Gerencia a limpeza automática das tabelas entre cada teste para garantir isolamento absoluto.

   * Testes de Serviço (Unitários):
       * Exemplo: `backend/app/tests/services/test_patient_service.py` e `test_employee_service.py`.
       * Validam regras críticas como unicidade de CPF, hashing de senhas e a serialização restrita de campos sensíveis (ex: ocultar salários
         para não-admins).

   * Testes de Controlador (Integração):
       * Exemplo: `backend/app/tests/controllers/test_auth_controller.py` e `test_attendance_controller.py`.
       * Simulam requisições HTTP reais usando o TestClient do FastAPI, validando códigos de status (200, 201, 403), cabeçalhos de autenticação e
         o formato do JSON retornado.

  ---

  2. Testes de Frontend (Jest e React Testing Library)

  No frontend, os testes focam no comportamento do usuário e na integração correta com o estado global da aplicação.

   * Configuração Global (`frontend/jest.setup.ts`):
       * Centraliza os mocks necessários para o ambiente JSDOM (como o roteador do Next.js e o serviço de cookies).
       * Gerencia o estado global do Zustand (`useAuthStore`), garantindo que os testes iniciem em um estado autenticado por padrão.

   * Testes de Componentes e Layout:
       * Exemplo: `frontend/src/spec/components/layout/Grid/Grid.spec.tsx` e `frontend/src/spec/components/layout/Form/SearchInput.spec.tsx`.
       * Validam lógicas complexas como a ordenação automática por `updated_at`, filtragem em tempo real em dropdowns pesquisáveis e renderização
         de badges coloridos.

   * Testes de Fluxo e RBAC:
       * Exemplo: `frontend/src/spec/app/users/UsersPage.spec.tsx`.
       * Comprova que o sistema redireciona usuários sem permissão (ex: Médicos tentando acessar a página de Usuários) e valida o preenchimento e
         submissão de formulários complexos via user-event.

  ---

  3. Execução Funcional

  O desenvolvimento funcional é comprovado pela execução bem-sucedida de 85 testes de backend e 186 testes de frontend dentro dos containers
  Docker, garantindo que qualquer alteração no código seja validada automaticamente contra regressões.

   * Comandos de Verificação:
       * Backend: docker-compose exec api pytest app/tests/
       * Frontend: docker-compose exec frontend npm test


## 🏗 Visão Geral: Lógica Dinâmica e Configuração

Diferente de ERPs rígidos, o MedManager utiliza um motor de **entidades dinâmicas**. O comportamento do fluxo clínico não é definido por código fixo, mas pela parametrização administrativa:

1.  **Dynamic Roles**: O administrador cria cargos (ex: "Cirurgião", "Enfermeiro de Triagem") e os vincula a um dos **5 Níveis de Acesso Base** (Medical, Logistics, Pharmaceutical, Admin ou Logged User).
2.  **Dynamic Procedures**: Cada ação clínica é um item de catálogo onde o administrador define a **Permission Matrix (RBAC)**:
    *   **Dispatch Roles**: Quais cargos podem *solicitar* o procedimento.
    *   **Execute Roles**: Quais cargos podem *executar* e registrar notas clínicas.

---

## 🛠 Tech Stack

### Frontend
- **Framework:** Next.js 15+ (App Router) | TypeScript
- **State Management:** Zustand (Session Global, RBAC e UI State)
- **Internationalization:** i18n-js (Suporte a PT-BR e EN)
- **Testing:** Jest + React Testing Library (Política de **Zero-Mock** para componentes internos)
- **Styling:** Vanilla CSS Variables (Paleta Zinc, cores OKLCH)

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL | SQLAlchemy 2.0 (ORM) | Alembic (Migrations)
- **Cache:** Redis (Camada de cache para performance de queries e catálogos)
- **Architecture:** **Service Layer Pattern** para desacoplamento da lógica de negócio.

---

## 🚀 Passo a Passo do Sistema (Tutorial)

> **Nota**: Para testar o fluxo completo, é necessário criar pelo menos **três usuários** com perfis diferentes (ex: Atendente, Enfermeiro e Médico).

### 1. Parametrização das Regras de Negócio (Admin Setup)
Logue como **Admin** para configurar a infraestrutura lógica:

*   **Criar Roles**: Em **Administration > Roles**, crie os cargos "Recepcionista" (Level: Attendant), "Enfermeiro" (Level: Nurse) e "Médico" (Level: Doctor).
<img width="1912" height="796" alt="Captura de tela 2026-05-27 211017" src="https://github.com/user-attachments/assets/a1a1b7cc-c5d0-4a52-872e-16e6b6584d18" />

*   **Registrar Staff**: Em **Administration > Employees**, cadastre os profissionais.
<img width="1913" height="843" alt="Captura de tela 2026-05-27 211134" src="https://github.com/user-attachments/assets/a7925b92-ab0f-4d22-bc95-ac9d4a2790cb" />

*   **Vincular Contas**: Em **Administration > Users**, crie as credenciais de login para os funcionários.
<img width="1918" height="775" alt="Captura de tela 2026-05-27 211448" src="https://github.com/user-attachments/assets/f6806df2-7c4f-4a7a-9c32-cac1f679c361" />

*   **Configurar Procedimentos**: Em **Administration > Procedures**, defina as regras de Dispatch e Execute para procedimentos como "Triagem" e "Consulta".
<img width="677" height="830" alt="Captura de tela 2026-05-27 211222" src="https://github.com/user-attachments/assets/9431166a-83a6-45f2-a481-1cb998957874" />

### 2. Fluxo de Admissão (Attendant Flow)
Logue como o **Recepcionista**:

*   **Registrar Paciente**: Em **Workspace > Patients**, faça o cadastro inicial.
<img width="1918" height="907" alt="Captura de tela 2026-05-27 211625" src="https://github.com/user-attachments/assets/13f8aa5a-7bee-4ed8-9d25-d2b2e0451ad7" />

*   **Iniciar Attendance**: Crie o atendimento e solicite a "Triagem". O sistema filtrará automaticamente apenas enfermeiros aptos.

### 3. Execução Clínica e Encaminhamento (Nurse Flow)
Logue como o **Enfermeiro**:

*   **Realizar Triagem**: Altere o status para **"In Progress"**, registre os sinais vitais e finalize como **"Done"**.
*   **Workflow em Cadeia**: Antes de fechar, solicite uma **"Consulta"**. Por ser um Enfermeiro, você tem autoridade para encaminhar o paciente ao Médico.
<img width="1918" height="912" alt="Captura de tela 2026-05-27 211654" src="https://github.com/user-attachments/assets/5685b1ad-34f3-43c4-bc9a-e2f81b223f09" />

### 4. Atendimento Especializado (Doctor Flow)
Logue como o **Médico**:

*   **Medical Review**: Revise as notas da triagem e execute a "Consulta", adicionando diagnóstico e tratamento (com busca integrada de **Medicines**).

---

## 🐳 Setup e Instalação (Docker)

### 1. Pré-requisitos
- Docker & Docker Compose.
- Arquivo `.env` na raiz (baseie-se no `.env.example`).

### 2. Subir a Infraestrutura
```bash
# Inicialização de todos os serviços (API, Web, DB, Redis)
docker-compose up --build
```

### 3. Migrações e Dados Iniciais (Seed)
As migrations rodam automaticamente. Para popular o banco com a conta Admin inicial e roles base, execute:

```bash
# Popular o banco (Seed)
docker-compose exec api python -m app.seed
```

**Credenciais Administrativas Iniciais:**
- **Email**: `admin@medmanager.com`
- **Senha**: `admin123`

### 4. Executando Testes
**Backend Tests (Pytest):**
```bash
docker-compose exec api pytest app/tests/
```

**Frontend Tests (Jest):**
```bash
docker-compose exec frontend npm test
```

---

## 🌍 Suporte a Idiomas (i18n)
O sistema é totalmente internacionalizado. Preferências de idioma são persistidas no `localStorage`.
- 🇧🇷 **Português (Padrão)**
- 🇺🇸 **Inglês**

---
*Este projeto foi desenvolvido como demonstração técnica de nível Pleno para o Processo Seletivo FESF-SUS (2026).*
   
