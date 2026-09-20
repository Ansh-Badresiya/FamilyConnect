# Eligibility Engine

The Eligibility Engine dynamically evaluates a family's qualifications for government schemes using a rules-based system driven by JSON configurations, rather than hardcoding scheme logic in Python.

## How it works

Each scheme is configured with an array of `SchemeRule` objects. A rule takes the following shape:
```json
{
  "description": "Family annual income must be under ₹3,00,000",
  "target": "FAMILY",
  "rule_config": {
    "field": "annual_income",
    "operator": "<=",
    "value": 300000
  }
}
```

### Targets
- `FAMILY`: The rule is evaluated against the overarching family properties (e.g. `annual_income`, `district`).
- `MEMBER`: The rule is evaluated against every member in the family (e.g. `age`, `occupation`). If **any** member satisfies the rule, the rule passes for the entire family.

### Evaluation
The `EligibilityEngine` service compares the `actual_value` retrieved from the database models against the `expected_value` using the specified `operator` (`==`, `!=`, `<`, `>`, `<=`, `>=`, `IN`).

It returns detailed insights on exactly *why* a scheme is eligible (matched rules) or ineligible (failed rules), providing transparency to the citizen.
