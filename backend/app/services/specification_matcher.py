import re


def normalize_value(value):
    """Normalize values for basic, case-insensitive comparison."""
    if value is None:
        return ""

    return re.sub(r"\s+", "", str(value)).lower()


def compare_specifications(
    requested_specs: dict,
    quoted_specs: list
) -> dict:
    """
    Compare purchase request specifications with
    specifications extracted from a supplier quotation.
    """

    # Convert Gemini's list of key-value pairs into a dictionary
    quoted_dict = {
        item["name"]: item.get("value")
        for item in quoted_specs
        if item.get("name")
    }

    results = []

    matched = 0
    mismatched = 0
    missing = 0

    for name, requested_value in requested_specs.items():

        quoted_value = next(
            (
                value
                for key, value in quoted_dict.items()
                if normalize_value(key) == normalize_value(name)
            ),
            None
        )

        if quoted_value is None or str(quoted_value).strip() == "":
            status = "missing"
            missing += 1

        elif normalize_value(requested_value) == normalize_value(quoted_value):
            status = "match"
            matched += 1

        else:
            status = "mismatch"
            mismatched += 1

        results.append({
            "specification": name,
            "requested": requested_value,
            "quoted": quoted_value,
            "status": status
        })

    total = len(requested_specs)

    return {
        "total_specifications": total,
        "matched": matched,
        "mismatched": mismatched,
        "missing": missing,
        "match_percentage": round(
            (matched / total) * 100, 2
        ) if total else 0,
        "overall_status": (
            "match" if total > 0 and matched == total
            else "review_required"
        ),
        "details": results
    }