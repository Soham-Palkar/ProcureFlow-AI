# ProcureFlow AI --- MVP Documentation

This folder contains the initial product and engineering documentation
for ProcureFlow AI.

## Documents

1.  **SRS.md** --- Software Requirements Specification: product context,
    scope, users, assumptions, constraints and acceptance criteria.
2.  **FUNCTIONAL_NON_FUNCTIONAL_REQUIREMENTS.md** --- Detailed
    functional and non-functional requirements with identifiers and
    priorities.
3.  **SYSTEM_ARCHITECTURE_MVP.md** --- MVP architecture, components,
    data flow, deployment view, security boundaries and implementation
    sequence.

## Product summary

ProcureFlow AI is an AI-assisted procurement workflow platform for SMEs
and manufacturers. It helps a company turn an internal purchase
requirement into supplier outreach, quotation collection, evidence-based
comparison, human approval and purchase-order preparation.

The MVP is designed around a human-controlled workflow. AI can extract,
classify, summarize and recommend, but it must not independently approve
purchases, make binding commitments or send purchase orders without
explicit authorization.

## MVP boundary

The first MVP focuses on:

-   Purchase request creation and tracking.
-   Supplier directory for existing and discovered suppliers.
-   RFQ preparation and email sending.
-   Supplier email replies and quotation attachment intake, subject to
    mailbox integration availability.
-   PDF and spreadsheet quotation extraction.
-   Evidence-based quotation comparison and supplier risk flags.
-   Human review and approval.
-   Purchase order draft generation and controlled sending.
-   Basic supplier performance records.

External supplier discovery/enrichment (Olostep and Crustdata),
automated negotiation, advanced analytics, multi-tenant SaaS billing and
ERP integrations are planned extensions unless time and API access
permit them in the hackathon MVP.

## Status and assumptions

These are baseline MVP documents, not a claim that the features have
already been implemented. Requirements should be revised as the team
validates scope, API access, security and the demo workflow.
