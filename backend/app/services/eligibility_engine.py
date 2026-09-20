from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.family import Family
from app.models.scheme import Scheme, SchemeRule
from app.models.person import Person
from app.models.family_membership import FamilyMembership

class EligibilityEngine:
    """
    Evaluates a family's eligibility for government schemes based on dynamic rules.
    """
    
    @staticmethod
    def evaluate_scheme(scheme: Scheme, family: Family, members: List[FamilyMembership]) -> Dict[str, Any]:
        result = {
            "scheme_id": scheme.id,
            "scheme_name": scheme.name,
            "description": scheme.description,
            "required_documents": scheme.required_documents,
            "eligible": True,
            "matched_rules": [],
            "failed_rules": []
        }
        
        if not scheme.rules:
            # If a scheme has no rules, it's universally eligible.
            result["matched_rules"].append("No specific eligibility rules required.")
            return result
            
        for rule in scheme.rules:
            rule_passed = EligibilityEngine._evaluate_rule(rule, family, members)
            if rule_passed:
                result["matched_rules"].append(rule.description)
            else:
                result["failed_rules"].append(rule.description)
                result["eligible"] = False
                
        return result
        
    @staticmethod
    def evaluate_all_schemes(db: Session, family_id: int) -> List[Dict[str, Any]]:
        family = db.query(Family).filter(Family.id == family_id).first()
        members = db.query(FamilyMembership).filter(
            FamilyMembership.family_id == family_id,
            FamilyMembership.status == "ACTIVE"
        ).all()
        
        # Load persons for members
        for m in members:
            m.person = db.query(Person).filter(Person.id == m.person_id).first()
            
        schemes = db.query(Scheme).filter(Scheme.is_active == True).all()
        
        results = []
        for scheme in schemes:
            res = EligibilityEngine.evaluate_scheme(scheme, family, members)
            results.append(res)
            
        return results

    @staticmethod
    def _evaluate_rule(rule: SchemeRule, family: Family, members: List[FamilyMembership]) -> bool:
        config = rule.rule_config
        field = config.get("field")
        op = config.get("operator")
        expected_value = config.get("value")
        
        if rule.target == "FAMILY":
            actual_value = getattr(family, field, None)
            return EligibilityEngine._compare(actual_value, op, expected_value)
            
        elif rule.target == "MEMBER":
            # For member rules, ANY member satisfying the rule makes it pass for the family
            for member in members:
                person = member.person
                if not person:
                    continue
                    
                actual_value = getattr(person, field, None)
                
                # Special handling for age which needs to be calculated from date_of_birth
                if field == "age":
                    if not person.date_of_birth:
                        continue
                    from datetime import date
                    today = date.today()
                    actual_value = today.year - person.date_of_birth.year - ((today.month, today.day) < (person.date_of_birth.month, person.date_of_birth.day))
                
                if EligibilityEngine._compare(actual_value, op, expected_value):
                    return True
            return False
            
        return False
        
    @staticmethod
    def _compare(actual: Any, op: str, expected: Any) -> bool:
        if actual is None:
            return False
            
        # Type casting for comparison
        try:
            if isinstance(expected, int) or isinstance(expected, float):
                actual = float(actual)
                expected = float(expected)
        except (ValueError, TypeError):
            pass
            
        if op == "==":
            return actual == expected
        elif op == "!=":
            return actual != expected
        elif op == ">":
            return actual > expected
        elif op == ">=":
            return actual >= expected
        elif op == "<":
            return actual < expected
        elif op == "<=":
            return actual <= expected
        elif op == "IN":
            return actual in expected
            
        return False
