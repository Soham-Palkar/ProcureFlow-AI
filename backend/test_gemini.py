from app.services.quotation_analyzer import analyze_quotation

sample_quotation = """
ABC Industrial Supplies

Quotation Number: QTN-2026-105

Product: Stainless Steel Sheets
Grade: SS 304
Thickness: 2mm
Finish: Matte

Quantity: 500 kg
Unit Price: INR 250
Total Amount: INR 125000

Delivery: 12 days
Warranty: 1 year
Payment Terms: 30% advance, 70% after delivery
Quotation Validity: 30 days
"""

result = analyze_quotation(sample_quotation)

print("\n===== GEMINI QUOTATION ANALYSIS =====")
print(result["data"])