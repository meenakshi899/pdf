# Odoo Support Scope V1.1 (7 April 2026) - Simple Hindi Guide

## 1) Yeh document kis liye hai?
Yeh guide Aha! Consulting ke Odoo support scope ko **simple language** mein explain karti hai, taaki management, admin team aur technical team sab easily samajh saken.

---

## 2) Overarching Requirements (High-Level Rules)
1. Current Odoo version: **V19**.
2. Saara kaam future upgrades ke liye compatible hona chahiye.
3. Existing database integrity aur customizations ko damage nahi hona chahiye.
4. Naya kaam existing live Odoo ko break kiye bina deploy hona chahiye.
5. Hosting currently custom server par hai:  
   **https://portal.ahaconsulting.net.au/**

---

## 3) IP, License aur Responsibility
1. Jo code/work banega uski IP Aha! Consulting ki hogi.
2. Code reuse pe koi ongoing fee nahi.
3. Aisa code nahi banana jo third-party paid dependency force kare.
4. Agar existing customized code ko damage hota hai, to repair no extra cost par hona chahiye.

---

## 4) Priority 1 - Stripe Credit Card Fee (1.5%)
### Business Need
Company chahti hai ki payment external custom Stripe portal ki jagah **standard Odoo portal flow** se ho, jisse reporting clean ho aur bugs kam hon.

### Required Behavior
Jab customer credit card (Stripe) choose kare:
1. **1.5% surcharge** auto calculate ho.
2. Invoice mein auto ek alag line item add ho.
3. Customer checkbox se acknowledge kare ki credit card fee apply hogi.

### Yeh flow 3 jagah kaam kare
1. Pay an Invoice
2. Book and Pay for Training
3. Purchase a Product

Existing stripe link (reference):  
https://www.ahaconsulting.net.au/stripe-payment

### Suggested Technical Approach (Odoo V19-compatible)
- Company settings mein fee rate field maintain karein (example: 1.5).
- Payment method selection event par surcharge line add/remove logic.
- Product-level dedicated “Stripe Fee Product” use karein.
- Tax treatment accounting team ke rule ke hisaab se set karein.
- Audit trail ke liye chatter/log maintain karein.

---

## 5) Priority 2 - Training Courses Display
### Goal
Website par do views hone chahiye:
1. **Upcoming events** (scheduled with date)
2. **Course portfolio** (evergreen catalog, even if unscheduled)

### Filters required
- Provider type:
  - Aha Academy: public full visibility + booking allowed
  - IAP2: public ko limited details; full course/price login ke baad
- Content type:
  - Engagement, Conflict, Facilitation, Evaluation
- Extra actions:
  - Booking link
  - Downloadable PDF

### Odoo standard limitation (important)
- Odoo standard mein login-status ke base par specific field hide/show direct config se limited hota hai.
- Event ko website par dikhane ke liye date required hoti hai.

### Practical Solution
1. Event Tags se provider/content filters implement karein.
2. Login-based visibility ke liye custom website template logic add karein.
3. “Portfolio” ke liye separate website model/page banayein jahan unscheduled courses bhi visible hon.
4. Event records ke liye scheduled/unscheduled + publish/unpublish toggles add karein.

---

## 6) Priority 3 - Past Work Catalog
### Requirement
Public-facing “Past Work” page jisme:
- Filter by **Sector**
- Filter by **Type of Work**
- Dono filters ek saath kaam karein
- Dynamic results aayein (page reload dependent static listing na ho)

### Content Source
- Spreadsheet-driven data (name, categories, images, PDF links, etc.)
- Non-technical team easily update kar sake

### Recommended Architecture
1. Spreadsheet sync job (scheduled import) -> Odoo custom model.
2. Website card layout (Level 1 summary + Level 2 detail accordion/button).
3. Multi-filter sidebar + dynamic query rendering.
4. Optional cache layer for speed.

---

## 7) Priority 4 - Ongoing AdHoc Support
Agar future mein Odoo.sh move hota hai to support scope mein include ho:
1. Ad-hoc bug fixes
2. Version update support
3. Repository hosting and release hygiene

---

## 8) Attachment/Screenshot Explanation (Simple)
Neeche diye screenshots se current system behavior samajh aata hai:

### Screenshot 1 - Past Work page (empty result)
- Filter panel left side par hai (Sector + Type of Work).
- Message aa raha: “No projects matched your selected filters.”
- Isse clear hai ki filtering setup hai, but data mapping ya filter combination issue ho sakta hai.

### Screenshot 2 - Training Courses listing page
- Upcoming events/portfolio tabs visible hain.
- Search + provider + content type + schedule filters available.
- Course cards with actions (Book, More information, Download PDF) shown.

### Screenshot 3 - Download behavior
- Browser download tray mein files appear ho rahi hain.
- Isse confirm hota hai ki download link action trigger ho raha hai.
- Validate karna hai ki correct file per course bind ho.

### Screenshot 4 - Odoo backend event form
- Custom fields visible: Provider Type, Content Type, Show in Portfolio, Unscheduled Course, Booking Link, More Information Link, Training PDF.
- Yeh dikhata hai ki training catalog customization ka backend foundation present hai.

### Screenshot 5 - Company Stripe Surcharge config
- Company settings mein Stripe Card Fee Rate set hai (example: 1.50%).
- Stripe fee product mapping ka concept available lag raha hai.

### Screenshot 6 - Portal My Account page
- Customer portal functional hai aur invoices/orders access available hai.
- Standard portal flow use karne ka objective realistic hai.

### Screenshot 7 - Portal invoice list with Pay Now
- Multiple invoices par “Pay Now” action visible hai.
- Payment flow portal se accessible hai, surcharge integration isi flow mein fit hogi.

### Screenshot 8 - Payment popup (no provider available)
- Message: “No payment providers are configured.”
- Yeh indicate karta hai ki Stripe/provider activation/configuration incomplete hai.
- Priority 1 deploy se pehle payment provider activation mandatory hai.

---

## 9) Immediate Action Plan (Recommended)
1. Payment provider configuration fix + Stripe test mode validation.
2. Surcharge logic ko invoice/training/product teeno flows mein implement + QA.
3. Training catalog ke login-conditional visibility rules implement.
4. Past Work spreadsheet sync + dynamic filter page implement.
5. UAT checklist bana kar staged rollout karein.

---

## 10) Risk Notes
- Live database par direct changes bina backup ke na karein.
- Existing custom modules ka dependency map pehle banayein.
- Odoo V19 future upgrades ko dhyan mein rakhkar clean modular code likhein.

---

## 11) Final Summary (One Line)
Aapka scope clear hai: **Odoo V19 par stable, upgrade-safe customization** chahiye jisme payment surcharge automation, training catalog controls, past-work dynamic showcase aur ongoing support include ho.
