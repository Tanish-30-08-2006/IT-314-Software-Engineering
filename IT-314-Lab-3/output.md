=== Smart Campus Cafeteria Requirements ===

--- STAKEHOLDERS ---
Based on the case study provided, here is the structured list of primary, secondary, and administrative stakeholders, complete with a one-sentence justification for each role:

### **Primary Stakeholders**
*Direct users who interact with the core ordering and fulfillment process daily.*

1. **Students**
   * *Justification:* They are the primary end-users who will use the digital system to place orders, track preparation times, and provide feedback.
2. **Cafeteria Vendors / Food Court Merchants**
   * *Justification:* They will use the platform to manage incoming digital orders, update inventory, and track sales to reduce waste and stock-outs.

---

### **Secondary Stakeholders**
*Individuals or groups impacted by the system's outcomes, operations, or data, but who do not directly place or fulfill food orders.*

3. **Hostel Wardens**
   * *Justification:* They need access to oversight tools within the system to track and manage meal plans for hostel students.
4. **Kitchen / Operational Staff**
   * *Justification:* They are responsible for preparing the food based on real-time digital orders and updating prep statuses in the system.

---

### **Administrative Stakeholders**
*Management and governing bodies responsible for high-level oversight, policy, and system governance.*

5. **Campus Administration / Management**
   * *Justification:* They require oversight tools to monitor pricing, hygiene standards, vendor performance, and overall value without relying exclusively on manual inspections.
6. **System Administrators / IT Support**
   * *Justification:* They are responsible for deploying, maintaining, and managing the technical infrastructure of the digital ordering and feedback platform.

--- GOALS & PAIN POINTS ---
Here is the structured mapping of explicit pain points and desired outcomes (goals) for each stakeholder group based on the case study:

---

### **Primary Stakeholders**

#### **1. Students**
* **Explicit Pain Points:**
  * Unpredictably long queues leading to wasted time and overcrowding/frustration.
  * Lack of transparency regarding food preparation times (waiting blindly).
  * Slow manual cash/card payment handling and frequent order/billing errors.
  * Informal, inefficient feedback channels (word of mouth) where complaints go unheard.
* **Desired Outcomes (Goals):**
  * Ability to place orders digitally ahead of time to skip physical lines.
  * Real-time tracking of order status and estimated pickup times.
  * Fast, seamless digital transactions.
  * A structured feedback loop to easily report issues or rate their experience.

#### **2. Cafeteria Vendors / Food Court Merchants**
* **Explicit Pain Points:**
  * Manual inventory management leading to severe food wastage or unexpected stock-outs.
  * Difficulty handling high volumes of verbal orders during peak hours, causing chaos and errors.
  * Lack of streamlined sales tracking and data-driven insights.
* **Desired Outcomes (Goals):**
  * A centralized platform to manage incoming digital orders efficiently.
  * Real-time inventory tracking to minimize food waste and prevent stock-outs.
  * Automated sales tracking to monitor daily performance and revenue.

---

### **Secondary Stakeholders**

#### **3. Hostel Wardens**
* **Explicit Pain Points:**
  * Lack of visibility into how hostel students are utilizing their meal plans through manual systems.
  * Difficulty tracking and auditing student meal consumption efficiently.
* **Desired Outcomes (Goals):**
  * Access to dedicated oversight tools within the system to track and manage hostel student meal plans.
  * Better accountability and data access regarding student food utilization.

#### **4. Kitchen / Operational Staff**
* **Explicit Pain Points:**
  * Confusion and pressure from managing unorganized verbal orders during rush hours.
  * Lack of a synchronized workflow to communicate prep statuses, leading to bottlenecks.
* **Desired Outcomes (Goals):**
  * Clear, sequential digital order queues to streamline food preparation.
  * Easy-to-use interface to update prep statuses in real-time so orders flow smoothly to students.

---

### **Administrative Stakeholders**

#### **5. Campus Administration / Management**
* **Explicit Pain Points:**
  * Heavy reliance on slow, manual inspections to monitor pricing, hygiene, and vendor compliance.
  * Inability to easily track overall vendor performance or campus food service quality at scale.
* **Desired Outcomes (Goals):**
  * High-level oversight tools to monitor vendor pricing, hygiene standards, and service value digitally.
  * Access to structured feedback and performance metrics to make informed governance decisions without manual-only interventions.

#### **6. System Administrators / IT Support** *(Implied/Secondary Impact)*
* **Explicit Pain Points:**
  * Potential system downtime, software bugs, or integration hurdles during peak campus hours.
  * Managing user accounts, security, and technical glitches across multiple user groups (students, vendors, admin).
* **Desired Outcomes (Goals):**
  * A stable, secure, and scalable digital ordering and feedback platform.
  * Easy-to-maintain technical infrastructure with minimal downtime and robust user management capabilities.

--- ELICITATION TECHNIQUES ---
Based on the stakeholders, their group sizes, accessibility, and the depth of insights required, here is the optimal requirements elicitation technique paired with a justification for each group:

---

### **1. Students**
* **Optimal Technique:** **Questionnaires / Surveys** (supplemented by a small focus group).
* **Justification:** 
  * *Group Size:* Very large, highly distributed, and constantly fluctuating.
  * *Accessibility:* Easy to reach digitally (via email, student portals, or campus apps).
  * *Depth of Insights:* While qualitative depth per student is low, surveys allow you to capture broad quantitative data (e.g., peak hours, average wait times, frequency of errors) across the entire student body efficiently. 

### **2. Cafeteria Vendors / Food Court Merchants**
* **Optimal Technique:** **Semi-structured Interviews** & **Observations**.
* **Justification:**
  * *Group Size:* Small to medium, highly localized.
  * *Accessibility:* Readily accessible on-site during operational hours, though busy.
  * *Depth of Insights:* High depth is required. Vendors have complex daily workflows (inventory, cash handling, rush-hour chaos) that cannot be captured via surveys. Interviews uncover operational bottlenecks, while observations during a lunch rush reveal actual physical constraints and layout issues they might forget to mention.

---

### **3. Hostel Wardens**
* **Optimal Technique:** **Semi-structured Interviews**.
* **Justification:**
  * *Group Size:* Small (typically one per hostel or a small administrative committee).
  * *Accessibility:* Highly accessible via scheduled appointments or office visits.
  * *Depth of Insights:* High depth is needed regarding meal plan tracking, compliance, and auditing rules. Interviews allow the analyst to explore specific reporting requirements and administrative constraints without taking up excessive time.

---

### **4. Kitchen / Operational Staff**
* **Optimal Technique:** **Observations** (Contextual Inquiry).
* **Justification:**
  * *Group Size:* Medium-sized teams working inside the kitchens.
  * *Accessibility:* Accessible directly in their work environment, though high-pressure during peak times.
  * *Depth of Insights:* Critical operational depth. Kitchen staff may struggle to articulate their workflow in a boardroom interview because it is fast-paced and muscle-memory driven. Observing them during a rush hour reveals physical layout limitations, display visibility needs, and exact interaction points with current unorganized orders.

---

### **5. Campus Administration / Management**
* **Optimal Technique:** **Semi-structured Interviews** & **Audits** (of current manual reporting/inspection processes).
* **Justification:**
  * *Group Size:* Small executive group.
  * *Accessibility:* Requires scheduled, formal meetings.
  * *Depth of Insights:* High-level strategic and governance insights are needed. Interviews help define high-level KPIs, compliance rules, and oversight dashboards. Auditing existing manual inspection documents helps translate current compliance standards into digital parameters.

---

### **6. System Administrators / IT Support**
* **Optimal Technique:** **Technical Document Analysis & Structured Workshops**.
* **Justification:**
  * *Group Size:* Small, specialized technical team.
  * *Accessibility:* Easily accessible via technical planning sessions.
  * *Depth of Insights:* Deep architectural, security, scalability, and integration requirements are needed. Workshops allow the IT team to map out system dependencies, user role permissions, hosting constraints, and potential failure points to ensure the platform is stable and secure.

--- ELICITATION INSTRUMENTS ---
Here are the generated elicitation instruments tailored to each stakeholder group based on the selected techniques.

---

### **1. Students: Questionnaire / Survey Instrument**
*Mode: Digital Survey (Campus App / Email Link)*

**Objective:** Capture broad quantitative data regarding student ordering habits, pain points, and usability expectations.

1. **How frequently do you use the campus cafeteria or food court services?**
   * [ ] Daily (Once or multiple times)
   * [ ] 2–3 times a week
   * [ ] Once a week
   * [ ] Rarely / Never
2. **On average, how long are you willing to wait in line for a meal during peak lunch hours?**
   * [ ] Less than 5 minutes
   * [ ] 5–10 minutes
   * [ ] 10–15 minutes
   * [ ] More than 15 minutes *(Admin oversight: Helps establish acceptable SLA/performance benchmarks for the new system)*
3. **Rank the following features in order of importance for a new campus food ordering app (1 = Most Important, 5 = Least Important):**
   * [ ] Pre-ordering meals ahead of time
   * [ ] Digital payments (Campus card, UPI, credit/debit)
   * [ ] Real-time order status tracking (e.g., "Preparing" vs. "Ready")
   * [ ] Viewing nutritional information / allergen alerts
   * [ ] Loyalty programs or student discounts
4. **Have you ever experienced issues with order accuracy, missing items, or payment failures? If yes, how frequently?**
   * [ ] Never
   * [ ] Occasionally (1-2 times a month)
   * [ ] Frequently (Weekly)
5. **Open-Ended:** What is your biggest frustration with the current campus food ordering and dining process?

---

### **2. Cafeteria Vendors / Food Court Merchants: Interview Guide & Observation Checklist**
*Mode: On-site Semi-Structured Interview*

**Objective:** Uncover operational bottlenecks, inventory management challenges, and daily cash-handling constraints.

**Interview Questions:**
1. **Workflow & Order Management:** Walk me through what happens from the moment an order is placed by a student to the moment it is handed over. Where do bottlenecks or miscommunications usually occur?
2. **Inventory & Menu Updates:** How do you currently update your daily menu items or notify customers when an item is sold out? How long does this take?
3. **Financials & Reconciliation:** What payment methods do you currently accept (cash, digital, meal points), and how do you reconcile daily sales at the end of a shift? *(Admin oversight: Ensure compliance with campus financial auditing rules).*
4. **Hardware & Space:** What physical space do you have at the counter for displaying screens, receipt printers, or point-of-sale (POS) hardware? 

**Observation Checklist (To be filled out during peak lunch rush):**
* [ ] Track time elapsed between customer approaching the counter and order placement.
* [ ] Observe how orders are queued (Are they written on paper, shouted to the kitchen, or entered into a machine?).
* [ ] Note physical constraints (e.g., glare on screens, lack of counter space for digital devices, bottlenecks in pickup areas).

---

### **3. Hostel Wardens: Semi-Structured Interview Guide**
*Mode: Scheduled Office Interview*

**Objective:** Define meal plan tracking, compliance rules, subsidy management, and automated reporting requirements.

**Interview Questions:**
1. **Meal Plan Oversight:** How do you currently track which hostel students have opted into specific meal plans or subsidies? How are changes or cancellations handled?
2. **Compliance & Auditing:** Are there specific university regulations or dietary compliance standards (e.g., mandatory subsidized meals, curfew-related dining rules) that the system must enforce? *(Admin oversight: Ensure institutional policy alignment).*
3. **Dispute Resolution:** When a student disputes a meal charge or claims a missed meal, what is the current process for verifying and resolving the issue?
4. **Reporting Requirements:** What kind of summary reports (weekly/monthly consumption, wastage, budget utilization) do you need to submit to campus administration, and how are they generated currently?

---

### **4. Kitchen / Operational Staff: Contextual Inquiry & Observation Guide**
*Mode: On-site Observation during Peak Hours*

**Objective:** Understand fast-paced, muscle-memory driven workflows, display visibility needs, and interaction points with order tickets.

**Observation Guide & Prompting Questions:**
1. **Kitchen Display & Visibility:** *Observe:* Where are cooks looking when preparing food? Are paper tickets pinned, clipped, or lying on counters? *Prompt:* "If you had a digital screen here instead of paper, what information would you need to see at a glance (e.g., cooking time, special instructions, order number)?"
2. **Physical Ergonomics & Safety:** *Observe:* Are kitchen staff handling devices with wet, greasy, or gloved hands? *Note:* System requirements must account for touchless, water-resistant, or large-button interfaces.
3. **Handoff Coordination:** *Observe:* How does the cook signal to the counter staff that an order is complete? Where does the communication break down most often?

---

### **5. Campus Administration / Management: Interview & Audit Protocol**
*Mode: Executive Stakeholder Meeting & Document Audit*

**Objective:** Define high-level KPIs, institutional governance, compliance rules, and oversight dashboards.

**Interview Questions:**
1. **Strategic Goals:** What are the primary institutional goals for digitizing the campus dining system (e.g., reducing food waste, improving student satisfaction, financial transparency)?
2. **User Roles & Permissions:** What hierarchical access levels are required? (e.g., Super Admin, Hostel Warden, Vendor Manager, Student, Auditor).
3. **Data Privacy & Security:** Are there institutional or regulatory compliance mandates (like data privacy laws or campus safety codes) regarding student spending data and personal information? *(Admin oversight: Establish data retention and security policies).*
4. **Key Performance Indicators (KPIs):** What metrics must the executive dashboard display to measure the success of the platform (e.g., average turnaround time, daily revenue, peak load times)?

**Current Process Audit Checklist:**
* [ ] Review current manual inspection sheets for hygiene and safety compliance.
* [ ] Examine current vendor contract terms regarding commission splits, transaction fees, and reporting timelines to ensure they are digitized correctly.

---

### **6. System Administrators / IT Support: Technical Workshop Agenda**
*Mode: Technical Planning Session*

**Objective:** Map out system dependencies, user role permissions, hosting constraints, and integration points.

**Workshop Agenda & Discussion Prompts:**
1. **Infrastructure & Hosting:** 
   * *Prompt:* Will this system be hosted on-premise on campus servers, or on a cloud infrastructure (AWS/Azure)? What are our scalability requirements during peak start-of-semester rushes?
2. **System Integrations:** 
   * *Prompt:* What existing campus systems must this application integrate with (e.g., Single Sign-On (SSO) student databases, existing campus card/wallet systems, financial ERP)?
3. **Security & Authentication:** 
   * *Prompt:* What protocols will be used for authentication (OAuth 2.0, LDAP)? How will role-based access control (RBAC) be managed for admins, vendors, and students?
4. **Maintenance & Backup:** 
   * *Prompt:* What are the RPO (Recovery Point Objective) and RTO (Recovery Time Objective) requirements in case of a system outage during meal times? What is the offline contingency plan if the internet drops?

--- FINAL FRs AND NFRs ---
Based on the synthesized analysis of the case study and the stakeholder elicitation instruments, here are the final system requirements for the Smart Campus Cafeteria / Food Court Ordering & Feedback System.

---

### **1. Functional Requirements (FRs)**

#### **User Authentication & Management (FR-AUTH)**
*   **FR-1.1:** The system shall authenticate users via Campus Single Sign-On (SSO / LDAP / OAuth 2.0).
*   **FR-1.2:** The system shall implement Role-Based Access Control (RBAC) supporting distinct user roles: *Student, Vendor Manager, Kitchen Staff, Hostel Warden, System Admin, and Auditor*.
*   **FR-1.3:** The system shall allow users to manage their profiles, including dietary preferences, allergies, and contact details.

#### **Digital Menu & Ordering (FR-MENU)**
*   **FR-2.1:** Vendors shall be able to create, update, and manage their daily digital menus, including item descriptions, pricing, nutritional information, and allergen alerts.
*   **FR-2.2:** Vendors shall be able to mark items as "sold out" in real-time, instantly reflecting the change on the student-facing app.
*   **FR-2.3:** Students shall be able to browse menus, customize orders (e.g., special instructions), and pre-order meals ahead of time.
*   **FR-2.4:** The system shall support multiple digital payment methods, including campus cards/wallets, UPI, credit/debit cards, and subsidized meal points.

#### **Order Processing & Real-Time Tracking (FR-TRACK)**
*   **FR-3.1:** The system shall display incoming orders on a Kitchen Display System (KDS) with order numbers, timestamps, and special instructions.
*   **FR-3.2:** Kitchen/Operational staff shall be able to update order statuses (e.g., *Received -> Preparing -> Ready for Pickup -> Completed*).
*   **FR-3.3:** Students shall receive real-time push notifications and live UI updates regarding their order status to reduce physical queue crowding.

#### **Inventory & Sales Management (FR-INV)**
*   **FR-4.1:** Vendors shall be able to track raw material inventory and receive low-stock or stock-out alerts to minimize food wastage.
*   **FR-4.2:** The system shall automatically reconcile daily sales, transactions, and commission splits per shift for vendor financial auditing.

#### **Hostel Meal Plan & Subsidy Management (FR-HOSTEL)**
*   **FR-5.1:** Hostel wardens shall be able to manage, track, and modify student meal plans, subsidies, and curfew-related dining rules.
*   **FR-5.2:** The system shall allow wardens and students to log, verify, and resolve meal charge disputes or missed-meal claims.
*   **FR-5.3:** The system shall generate automated weekly/monthly consumption, wastage, and budget utilization reports for wardens.

#### **Feedback & Governance Loop (FR-FEEDBACK)**
*   **FR-6.1:** Students shall be able to submit structured ratings and feedback on food quality, order accuracy, and hygiene post-consumption.
*   **FR-6.2:** Campus Administration shall have oversight dashboards displaying institutional KPIs (e.g., average turnaround times, daily revenue, peak load hours, and feedback scores).
*   **FR-6.3:** Administrators shall be able to review digital hygiene, safety compliance checklists, and vendor contract performance metrics.

---

### **2. Non-Functional Requirements (NFRs)**

#### **Performance & Scalability (NFR-PERF)**
*   **NFR-1.1:** The system shall handle peak load traffic (e.g., lunch rush and start-of-semester surges) with zero downtime, maintaining an API response time of under 2 seconds.
*   **NFR-1.2:** The order placement and KDS synchronization delay shall not exceed 1 second to support fast-paced kitchen environments.

#### **Reliability & Availability (NFR-REL)**
*   **NFR-2.1:** The system shall maintain high availability (99.9% uptime) during operational cafeteria hours.
*   **NFR-2.2:** The system shall provide an offline contingency mode (or local caching) for order logging and POS execution in the event of temporary campus internet drops.
*   **NFR-2.3:** Recovery Point Objective (RPO) and Recovery Time Objective (RTO) must adhere to institutional disaster recovery policies to prevent financial or order data loss.

#### **Security & Data Privacy (NFR-SEC)**
*   **NFR-3.1:** All data in transit shall be encrypted using TLS 1.3, and data at rest (including student spending data and personal information) must be encrypted following institutional security mandates.
*   **NFR-3.2:** Payment processing modules shall comply with standard financial security guidelines (e.g., PCI-DSS compliance for digital transactions).

#### **Usability & Ergonomics (NFR-USAG)**
*   **NFR-4.1:** The student-facing mobile/web application shall feature an intuitive UI with high contrast, accessibility standards (WCAG 2.1 AA), and clear navigation.
*   **NFR-4.2:** Kitchen Display System (KDS) and vendor POS interfaces shall feature large, water-resistant, and touch-friendly buttons to accommodate staff handling devices in high-stress, greasy, or gloved environments.
*   **NFR-4.3:** Hardware deployment must account for physical constraints at counters (e.g., anti-glare screen visibility, compact receipt printer sizing).

#### **Maintainability & Integration (NFR-MAINT)**
*   **NFR-5.1:** The system shall cleanly integrate with existing campus infrastructure, including SSO directories, campus card databases, and financial ERP systems via secure RESTful APIs.
*   **NFR-5.2:** Cloud-based infrastructure (e.g., AWS/Azure) or campus-hosted architecture shall allow modular updates and automated backups without disrupting active dining shifts.
