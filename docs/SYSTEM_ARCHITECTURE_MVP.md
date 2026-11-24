# System Architecture --- ProcureFlow AI MVP

**Document version:** 1.0\
**Architecture style:** Modular web application with AI workflow
orchestration\
**Target:** 10-day MVP

------------------------------------------------------------------------

## 1. Architecture goals

-   Deliver an end-to-end procurement workflow within the MVP timeline.
-   Keep business rules deterministic and testable.
-   Use AI for unstructured information processing, not for unchecked
    financial authority.
-   Keep external providers replaceable.
-   Preserve traceability from recommendations to source documents and
    emails.
-   Make human approval mandatory for consequential procurement actions.

## 2. High-level architecture

``` mermaid
flowchart TB
    U[Requester / Procurement / Approver]
    FE[React + Vite + Tailwind UI]
    API[FastAPI Application API]
    AUTH[Authentication and Authorization]
    SVC[Procurement Domain Services]
    DB[(Supabase PostgreSQL)]
    STORE[(Supabase Storage)]
    WF[LangGraph Workflow Layer]
    LLM[LLM Provider Adapter]
    EMAIL[Email Provider Adapter]
    DISC[Supplier Discovery Adapter]
    DOC[Document Extraction Service]
    AUDIT[Audit Event Service]

    U --> FE
    FE -->|HTTPS REST| API
    API --> AUTH
    AUTH --> SVC
    SVC <--> DB
    SVC <--> STORE
    SVC --> WF
    WF <--> LLM
    SVC <--> EMAIL
    WF --> DOC
    SVC <--> DISC
    SVC --> AUDIT
    AUDIT --> DB
```

### 2.1 Component responsibilities

  -----------------------------------------------------------------------
  Component                           Responsibility
  ----------------------------------- -----------------------------------
  React frontend                      User-facing dashboard, forms,
                                      tables, document upload,
                                      comparisons and approval actions.

  FastAPI API                         Authentication checks, request
                                      validation, orchestration of domain
                                      services and REST responses.

  Procurement domain services         Purchase request, supplier, RFQ,
                                      quotation, evaluation, approval and
                                      PO business logic.

  Supabase PostgreSQL                 Durable relational business records
                                      and workflow state.

  Supabase Storage                    Private storage for quotations,
                                      certificates, datasheets and
                                      generated PO documents.

  LangGraph                           Stateful orchestration of selected
                                      multi-step AI workflows, with
                                      checkpoints and human review pauses
                                      where needed.

  LLM adapter                         Calls the configured language model
                                      for extraction, classification,
                                      summarization and draft generation.

  Email adapter                       Sends outbound RFQs and retrieves
                                      inbound replies through the
                                      configured provider.

  Document extraction                 Parses PDF and spreadsheet files;
                                      OCR can be added for scanned files.

  Supplier discovery adapter          Searches permitted public sources
                                      through configured services such as
                                      Olostep; enrichment may use
                                      Crustdata if available.

  Audit service                       Records important user actions,
                                      workflow transitions, approvals and
                                      outbound communications.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 3. Recommended technology stack

  -----------------------------------------------------------------------
  Layer                               MVP technology
  ----------------------------------- -----------------------------------
  Frontend                            React, Vite, Tailwind CSS

  Frontend HTTP                       Axios or Fetch

  Backend                             Python, FastAPI, Pydantic

  ORM / database access               SQLAlchemy

  Database                            Supabase PostgreSQL

  Object storage                      Supabase Storage

  Workflow orchestration              LangGraph

  LLM                                 Gemini API through backend adapter,
                                      subject to API access and data
                                      terms

  PDF extraction                      PyMuPDF

  Spreadsheet extraction              openpyxl

  Scanned document OCR                Optional OCR component if time
                                      permits

  PO PDF                              ReportLab

  Email send                          SMTP or provider send API

  Email receive                       Gmail API or Microsoft Graph; OAuth
                                      required

  Supplier web discovery              Olostep adapter, subject to credits
                                      and API terms

  Company enrichment                  Crustdata adapter, subject to
                                      credits and API terms

  Tests                               pytest, HTTPX; frontend tests can
                                      be added as time permits
  -----------------------------------------------------------------------

**Integration principle:** A provider's promotional credits do not
guarantee data coverage, API availability or permission to use all data.
Keep each provider behind an adapter and handle provider failure
gracefully.

------------------------------------------------------------------------

## 4. Backend modular structure

Suggested backend structure:

``` text
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── permissions.py
│   ├── api/
│   │   └── v1/
│   │       ├── purchase_requests.py
│   │       ├── suppliers.py
│   │       ├── rfqs.py
│   │       ├── emails.py
│   │       ├── quotations.py
│   │       ├── evaluations.py
│   │       ├── approvals.py
│   │       └── purchase_orders.py
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   │   ├── procurement_service.py
│   │   ├── supplier_service.py
│   │   ├── quotation_service.py
│   │   ├── evaluation_service.py
│   │   ├── approval_service.py
│   │   └── purchase_order_service.py
│   ├── agents/
│   │   ├── graphs/
│   │   ├── nodes/
│   │   ├── prompts/
│   │   └── state.py
│   ├── integrations/
│   │   ├── email/
│   │   ├── llm/
│   │   ├── supplier_discovery/
│   │   └── storage/
│   ├── documents/
│   │   ├── pdf_parser.py
│   │   ├── spreadsheet_parser.py
│   │   └── po_generator.py
│   └── audit/
├── tests/
├── .env.example
└── requirements.txt
```

Keep API route handlers thin. Put validation and procurement rules in
services. Keep external provider code out of route handlers.

------------------------------------------------------------------------

## 5. Core data model

``` mermaid
erDiagram
    ORGANIZATION ||--o{ USER : contains
    ORGANIZATION ||--o{ PURCHASE_REQUEST : owns
    ORGANIZATION ||--o{ SUPPLIER : owns
    PURCHASE_REQUEST ||--o{ RFQ : creates
    RFQ ||--o{ RFQ_RECIPIENT : targets
    SUPPLIER ||--o{ RFQ_RECIPIENT : receives
    SUPPLIER ||--o{ EMAIL_MESSAGE : sends_or_receives
    PURCHASE_REQUEST ||--o{ EMAIL_MESSAGE : relates_to
    PURCHASE_REQUEST ||--o{ QUOTATION : receives
    SUPPLIER ||--o{ QUOTATION : submits
    QUOTATION ||--o{ QUOTATION_LINE_ITEM : contains
    PURCHASE_REQUEST ||--o{ EVALUATION : evaluated_by
    EVALUATION ||--o{ APPROVAL : requires
    APPROVAL ||--o| PURCHASE_ORDER : authorizes
    SUPPLIER ||--o{ PURCHASE_ORDER : awarded
    SUPPLIER ||--o{ SUPPLIER_PERFORMANCE : has
    ORGANIZATION ||--o{ AUDIT_EVENT : records
```

### 5.1 Core entities and important fields

  -----------------------------------------------------------------------
  Entity                              Important fields
  ----------------------------------- -----------------------------------
  Organization                        id, name, settings

  User                                id, organization_id, email, role,
                                      status

  PurchaseRequest                     id, organization_id,
                                      request_number, item,
                                      specifications, quantity, budget,
                                      required_by, status

  Supplier                            id, organization_id, name,
                                      contacts, source,
                                      verification_status

  SupplierEvidence                    id, supplier_id, evidence_type,
                                      file_path, issuer, expiry_date,
                                      verification_state

  RFQ                                 id, purchase_request_id, reference,
                                      content, response_deadline, status

  RFQRecipient                        id, rfq_id, supplier_id,
                                      recipient_email, send_status

  EmailMessage                        id, supplier_id,
                                      purchase_request_id, rfq_id,
                                      direction, provider_message_id,
                                      subject, body, timestamps

  Quotation                           id, purchase_request_id,
                                      supplier_id, document_path,
                                      currency, totals, extracted_data,
                                      review_status

  QuotationLineItem                   id, quotation_id, description,
                                      quantity, unit_price, tax, total

  Evaluation                          id, purchase_request_id, criteria,
                                      mandatory_checks, score, findings,
                                      evidence_refs

  Approval                            id, evaluation_id, approver_id,
                                      decision, comments, timestamp

  PurchaseOrder                       id, purchase_request_id,
                                      supplier_id, quotation_id,
                                      po_number, total, status

  SupplierPerformance                 id, supplier_id, purchase_order_id,
                                      delivery_result, inspection_result,
                                      defects

  AuditEvent                          id, organization_id, actor_id,
                                      action, entity_type, entity_id,
                                      timestamp, metadata
  -----------------------------------------------------------------------

The five initial tables created during setup are a starting subset. Add
the remaining entities as their features are implemented. For
multi-company production use, every business record must be
organization-scoped and protected by backend authorization and database
policies.

------------------------------------------------------------------------

## 6. End-to-end workflow and data flow

``` mermaid
flowchart TD
    A[Requester creates purchase request]
    B[Validate mandatory fields]
    C{Information complete?}
    D[Ask requester for clarification]
    E[Procurement reviews request]
    F[Select existing and discovered suppliers]
    G[Generate RFQ draft]
    H[Human reviews and confirms send]
    I[Send RFQ email]
    J[Receive supplier replies and attachments]
    K[Upload or ingest quotation]
    L[Extract quotation fields]
    M[Human corrects uncertain fields]
    N[Run mandatory checks and comparison]
    O[Show evidence, risks and recommendation]
    P{Approver decision}
    Q[Request more information / reject]
    R[Create PO draft]
    S[Authorized user confirms PO send]
    T[Record delivery and inspection outcome]

    A --> B --> C
    C -->|No| D --> B
    C -->|Yes| E --> F --> G --> H --> I --> J --> K --> L --> M --> N --> O --> P
    P -->|More information or reject| Q
    P -->|Approve| R --> S --> T
```

### 6.1 Purchase request

The requester submits structured requirements. AI may help interpret
free text and identify missing information, but the requester must
confirm the final specification.

### 6.2 Supplier selection

The procurement officer can select existing suppliers and add candidates
from permitted discovery sources. New supplier data is labelled with
source and verification status. Discovery results are candidates, not
automatically approved suppliers.

### 6.3 RFQ sending

The RFQ service renders a template using the approved request data. The
UI displays recipient addresses and message content. The user confirms
the send action. The email provider response and message identifier are
stored.

### 6.4 Inbound email and quotation intake

The email adapter synchronizes messages from the connected mailbox.
Matching uses RFQ reference, sender, thread/message identifiers and
other metadata. Low-confidence matches are queued for manual
association. Attachments are validated and stored privately.

### 6.5 Quotation extraction

The document service extracts text and tables. The LLM may map
unstructured content into a validated schema. Each field should retain
provenance such as page, table, source text or extraction method where
practical. Uncertain fields are marked for review.

### 6.6 Evaluation

The evaluation service: 1. Normalizes currencies, units and totals where
reliable conversion data is available. 2. Checks mandatory
specifications and compliance conditions. 3. Flags missing, expired or
unverified evidence. 4. Calculates weighted criteria for eligible
suppliers. 5. Shows the evidence and rationale behind the comparison.

Mandatory criteria cannot be compensated for by a lower price. Physical
quality must be established through inspection, samples or recorded test
results, not inferred from a quotation alone.

### 6.7 Approval and purchase order

An authorized human reviews the recommendation and makes the decision. A
PO draft is generated only after approval. Sending the PO is a separate,
explicitly authorized action.

### 6.8 Supplier performance

After delivery, users record actual delivery and inspection results.
Future supplier evaluations can use these records while distinguishing
verified outcomes from claims.

------------------------------------------------------------------------

## 7. LangGraph workflow design

Use LangGraph only for workflows that benefit from state, branching,
retries or human review. Do not turn every CRUD endpoint into an agent.

Suggested initial graphs:

### Graph A --- Requirement Assistant

``` mermaid
flowchart TD
    A[Receive purchase request text]
    B[Extract item and specifications]
    C[Validate required fields]
    D{Missing or ambiguous?}
    E[Ask clarifying question]
    F[Requester confirms]
    G[Save structured request]
    A --> B --> C --> D
    D -->|Yes| E --> F --> B
    D -->|No| G
```

### Graph B --- Quotation Intelligence

``` mermaid
flowchart TD
    A[Receive uploaded document]
    B[Validate file]
    C[Extract PDF or spreadsheet content]
    D[LLM maps content to schema]
    E[Validate schema and calculations]
    F[Mark uncertain fields]
    G[Human reviews extracted data]
    H[Save approved quotation data]
    A --> B --> C --> D --> E --> F --> G --> H
```

### Graph C --- Supplier Evaluation

``` mermaid
flowchart TD
    A[Load request, suppliers and quotations]
    B[Run deterministic mandatory checks]
    C{Mandatory requirements passed?}
    D[Mark supplier ineligible or needs review]
    E[Calculate configurable weighted criteria]
    F[Prepare evidence-linked explanation]
    G[Present comparison to approver]
    A --> B --> C
    C -->|No| D --> G
    C -->|Yes| E --> F --> G
```

### Agent safety boundaries

-   Email bodies, PDFs, spreadsheets and scraped web pages are untrusted
    input.
-   Extracted content must never override system instructions or
    authorization policy.
-   Agents may draft messages and recommendations but may not bypass
    approval.
-   Tool permissions should be narrow and action-specific.
-   Validate every structured model output with Pydantic.
-   Use deterministic code for money, totals, dates, thresholds,
    eligibility and approval.
-   Keep a record of model/provider, prompt version, output and source
    references where appropriate.

------------------------------------------------------------------------

## 8. API surface for MVP

Suggested REST endpoints:

  -------------------------------------------------------------------------------------------
  Method                  Endpoint                                    Purpose
  ----------------------- ------------------------------------------- -----------------------
  POST                    `/api/v1/purchase-requests`                 Create a request

  GET                     `/api/v1/purchase-requests`                 List requests

  GET                     `/api/v1/purchase-requests/{id}`            Get request details

  PATCH                   `/api/v1/purchase-requests/{id}`            Update permitted fields

  POST                    `/api/v1/suppliers`                         Create supplier

  GET                     `/api/v1/suppliers`                         List/search suppliers

  PATCH                   `/api/v1/suppliers/{id}`                    Update supplier

  POST                    `/api/v1/purchase-requests/{id}/rfqs`       Create RFQ draft

  POST                    `/api/v1/rfqs/{id}/send`                    Send after
                                                                      authorization

  GET                     `/api/v1/purchase-requests/{id}/emails`     List related messages

  POST                    `/api/v1/quotations/upload`                 Upload quotation

  POST                    `/api/v1/quotations/{id}/extract`           Start extraction

  PATCH                   `/api/v1/quotations/{id}`                   Correct extracted
                                                                      values

  POST                    `/api/v1/purchase-requests/{id}/evaluate`   Run evaluation

  POST                    `/api/v1/evaluations/{id}/decision`         Record
                                                                      approval/rejection

  POST                    `/api/v1/purchase-orders`                   Create approved PO
                                                                      draft

  POST                    `/api/v1/purchase-orders/{id}/send`         Send after
                                                                      authorization
  -------------------------------------------------------------------------------------------

All endpoints must authenticate the caller, authorize the requested
action, validate input and scope records to the correct organization.

------------------------------------------------------------------------

## 9. Email integration architecture

``` mermaid
flowchart LR
    API[FastAPI Email Service]
    OUT[Outbound Provider Adapter]
    IN[Inbound Mailbox Sync]
    DB[(EmailMessage records)]
    FILES[(Private attachment storage)]
    WF[Email Classification Workflow]
    API --> OUT
    OUT --> DB
    IN --> DB
    IN --> FILES
    DB --> WF
    FILES --> WF
```

-   Outbound sending can use SMTP or a provider send API.
-   Inbound monitoring requires Gmail API, Microsoft Graph, IMAP or
    another supported mechanism.
-   Gmail API and Microsoft Graph typically require OAuth consent and
    configured permissions.
-   Include the RFQ reference in subject and body to improve matching.
-   Store provider message/thread IDs where available.
-   Prevent duplicate processing using provider message IDs and
    idempotency keys.
-   Keep attachment storage private and validate files before
    processing.
-   If mailbox integration is unavailable, allow manual quotation upload
    and clearly identify the email feature as not connected.

------------------------------------------------------------------------

## 10. Security and trust boundaries

1.  Browser to FastAPI: HTTPS, authenticated session/token and input
    validation.
2.  FastAPI to Supabase: server-side credentials, least privilege and
    organization-scoped access.
3.  FastAPI to LLM: server-side API key, minimal necessary data and
    provider data-term review.
4.  FastAPI to mailbox: OAuth tokens stored securely with
    least-privilege scopes.
5.  Document storage: private buckets, access checks and signed URLs
    with short expiry.
6.  Agent tools: allowlisted functions with explicit permissions and
    human approval for consequential actions.

Do not place Supabase service-role keys, database passwords, Gemini keys
or mailbox refresh tokens in the React environment or source repository.

------------------------------------------------------------------------

## 11. Deployment view

### Hackathon deployment

-   Frontend: Vercel or another static frontend host.
-   Backend: a Python-compatible application host.
-   Database and file storage: Supabase.
-   LLM and mailbox integrations: accessed only from backend.
-   Secrets: host environment variables or secret manager.
-   Logs: structured application logs with sensitive values redacted.

Local development: - React: `http://localhost:5173` - FastAPI:
`http://localhost:8000` - Supabase: hosted project

CORS should allow only the intended frontend origin(s). Production
deployments must use HTTPS and production-specific environment
variables.

------------------------------------------------------------------------

## 12. Reliability and observability

-   Add request IDs and structured logs.
-   Record external provider status and latency without logging secrets
    or full sensitive documents.
-   Apply request timeouts and bounded retries to external calls.
-   Use idempotency for email sends, inbound message processing and PO
    actions.
-   Store long-running extraction/evaluation task status in the
    database.
-   Show pending, processing, completed and failed states in the UI.
-   Provide a safe retry path that does not duplicate consequential
    actions.

------------------------------------------------------------------------

## 13. 10-day implementation sequence

  -----------------------------------------------------------------------
  Day                                 Deliverable
  ----------------------------------- -----------------------------------
  1                                   Repository, environment, Supabase
                                      schema, FastAPI connection and
                                      health endpoint

  2                                   Purchase request and supplier CRUD,
                                      frontend navigation and forms

  3                                   RFQ creation, templates and
                                      supplier selection

  4                                   Outbound email integration and
                                      communication history

  5                                   Quotation upload, private storage
                                      and PDF/XLSX parsing

  6                                   Structured AI extraction and human
                                      correction UI

  7                                   Mandatory checks, supplier
                                      comparison and evidence/risk
                                      display

  8                                   Approval workflow and PO PDF draft

  9                                   Inbound email integration if
                                      provider access is ready;
                                      performance records and integration
                                      tests

  10                                  End-to-end testing, deployment,
                                      demo data, documentation and demo
                                      rehearsal
  -----------------------------------------------------------------------

If email OAuth or external provider access is delayed, prioritize manual
quotation upload and the end-to-end approval/PO workflow. Do not fake a
successful live integration.

------------------------------------------------------------------------

## 14. MVP architecture decisions

  -----------------------------------------------------------------------
  Decision                            Rationale
  ----------------------------------- -----------------------------------
  FastAPI as the main backend         One controlled place for business
                                      rules, permissions and
                                      integrations.

  Supabase PostgreSQL                 Relational data fits purchase
                                      requests, suppliers, quotations,
                                      approvals and POs.

  LangGraph for selected workflows    Supports stateful orchestration and
                                      human review without making every
                                      action autonomous.

  Provider adapters                   Allows email, LLM and supplier
                                      discovery vendors to be replaced.

  Human approval                      Prevents AI from making
                                      unauthorized purchasing
                                      commitments.

  Deterministic evaluation rules      Ensures money, mandatory
                                      requirements and approval policy
                                      are auditable.

  Private object storage              Keeps quotation and supplier
                                      documents out of public URLs.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 15. Known MVP limitations

-   Supplier discovery cannot guarantee completeness or supplier
    legitimacy.
-   Business-data enrichment is not a substitute for supplier due
    diligence.
-   Document extraction may fail on scans, poor layouts or ambiguous
    units.
-   Email threading and reply matching may require human correction.
-   Physical quality cannot be confirmed from documents alone.
-   A hackathon deployment is not automatically production-ready for
    confidential procurement data or multiple customer organizations.
