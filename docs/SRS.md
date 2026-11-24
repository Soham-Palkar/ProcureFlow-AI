# Software Requirements Specification (SRS)

## ProcureFlow AI --- Minimum Viable Product

**Document version:** 1.0\
**Status:** Initial baseline\
**Target:** 10-day hackathon MVP\
**Product type:** AI-assisted procurement workflow platform

------------------------------------------------------------------------

## 1. Introduction

### 1.1 Purpose

This document defines the software requirements for ProcureFlow AI MVP.
It establishes the product's purpose, scope, users, operating
environment, assumptions, constraints and acceptance criteria. It is
intended for the development team, reviewers and stakeholders.

### 1.2 Product vision

ProcureFlow AI acts as an AI-assisted procurement department for small
and medium-sized enterprises (SMEs) and manufacturers. It coordinates
procurement work from an internal purchase request through supplier
outreach, quotation analysis, human approval and purchase-order
preparation.

The platform combines structured business rules with AI-assisted
document and email understanding. It aims to reduce manual coordination,
make supplier comparisons more transparent and preserve an auditable
record of procurement decisions.

### 1.3 Problem statement

Procurement teams often manage requirements, supplier contacts, RFQs,
quotation files, comparisons, approvals and purchase orders across
disconnected spreadsheets, email inboxes and documents. This creates
delays, repeated manual data entry, inconsistent comparisons and limited
visibility into why a supplier was selected.

ProcureFlow AI provides one workflow and record of truth for these
activities.

### 1.4 Intended audience

-   Procurement officers and buyers.
-   Production or department managers who raise purchase requests.
-   Procurement managers and approvers.
-   Administrators responsible for supplier and user records.
-   Developers, testers and hackathon evaluators.

### 1.5 Definitions

  -----------------------------------------------------------------------
  Term                                Definition
  ----------------------------------- -----------------------------------
  PR                                  Purchase Request raised by an
                                      internal department.

  RFQ                                 Request for Quotation sent to
                                      prospective suppliers.

  Quotation                           Supplier's commercial and technical
                                      offer.

  PO                                  Purchase Order prepared after
                                      approval.

  Supplier evidence                   Documents or records supporting
                                      supplier claims, such as
                                      certificates, datasheets and past
                                      performance.

  Human-in-the-loop                   A workflow in which a person
                                      reviews or authorizes consequential
                                      actions.

  Document-based compliance           Assessment of supplied documents
                                      against required specifications or
                                      certificates; it is not proof of
                                      physical product quality.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 2. Overall description

### 2.1 Product perspective

ProcureFlow AI is a web application with: - A React-based user
interface. - A Python FastAPI application backend. - Supabase-hosted
PostgreSQL for structured data. - Supabase Storage for quotation and
supporting documents. - A workflow/agent layer using LangGraph for
selected AI-assisted tasks. - External email and supplier-data
integrations through replaceable service adapters.

The backend is the trusted application boundary. The browser must not
connect directly to privileged database credentials or external AI
provider secrets.

### 2.2 Product objectives

1.  Centralize purchase requests and supplier information.
2.  Reduce manual RFQ drafting and supplier follow-up work.
3.  Extract comparable fields from supplier quotation documents.
4.  Compare suppliers using explicit, configurable criteria and
    evidence.
5.  Identify missing, expired, unverified or inconsistent supplier
    evidence.
6.  Keep final procurement decisions and binding commitments under human
    control.
7.  Preserve communication, evaluation and approval history.

### 2.3 User classes

  -----------------------------------------------------------------------
  User class                          Main responsibilities
  ----------------------------------- -----------------------------------
  Requester / Department Manager      Create purchase requests, provide
                                      specifications, track status.

  Procurement Officer                 Maintain suppliers, prepare RFQs,
                                      collect quotations and manage
                                      comparisons.

  Approver / Procurement Manager      Review evidence, request
                                      clarification, approve or reject
                                      recommendations and PO drafts.

  Administrator                       Configure users, roles,
                                      organization settings and
                                      integrations.
  -----------------------------------------------------------------------

For the hackathon MVP, role enforcement may initially be limited to a
small set of seeded or authenticated users. The data model should not
assume that every user has unrestricted access.

### 2.4 Operating environment

-   Windows development environment.
-   Modern desktop browser.
-   React + Vite frontend.
-   Python 3.11+ and FastAPI backend.
-   Supabase PostgreSQL and Storage.
-   Internet access for hosted database, LLM and authorized
    integrations.
-   Email integration through a configured mailbox/provider.

### 2.5 Design and implementation constraints

-   The MVP must be deliverable within approximately 10 days.
-   API credentials and database secrets must remain server-side.
-   Supplier discovery and enrichment depend on provider API access,
    quotas and terms.
-   Email receiving requires mailbox API/OAuth or another supported
    inbound mechanism; SMTP alone is for sending.
-   AI-generated values must be traceable to source documents or clearly
    marked as inferred/unverified.
-   Arithmetic, eligibility checks, policy thresholds and approval rules
    must be deterministic backend logic.
-   The MVP must not claim that document analysis guarantees physical
    product quality.

### 2.6 Assumptions and dependencies

-   The organization can provide supplier contacts and internal
    procurement requirements.
-   The team can create and configure a Supabase project.
-   An LLM API key and mailbox integration credentials may be available;
    if not, the related feature must be disabled or demonstrated using
    clearly labelled test fixtures.
-   External supplier information is subject to provider terms, public
    availability and verification limitations.
-   A human approver is available to review purchase recommendations and
    authorize purchase orders.

------------------------------------------------------------------------

## 3. Scope

### 3.1 In scope for MVP

1.  Create, view and track purchase requests.
2.  Maintain an existing supplier directory.
3.  Add newly discovered suppliers with provenance and verification
    status.
4.  Generate RFQ drafts from approved purchase requirements.
5.  Send RFQ emails to selected suppliers after user confirmation.
6.  Associate supplier replies and quotation files with a purchase
    request.
7.  Upload PDF and spreadsheet quotation files.
8.  Extract relevant commercial and technical fields.
9.  Compare quotations and show evidence, missing fields and risk flags.
10. Support human review, approval and rejection.
11. Generate a purchase-order draft from an approved quotation.
12. Store communication and decision history.
13. Record basic delivery/quality outcomes for supplier performance.

### 3.2 Out of scope for initial MVP

-   Autonomous purchasing, payments or legally binding commitments.
-   Autonomous negotiation that sends offers without human
    authorization.
-   Guaranteed physical quality assessment from supplier documents.
-   Full ERP/accounting integration.
-   Complex multi-tenant SaaS subscription and billing.
-   Complete supplier onboarding, KYC or certification authority.
-   Guaranteed discovery of every eligible supplier on the internet.
-   Production-grade support for every email provider.
-   Advanced forecasting and enterprise-scale analytics.

### 3.3 MVP success criteria

The MVP is successful when a user can complete this demonstrable
workflow:

1.  Create a purchase request with quantity, specifications, budget and
    required date.
2.  Select existing suppliers and optionally add a newly discovered
    supplier.
3.  Generate and review an RFQ.
4.  Send the RFQ to selected suppliers, or use clearly identified test
    mailbox fixtures if live mailbox access is unavailable.
5.  Upload supplier quotation documents and associate them with the
    request.
6.  View extracted values alongside source evidence and extraction
    confidence/status.
7.  Compare suppliers using mandatory eligibility checks and
    configurable evaluation criteria.
8.  Review risk flags and approve or reject the recommendation.
9.  Generate a PO draft for the selected supplier.
10. Preserve the PR, RFQ, quotation, evaluation and approval records.

------------------------------------------------------------------------

## 4. High-level system features

### 4.1 Purchase request management

Requesters create purchase requests with product/service name,
description, quantity, specifications, budget, department, priority and
required date. The system validates mandatory fields and tracks request
status.

### 4.2 Supplier management

Procurement users maintain supplier profiles and distinguish existing
suppliers from newly discovered suppliers. Supplier claims and evidence
carry verification states and provenance.

### 4.3 RFQ and email communication

The system prepares RFQ messages and attachments. A user reviews
recipients and content before sending. Incoming supplier responses are
associated with the relevant request and supplier where possible.
Ambiguous messages require manual association.

### 4.4 Quotation intake and extraction

Users upload PDF or spreadsheet quotations. The system extracts fields
such as quoted items, unit price, total price, currency, taxes, delivery
lead time, warranty and payment terms. Users can correct extracted
values.

### 4.5 Supplier evaluation

The system first checks mandatory requirements. A supplier that fails a
mandatory technical or compliance requirement must be visibly flagged
and must not pass solely because of a low price. Eligible suppliers are
compared on configured criteria such as price, evidence of quality
compliance, delivery, reliability, warranty and payment terms.

### 4.6 Approval and PO preparation

An authorized approver reviews the comparison and supporting evidence.
The system records approval/rejection and comments. A PO draft can be
generated only from an approved decision. Sending a PO requires explicit
authorization.

### 4.7 Supplier performance

Users can record actual delivery, inspection results, defects, returns
and service issues. These records may inform future supplier
evaluations. A new supplier with no history is marked as having
insufficient history, not automatically poor performance.

------------------------------------------------------------------------

## 5. External interfaces

### 5.1 User interface

The web UI provides dashboard, purchase request, supplier, RFQ/email,
quotation, comparison, approval and purchase-order views.

### 5.2 Software interfaces

-   FastAPI REST endpoints for frontend operations.
-   PostgreSQL connection through SQLAlchemy or an equivalent backend
    data layer.
-   Supabase Storage API for document storage.
-   LLM provider API through a backend adapter.
-   Gmail API or Microsoft Graph for mailbox integration, subject to
    OAuth permissions.
-   Olostep and Crustdata through server-side adapters if enabled and
    permitted.

### 5.3 Communication interfaces

-   HTTPS for browser-to-backend and backend-to-provider communication.
-   OAuth for supported mailbox integrations.
-   SMTP may be used for outbound mail where appropriate.
-   Webhooks or periodic synchronization may be used for inbound message
    updates, depending on provider support.

------------------------------------------------------------------------

## 6. Data requirements

Core entities:

-   Organization (future-ready; required before multi-tenant
    production).
-   User and role.
-   PurchaseRequest.
-   Supplier.
-   SupplierEvidence.
-   RFQ.
-   EmailMessage.
-   Quotation.
-   QuotationLineItem.
-   Evaluation and EvaluationCriterion.
-   Approval.
-   PurchaseOrder.
-   SupplierPerformanceRecord.
-   AuditEvent.

Every uploaded document should have metadata including
owner/organization, file type, storage path, upload time, source and
related procurement record. Do not store secrets in business tables.

------------------------------------------------------------------------

## 7. Security, privacy and audit

-   Authenticate users before accessing business records.
-   Enforce role-based permissions for approval and PO sending.
-   Scope records to the correct organization before enabling multiple
    organizations.
-   Keep database service credentials, LLM keys and mailbox tokens on
    the backend only.
-   Use least-privilege provider scopes.
-   Validate uploaded file type and size; scan files where
    infrastructure permits.
-   Restrict document access using private storage and short-lived
    signed URLs.
-   Record who created, edited, approved, rejected or sent consequential
    records.
-   Do not treat email or document content as trusted system
    instructions. It is untrusted business data and must not override
    agent policies.
-   Apply retention and deletion policies appropriate to business and
    legal requirements.

------------------------------------------------------------------------

## 8. Acceptance criteria

  -----------------------------------------------------------------------
  ID                                  Acceptance criterion
  ----------------------------------- -----------------------------------
  AC-01                               A requester can create a valid
                                      purchase request and retrieve it
                                      later.

  AC-02                               A procurement user can create and
                                      update supplier profiles.

  AC-03                               An RFQ draft can be generated from
                                      a purchase request and reviewed
                                      before sending.

  AC-04                               A quotation PDF or spreadsheet can
                                      be uploaded and linked to a
                                      supplier and request.

  AC-05                               Extracted quotation values are
                                      editable and visibly distinguish
                                      extracted, missing and
                                      user-corrected data.

  AC-06                               Supplier comparison shows mandatory
                                      requirement failures separately
                                      from weighted scoring.

  AC-07                               The system displays evidence and
                                      risk flags supporting the
                                      evaluation.

  AC-08                               An authorized approver can approve
                                      or reject with a recorded decision.

  AC-09                               A PO draft cannot be sent without
                                      the required approval and explicit
                                      send action.

  AC-10                               Relevant actions and email
                                      communications are recorded and
                                      retrievable.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 9. Risks and mitigations

  -----------------------------------------------------------------------
  Risk                                Mitigation
  ----------------------------------- -----------------------------------
  Supplier data is inaccurate         Store source and verification
                                      state; require human verification
                                      for important claims.

  AI extraction is incorrect          Show source document,
                                      confidence/status and editable
                                      fields; do not silently accept
                                      uncertain values.

  Email replies cannot be matched     Use RFQ reference IDs in
                                      subject/body; allow manual
                                      association.

  Mailbox API access is delayed       Keep email provider behind an
                                      adapter; demonstrate with test
                                      mailbox or manual upload while
                                      clearly labelling it.

  LLM output is inconsistent          Validate structured output and use
                                      deterministic business rules for
                                      calculations and eligibility.

  New suppliers lack history          Mark history as unavailable; do not
                                      treat missing history as a negative
                                      score.

  Sensitive documents are exposed     Private storage, authentication,
                                      authorization and short-lived
                                      signed access.

  Hackathon scope grows               Prioritize end-to-end procurement
                                      workflow before optional
                                      integrations.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 10. Future enhancements

-   Deeper Olostep supplier discovery and web research.
-   Crustdata company enrichment and contact discovery.
-   Microsoft 365 and additional mailbox providers.
-   Multi-tenant organization management and fine-grained RBAC.
-   ERP/accounting integrations.
-   Advanced supplier performance analytics.
-   Configurable procurement policies and approval chains.
-   More document formats and multilingual extraction.
