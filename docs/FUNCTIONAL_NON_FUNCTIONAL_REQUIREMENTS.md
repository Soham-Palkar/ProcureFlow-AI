# Functional and Non-Functional Requirements

## ProcureFlow AI --- MVP

**Document version:** 1.0\
**Status:** Initial baseline

Priority definitions: - **P0 --- Must:** Required for the end-to-end
MVP. - **P1 --- Should:** Important, but can be simplified for the
hackathon. - **P2 --- Could:** Optional enhancement if time permits.

------------------------------------------------------------------------

# Part A --- Functional Requirements

## FR-01: User access and roles

  -----------------------------------------------------------------------
  ID                      Requirement             Priority
  ----------------------- ----------------------- -----------------------
  FR-01.1                 The system shall        P0
                          require a user to       
                          authenticate before     
                          accessing company       
                          procurement records.    

  FR-01.2                 The system shall        P0
                          distinguish requester,  
                          procurement officer,    
                          approver and            
                          administrator           
                          permissions.            

  FR-01.3                 Only authorized         P0
                          approvers shall approve 
                          or reject procurement   
                          decisions.              

  FR-01.4                 Only users with the     P0
                          appropriate permission  
                          shall send a purchase   
                          order.                  

  FR-01.5                 The system shall        P1
                          associate actions with  
                          the authenticated user. 
  -----------------------------------------------------------------------

For a short hackathon implementation, authentication may use a minimal
role setup, but authorization checks must be enforced by the backend,
not only by hiding UI controls.

## FR-02: Purchase request management

  -----------------------------------------------------------------------
  ID                      Requirement             Priority
  ----------------------- ----------------------- -----------------------
  FR-02.1                 A requester shall       P0
                          create a purchase       
                          request.                

  FR-02.2                 A purchase request      P0
                          shall capture item      
                          name, description,      
                          quantity,               
                          specifications,         
                          department, budget,     
                          priority and required   
                          date where applicable.  

  FR-02.3                 The backend shall       P0
                          validate mandatory      
                          fields and reject       
                          invalid quantities or   
                          malformed data.         

  FR-02.4                 The system shall assign P0
                          a unique purchase       
                          request reference.      

  FR-02.5                 Users shall view and    P0
                          search purchase         
                          requests.               

  FR-02.6                 Authorized users shall  P1
                          update a request before 
                          it enters a             
                          locked/approved stage.  

  FR-02.7                 The system shall track  P0
                          request status and      
                          status changes.         

  FR-02.8                 An AI requirement       P1
                          assistant may identify  
                          missing or ambiguous    
                          specifications and ask  
                          for clarification.      
  -----------------------------------------------------------------------

Suggested statuses: Draft, Submitted, Clarification Required, Approved
for Sourcing, RFQ in Progress, Evaluation, Pending Approval, Approved,
Rejected, PO Created, Closed, Cancelled.

## FR-03: Supplier management and intelligence

  -----------------------------------------------------------------------
  ID                      Requirement             Priority
  ----------------------- ----------------------- -----------------------
  FR-03.1                 Procurement users shall P0
                          create, view, update    
                          and deactivate supplier 
                          profiles.               

  FR-03.2                 A supplier profile      P0
                          shall store company     
                          name and may store      
                          contacts, email, phone, 
                          website, address and    
                          category.               

  FR-03.3                 The system shall        P0
                          distinguish existing    
                          suppliers from newly    
                          discovered suppliers.   

  FR-03.4                 The system shall record P1
                          the source and          
                          verification status of  
                          supplier information.   

  FR-03.5                 The system may discover P1
                          public supplier         
                          candidates through an   
                          approved web research   
                          provider.               

  FR-03.6                 The system may enrich   P2
                          company information     
                          through a permitted     
                          business-data provider. 

  FR-03.7                 The system shall not    P0
                          label a supplier as     
                          certified or verified   
                          without supporting      
                          evidence.               

  FR-03.8                 The system shall        P0
                          indicate when supplier  
                          performance history is  
                          unavailable.            
  -----------------------------------------------------------------------

## FR-04: RFQ management

  -----------------------------------------------------------------------
  ID                      Requirement             Priority
  ----------------------- ----------------------- -----------------------
  FR-04.1                 A procurement user      P0
                          shall create an RFQ     
                          from a purchase         
                          request.                

  FR-04.2                 The RFQ shall include a P0
                          unique reference, item  
                          details, quantity,      
                          specifications,         
                          response deadline and   
                          contact information.    

  FR-04.3                 A user shall select one P0
                          or more suppliers as    
                          RFQ recipients.         

  FR-04.4                 The system shall        P0
                          generate an editable    
                          RFQ email draft.        

  FR-04.5                 The user shall review   P0
                          and confirm recipients  
                          and content before      
                          sending.                

  FR-04.6                 The system shall record P0
                          send status, timestamp, 
                          recipient and provider  
                          message identifier      
                          where available.        

  FR-04.7                 The system shall        P1
                          support reminders for   
                          suppliers who have not  
                          replied.                
  -----------------------------------------------------------------------

## FR-05: Email communication

  -----------------------------------------------------------------------
  ID                      Requirement             Priority
  ----------------------- ----------------------- -----------------------
  FR-05.1                 The system shall send   P0
                          RFQ emails through a    
                          configured email        
                          provider.               

  FR-05.2                 The system shall store  P0
                          sent email metadata and 
                          associate it with the   
                          supplier and RFQ.       

  FR-05.3                 The system should       P1
                          retrieve incoming       
                          supplier replies        
                          through an authorized   
                          mailbox integration.    

  FR-05.4                 The system should       P1
                          associate replies using 
                          RFQ reference, sender   
                          address and             
                          message/thread          
                          metadata.               

  FR-05.5                 The system shall allow  P0
                          manual association when 
                          an incoming email       
                          cannot be matched       
                          confidently.            

  FR-05.6                 The system shall        P1
                          identify and store      
                          attachments for         
                          quotation intake.       

  FR-05.7                 The system may classify P1
                          incoming messages as    
                          quotation,              
                          clarification, decline, 
                          follow-up or other.     

  FR-05.8                 The system shall not    P0
                          send negotiation        
                          messages or POs without 
                          user authorization.     
  -----------------------------------------------------------------------

**Implementation note:** SMTP is sufficient for outbound email only.
Inbound monitoring requires Gmail API, Microsoft Graph, IMAP or another
supported inbound mechanism. The selected provider and its OAuth
permissions must be configured separately.

## FR-06: Quotation intake and extraction

  -----------------------------------------------------------------------
  ID                      Requirement             Priority
  ----------------------- ----------------------- -----------------------
  FR-06.1                 A user shall upload a   P0
                          quotation PDF or        
                          spreadsheet.            

  FR-06.2                 The system shall        P0
                          associate a quotation   
                          with a supplier and     
                          purchase request.       

  FR-06.3                 The system shall        P0
                          extract supplier name,  
                          quotation number, line  
                          items, quantities,      
                          prices, currency,       
                          taxes, delivery,        
                          warranty and payment    
                          terms when present.     

  FR-06.4                 The system shall        P0
                          preserve the original   
                          uploaded document.      

  FR-06.5                 The system shall        P0
                          distinguish extracted,  
                          missing, uncertain and  
                          user-corrected fields.  

  FR-06.6                 The user shall be able  P0
                          to correct extracted    
                          values before           
                          evaluation.             

  FR-06.7                 The system shall flag a P0
                          quotation whose         
                          supplier or request     
                          association is          
                          uncertain.              
  -----------------------------------------------------------------------

## FR-07: Supplier evaluation and comparison

  -----------------------------------------------------------------------
  ID                      Requirement             Priority
  ----------------------- ----------------------- -----------------------
  FR-07.1                 The system shall        P0
                          compare quotations      
                          linked to the same      
                          purchase request.       

  FR-07.2                 The system shall        P0
                          evaluate mandatory      
                          technical and           
                          compliance requirements 
                          separately from         
                          weighted criteria.      

  FR-07.3                 A supplier failing a    P0
                          mandatory requirement   
                          shall be visibly        
                          flagged and shall not   
                          pass solely due to a    
                          low price.              

  FR-07.4                 The system shall        P0
                          compare price,          
                          quality/compliance      
                          evidence, delivery,     
                          reliability, warranty   
                          and payment terms where 
                          data exists.            

  FR-07.5                 Evaluation weights      P1
                          shall be configurable   
                          or clearly documented   
                          as MVP defaults.        

  FR-07.6                 The system shall show   P0
                          missing evidence and    
                          risk flags.             

  FR-07.7                 The system shall        P0
                          explain the basis of    
                          recommendations and     
                          link findings to        
                          quotation or supplier   
                          evidence.               

  FR-07.8                 The system shall not    P0
                          present document-based  
                          compliance as proof of  
                          physical product        
                          quality.                

  FR-07.9                 A new supplier without  P0
                          history shall be marked 
                          as insufficient         
                          history, not            
                          automatically assigned  
                          a poor performance      
                          score.                  
  -----------------------------------------------------------------------

## FR-08: Approval workflow

  -----------------------------------------------------------------------
  ID                      Requirement             Priority
  ----------------------- ----------------------- -----------------------
  FR-08.1                 The system shall        P0
                          present the comparison  
                          and supporting evidence 
                          to an authorized        
                          approver.               

  FR-08.2                 The approver shall be   P0
                          able to approve, reject 
                          or request more         
                          information.            

  FR-08.3                 The system shall record P0
                          approver, decision,     
                          comments and timestamp. 

  FR-08.4                 The system shall        P0
                          prevent unauthorized    
                          users from changing     
                          approval outcomes.      

  FR-08.5                 The system shall        P1
                          preserve prior          
                          decisions in an audit   
                          history.                
  -----------------------------------------------------------------------

## FR-09: Purchase order generation

  -----------------------------------------------------------------------
  ID                      Requirement             Priority
  ----------------------- ----------------------- -----------------------
  FR-09.1                 The system shall        P0
                          generate a PO draft     
                          from an approved        
                          supplier/quotation      
                          selection.              

  FR-09.2                 The PO shall include a  P0
                          unique PO number,       
                          supplier, items,        
                          quantities, agreed      
                          price, currency,        
                          delivery and payment    
                          terms.                  

  FR-09.3                 The system shall        P0
                          generate a downloadable 
                          PDF PO.                 

  FR-09.4                 The system shall        P0
                          require explicit        
                          authorization before    
                          sending the PO.         

  FR-09.5                 The system shall record P0
                          PO status and sending   
                          history.                
  -----------------------------------------------------------------------

## FR-10: Supplier performance

  -----------------------------------------------------------------------
  ID                      Requirement             Priority
  ----------------------- ----------------------- -----------------------
  FR-10.1                 Authorized users shall  P1
                          record actual delivery  
                          dates and inspection    
                          outcomes.               

  FR-10.2                 The system shall record P1
                          defects, returns and    
                          service issues where    
                          known.                  

  FR-10.3                 Historical performance  P1
                          records may inform      
                          future supplier         
                          evaluations.            

  FR-10.4                 The system shall        P0
                          distinguish actual      
                          recorded performance    
                          from supplier-provided  
                          claims.                 
  -----------------------------------------------------------------------

## FR-11: Audit and dashboard

  -----------------------------------------------------------------------
  ID                      Requirement             Priority
  ----------------------- ----------------------- -----------------------
  FR-11.1                 The dashboard shall     P0
                          summarize purchase      
                          requests, suppliers,    
                          quotations and pending  
                          approvals.              

  FR-11.2                 The system shall retain P0
                          key procurement         
                          activity history.       

  FR-11.3                 Users shall view the    P1
                          timeline of a purchase  
                          request, including      
                          RFQs, replies,          
                          quotations, evaluations 
                          and decisions.          
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Part B --- Non-Functional Requirements

The targets below are proposed MVP engineering targets. They should be
validated against the hosting plan, provider quotas and demo
environment.

## NFR-01: Performance

-   NFR-01.1: Typical CRUD API requests should complete within 2 seconds
    under the expected demo workload, excluding external provider calls.
-   NFR-01.2: Long-running document extraction and AI tasks should
    return a task/status response rather than blocking a browser request
    indefinitely.
-   NFR-01.3: The dashboard should load its core summary within 3
    seconds under normal demo conditions.
-   NFR-01.4: The system should paginate supplier, request, email and
    quotation lists as data grows.

## NFR-02: Availability and reliability

-   NFR-02.1: The application should display a clear error when the
    database, email provider or LLM provider is unavailable.
-   NFR-02.2: Failed external calls should not create duplicate RFQs,
    emails or purchase orders when retried.
-   NFR-02.3: Important workflow state should be persisted in
    PostgreSQL.
-   NFR-02.4: The application should not report an email as sent until
    the email provider confirms successful submission.

## NFR-03: Security

-   NFR-03.1: All deployed application traffic shall use HTTPS.
-   NFR-03.2: Authentication and backend authorization shall protect
    procurement records and privileged actions.
-   NFR-03.3: Secrets shall be stored in server-side environment
    variables or a secret manager, never in frontend source code or Git.
-   NFR-03.4: Database access shall use least privilege and
    organization-scoped authorization before production multi-tenant
    use.
-   NFR-03.5: Uploaded files shall be validated by type and size and
    stored privately.
-   NFR-03.6: Email OAuth tokens and API credentials shall be protected
    and revocable.
-   NFR-03.7: AI agents shall treat email bodies, attachments and web
    pages as untrusted input, not as instructions that can override
    system policies.

## NFR-04: Privacy and data handling

-   NFR-04.1: Only the minimum supplier and employee information
    required for procurement shall be collected.
-   NFR-04.2: Sensitive quotations and supplier documents shall not be
    sent to an external LLM unless the organization has reviewed and
    accepted the provider's data terms.
-   NFR-04.3: The system shall support deletion or retention controls
    appropriate to organizational policy.
-   NFR-04.4: Access to quotation documents shall be limited to
    authorized users.

## NFR-05: Usability and accessibility

-   NFR-05.1: The UI shall use consistent navigation and status labels.
-   NFR-05.2: Mandatory fields and validation errors shall be clearly
    identified.
-   NFR-05.3: Supplier comparisons shall make missing information and
    disqualifying requirements visually clear.
-   NFR-05.4: Core desktop workflows shall be usable at common laptop
    resolutions.
-   NFR-05.5: Important actions such as approve, reject and send PO
    shall require clear confirmation.

## NFR-06: Maintainability

-   NFR-06.1: Backend routes, business logic, data access and external
    integrations shall be separated into modules.
-   NFR-06.2: Email, LLM and supplier-data providers shall be accessed
    through replaceable adapters.
-   NFR-06.3: Database schema changes shall be version-controlled
    through migrations or reviewed SQL scripts.
-   NFR-06.4: API request and response schemas shall be validated.
-   NFR-06.5: Environment-specific configuration shall not be
    hard-coded.

## NFR-07: Scalability

-   NFR-07.1: The architecture should support adding background workers
    for email synchronization and document processing.
-   NFR-07.2: The data model should support multiple organizations, even
    if full multi-tenant functionality is not delivered in the first
    demo.
-   NFR-07.3: Document files shall be stored in object storage rather
    than as large binary values in relational tables.
-   NFR-07.4: External provider usage shall be bounded by timeouts,
    quotas and retry policies.

## NFR-08: Explainability and AI quality

-   NFR-08.1: AI-extracted fields shall retain a link to the source
    document or message where possible.
-   NFR-08.2: Uncertain or missing extracted values shall be shown as
    such, not silently invented.
-   NFR-08.3: Price totals, tax calculations, mandatory checks and
    weighted scores shall be computed by deterministic code.
-   NFR-08.4: AI recommendations shall show their criteria and evidence.
-   NFR-08.5: The system shall not claim to verify physical product
    quality solely from documents.
-   NFR-08.6: AI-generated email drafts shall be reviewed by a user
    before sending.

## NFR-09: Auditability

-   NFR-09.1: The system shall record key state transitions and
    consequential actions.
-   NFR-09.2: Approval and PO events shall include actor and timestamp.
-   NFR-09.3: The system shall retain references to the source
    quotations and evidence used for a decision.
-   NFR-09.4: Audit history shall not be silently overwritten by
    ordinary editing operations.

------------------------------------------------------------------------

# Part C --- Verification Matrix

  -----------------------------------------------------------------------
  Requirement group       Verification method     MVP evidence
  ----------------------- ----------------------- -----------------------
  Purchase requests       API and UI test         Create and retrieve a
                                                  PR

  Suppliers               API and UI test         Create, list and update
                                                  supplier

  RFQ/email               Provider integration    Confirmed send record
                          test                    and message ID

  Inbound email           Mailbox integration     Retrieved reply linked
                          test                    to RFQ or queued for
                                                  manual matching

  Quotation extraction    Document test set       Extracted fields
                                                  compared with known
                                                  sample values

  Evaluation              Unit tests              Mandatory checks and
                                                  score calculation

  Approval                Authorization test      Unauthorized approval
                                                  is rejected

  PO                      Workflow test           PO draft created only
                                                  after approval

  Security                Configuration and       No secrets in frontend;
                          access tests            protected endpoints and
                                                  private files

  Audit                   Database/API test       Actor, action and
                                                  timestamp retained
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Part D --- MVP release gate

The MVP should not be considered complete until: 1. A purchase request
can be created and tracked. 2. Supplier records can be managed. 3. RFQs
can be reviewed and sent or clearly demonstrated through an approved
test provider. 4. Quotations can be uploaded and linked. 5. Comparison
results expose evidence, uncertainty and mandatory failures. 6. An
authorized human can approve or reject. 7. A PO draft can be generated
after approval. 8. Key actions and communications are auditable. 9. The
team can demonstrate failure handling for at least one unavailable
external service.
