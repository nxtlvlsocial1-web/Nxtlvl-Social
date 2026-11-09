# Nxtlvl Ledger

Client, invoice and money manager for Nxtlvl Social, built for Indian rules. One self-contained page (`index.html`),
published as a private claude.ai artifact: https://claude.ai/artifact/7SGeMGrvWrMmVLDxkBfRyu

Data lives in the artifact's own database (readable and writable only by the owner and anyone they make an Editor).
Opened outside claude.ai, the same page falls back to saving in the browser.

## What it does
- **Clients & brands**: GSTIN auto-fills state and PAN; billing currency, TDS rate, payment terms, monthly retainer and bill day.
  Per-client GST setting: Auto (follows your own GST registration), Charge GST, or No GST.
- **Invoices**: numbered PREFIX/26-27/001 (restarts each April); CGST+SGST or IGST from place of supply, export under LUT,
  or no GST, with an Applicable / Not applicable switch on every invoice; SAC codes; TDS shown with net payable; amount in words (Indian system); UPI QR for the amount due;
  download as HTML (print to PDF); copy or WhatsApp a payment reminder; duplicate, cancel, mark fully paid.
- **Payments**: against an invoice (pre-fills balance and TDS) or as other income (brand deals, AdSense, affiliate);
  UPI/NEFT/IMPS/RTGS/cash/cheque/PayPal/Wise, UTR reference, foreign currency with INR credited.
- **Expenses**: categories, GST input credit, monthly/yearly repeats, client-linked costs.
- **Deals**: brand and client pipeline from lead to delivered, with "create invoice" when won.
- **Overview**: revenue excl. GST, cash in, outstanding/overdue, expenses, net profit, monthly retainers; revenue vs
  expenses chart by FY month; GST payable this quarter, TDS to claim, income-tax set-aside, progress to the ₹20 L limit;
  overdue invoices, retainers to bill, deals to chase; GSTR-1/3B, advance tax and ITR due dates.
- **Reports**: P&L by month, GST by quarter (output, ITC, net), TDS by client; CSV exports for the CA; full JSON backup/restore.

Example records (marked "Example") were seeded for the first look; the banner's **Clear example data** removes them.
Tax figures are estimates for planning; confirm filings with a CA.
