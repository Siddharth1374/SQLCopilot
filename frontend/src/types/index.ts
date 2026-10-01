export interface Column { name: string; type: string; is_primary_key: boolean; references: string | null }
export interface Table { name: string; columns: Column[] }
export interface DatabaseSchema { tables: Table[] }
export interface Check { label: string; ok: boolean }
export interface ValidationResult { valid: boolean; checks: Check[]; errors: string[] }
export interface SafetyReport { safe: boolean; risk_level: string; findings: string[]; requires_confirmation: boolean }
export interface NLToSQLResponse { sql: string; validation: ValidationResult; safety: SafetyReport; explanation: string; optimizations: string[] }
export interface SQLToNLResponse { explanation: string; steps: string[]; optimizations: string[] }
export interface HistoryItem { id: number; name: string; natural_language: string; sql: string; direction: string; saved: boolean; created_at: string }
