export interface User {
  id: number;
  email: string;
  role: 'CITIZEN' | 'OFFICER';
  person_id?: number;
  is_active: boolean;
}

export interface Person {
  id?: number;
  name: string;
  date_of_birth: string;
  gender: string;
  mobile?: string;
  occupation?: string;
  education?: string;
}

export interface Family {
  id: number;
  family_id: string;
  family_head_person_id?: number;
  annual_income: number;
  address?: string;
  district?: string;
  taluka?: string;
  village?: string;
  members?: FamilyMembership[];
}

export interface FamilyMembership {
  id: number;
  family_id: number;
  person_id: number;
  relationship: string;
  is_head: boolean;
  status: string;
  person: Person;
}

export interface SchemeRule {
  id?: number;
  field_name: string;
  operator: string;
  value: string;
  logical_group: string;
}

export interface Scheme {
  id: number;
  name: string;
  description?: string;
  required_documents?: string;
  is_active: boolean;
}

export interface EligibilityResult {
  scheme_id: number;
  scheme_name: string;
  description?: string;
  required_documents?: string;
  eligible: boolean;
  matched_rules: string[];
  failed_rules: string[];
}

export interface Application {
  id: number;
  family_id: number;
  scheme_id: number;
  applicant_person_id: number;
  status: string;
  remarks?: string;
  submitted_at: string;
  scheme?: Scheme;
}

export interface ChangeRequest {
  id: number;
  family_id: number;
  person_id?: number;
  field_name: string;
  old_value?: string;
  requested_value: string;
  reason?: string;
  supporting_document?: string;
  verification_status: string;
  verification_source?: string;
  created_at: string;
  reviewed_at?: string;
}

export interface FamilyTransferRequest {
  id: number;
  person_id: number;
  current_family_id: number;
  target_family_id: number;
  reason: string;
  spouse_aadhaar?: string;
  status: string;
  remarks?: string;
  created_at: string;
  completed_at?: string;
}
