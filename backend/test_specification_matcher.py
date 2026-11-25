from app.services.specification_matcher import compare_specifications


# Original purchase request from Supabase
requested_specs = {
    "grade": "SS 304",
    "thickness": "2mm",
    "finish": "Matte"
}


# Gemini extracted quotation data
quoted_specs = [
    {"name": "Grade", "value": "SS 304"},
    {"name": "Thickness", "value": "2mm"},
    {"name": "Finish", "value": "Matte"}
]


result = compare_specifications(
    requested_specs,
    quoted_specs
)

print("\n===== SPECIFICATION COMPARISON =====")

for item in result["details"]:
    print(
        f'{item["specification"]}: '
        f'Requested={item["requested"]}, '
        f'Quoted={item["quoted"]}, '
        f'Status={item["status"]}'
    )

print("\n===== SUMMARY =====")
print(result)