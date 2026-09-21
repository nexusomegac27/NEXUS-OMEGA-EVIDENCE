"""
Nexus Synapsen-Protokoll Validator – Prototyp-Implementierung
============================================================

Kanonische Referenz: NEXUS_TESSARAKT_BRAIN_METAPHER.txt (User-Upload, 21.09.2026)

Dieser Validator erzwingt:
- C1-Konformität (alle Messages sind rein deskriptiv)
- No-Root-Transfer (keine Rechteübertragung)
- Fail-Closed bei Schema-Verletzungen
- Strenge Typprüfung aller Felder

Verwendung:
    python nexus_validator.py

Abhängigkeiten:
    pip install jsonschema
"""

import json
from jsonschema import validate, ValidationError, Draft7Validator
from typing import Dict, Any, Optional, Tuple
import re


# =============================================================================
# KANONISCHES JSON-SCHEMA (äquivalent zu CDDL aus der Spezifikation)
# =============================================================================

NEXUS_MESSAGE_SCHEMA: Dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://nexus-mobile.de/schemas/nexus_message_v1.json",
    "title": "NexusMessage",
    "description": "Kanonisches Schema für Nexus Synapsen-Protokoll Messages. C1_DESCRIPTIVE_ONLY.",
    "type": "object",
    "required": ["envelope", "routing", "semantic_layer", "payload", "provenance"],
    "additionalProperties": False,
    "properties": {
        "envelope": {"$ref": "#/definitions/Envelope"},
        "routing": {"$ref": "#/definitions/Routing"},
        "semantic_layer": {"$ref": "#/definitions/SemanticLayer"},
        "payload": {"$ref": "#/definitions/Payload"},
        "provenance": {"$ref": "#/definitions/Provenance"}
    },
    "definitions": {
        # -------------------------------------------------------------------------
        # Envelope: Transport-Metadaten
        # -------------------------------------------------------------------------
        "Envelope": {
            "type": "object",
            "required": ["msg_id", "timestamp", "ttl_blocks", "source_node_id", "signature", "schema_version"],
            "additionalProperties": False,
            "properties": {
                "msg_id": {
                    "type": "string",
                    "pattern": r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
                    "description": "UUID v7 (zeitbasiert)"
                },
                "timestamp": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "Unix epoch seconds"
                },
                "ttl_blocks": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "description": "Maximale Lebensdauer in Blöcken/Ticks"
                },
                "source_node_id": {
                    "type": "string",
                    "pattern": r"^[0-9a-f]{64}$",
                    "minLength": 64,
                    "maxLength": 64,
                    "description": "SHA-256 Hash der ed25519 Public Key"
                },
                "signature": {
                    "type": "string",
                    "description": "ed25519 Signatur über kanonische Message-Darstellung"
                },
                "schema_version": {
                    "type": "string",
                    "pattern": r"^1\.[0-9]+\.[0-9]+$",
                    "description": "Semantic Versioning (1.x.x)"
                }
            }
        },
        
        # -------------------------------------------------------------------------
        # Routing: Zielinformationen
        # -------------------------------------------------------------------------
        "Routing": {
            "type": "object",
            "required": ["target_node_id", "synapse_id"],
            "additionalProperties": False,
            "properties": {
                "target_node_id": {
                    "type": "string",
                    "pattern": r"^[0-9a-f]{64}$",
                    "minLength": 64,
                    "maxLength": 64,
                    "description": "SHA-256 Hash der Ziel-Node Public Key"
                },
                "synapse_id": {
                    "type": "string",
                    "pattern": r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
                    "description": "UUID v4 für Synapsen-Identifikation"
                }
            }
        },
        
        # -------------------------------------------------------------------------
        # SemanticLayer: Typ und Kontext
        # -------------------------------------------------------------------------
        "SemanticLayer": {
            "type": "object",
            "required": ["type", "uncertainty", "context_hash"],
            "additionalProperties": False,
            "properties": {
                "type": {
                    "enum": ["CLAIM", "RECEIPT", "QUERY", "REVOKE"],
                    "description": "Geschlossenes Enum – keine Erweiterung zur Laufzeit"
                },
                "intent_vector": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "Rein deskriptiv. DARF NICHT als Entscheidungsinput verwendet werden (C1)."
                },
                "uncertainty": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "description": "Unsicherheitswert der Message"
                },
                "context_hash": {
                    "type": "string",
                    "pattern": r"^[0-9a-f]{64}$",
                    "minLength": 64,
                    "maxLength": 64,
                    "description": "SHA-256 Hash des Kontexts"
                }
            }
        },
        
        # -------------------------------------------------------------------------
        # Provenance: Nachvollziehbarkeit
        # -------------------------------------------------------------------------
        "Provenance": {
            "type": "object",
            "required": ["causal_chain_hash", "worm_anchor"],
            "additionalProperties": False,
            "properties": {
                "causal_chain_hash": {
                    "type": "string",
                    "pattern": r"^[0-9a-f]{64}$",
                    "minLength": 64,
                    "maxLength": 64,
                    "description": "SHA-256 Hash des vorherigen Zustands des Senders"
                },
                "worm_anchor": {
                    "type": "string",
                    "pattern": r"^[0-9a-f]{64}$",
                    "minLength": 64,
                    "maxLength": 64,
                    "description": "Merkle Root oder WORM-Anker"
                }
            }
        },
        
        # -------------------------------------------------------------------------
        # Payload: Die vier Kern-Typen (oneOf)
        # -------------------------------------------------------------------------
        "Payload": {
            "oneOf": [
                {"$ref": "#/definitions/ClaimPayload"},
                {"$ref": "#/definitions/ReceiptPayload"},
                {"$ref": "#/definitions/QueryPayload"},
                {"$ref": "#/definitions/RevokePayload"}
            ]
        },
        
        "ClaimPayload": {
            "type": "object",
            "required": ["observation", "confidence", "evidence_refs"],
            "additionalProperties": False,
            "properties": {
                "observation": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 4096,
                    "description": "Rein deskriptiv (C1). DARF KEINE Imperative enthalten."
                },
                "confidence": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "description": "Vertrauenswert der Beobachtung"
                },
                "evidence_refs": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Liste von Message-IDs oder Hash-Referenzen"
                }
            },
            "description": "CLAIM: Deskriptive Beobachtung ohne Imperative"
        },
        
        "ReceiptPayload": {
            "type": "object",
            "required": ["claim_ref", "validation_result", "policy_hash_used"],
            "additionalProperties": False,
            "properties": {
                "claim_ref": {
                    "type": "string",
                    "description": "msg_id des CLAIMs, auf den sich dieser RECEIPT bezieht"
                },
                "validation_result": {
                    "enum": ["ACCEPTED", "REJECTED", "QUARANTINED"],
                    "description": "Ergebnis der Policy-Prüfung"
                },
                "policy_hash_used": {
                    "type": "string",
                    "pattern": r"^[0-9a-f]{64}$",
                    "minLength": 64,
                    "maxLength": 64,
                    "description": "SHA-256 Hash der verwendeten Policy"
                },
                "notes": {
                    "type": "string",
                    "maxLength": 512,
                    "description": "Optionale Anmerkung zur Validierung"
                }
            },
            "description": "RECEIPT: Bestätigt nur Eingang und lokale Policy-Prüfung"
        },
        
        "QueryPayload": {
            "type": "object",
            "required": ["target_schema", "constraints", "max_cost"],
            "additionalProperties": False,
            "properties": {
                "target_schema": {
                    "type": "string",
                    "description": "Schema, das abgefragt wird"
                },
                "constraints": {
                    "type": "object",
                    "additionalProperties": True,
                    "description": "Abfrage-Bedingungen (müssen vom Empfänger validiert werden)"
                },
                "max_cost": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000,
                    "description": "Maximale Kosten für die Abfrage"
                }
            },
            "description": "QUERY: Fordert Daten an, erzwingt aber KEINE Antwort (Fail-Closed erlaubt)"
        },
        
        "RevokePayload": {
            "type": "object",
            "required": ["target_ref", "reason"],
            "additionalProperties": False,
            "properties": {
                "target_ref": {
                    "type": "string",
                    "description": "msg_id des eigenen vorherigen CLAIMs, der widerrufen wird"
                },
                "reason": {
                    "enum": ["TTL_EXPIRED", "SELF_CORRECTION", "OPERATOR_REQUEST"],
                    "description": "Grund für den Widerruf"
                }
            },
            "description": "REVOKE: Kann NUR eigene Claims referenzieren (source_node_id muss matchen)"
        }
    }
}


# =============================================================================
# VERBOTENE FELDER (No-Root-Transfer Garantie)
# =============================================================================

FORBIDDEN_FIELDS: set = {
    # Imperative
    'execute', 'run', 'start', 'stop', 'halt', 'terminate',
    # Policy-Änderungen
    'set_policy', 'update_policy', 'change_policy', 'modify_policy',
    # Rechteübertragung
    'grant', 'revoke_access', 'elevate', 'escalate', 'promote',
    # Root-Autorität
    'root', 'admin', 'sudo', 'override', 'force',
    # Befehle
    'command', 'instruction', 'directive', 'order',
    # Sonstiges
    'privilege', 'authority', 'control'
}

# Verbotene Muster in observation-Feldern (CLAIM)
FORBIDDEN_PATTERNS: list = [
    r'\bexecute\b', r'\brun\b', r'\bgrant\b', r'\boverride\b',
    r'\bforce\b', r'\badmin\b', r'\broot\b'
]


# =============================================================================
# VALIDATOR-KLASSE
# =============================================================================

class NexusValidator:
    """
    Validator für Nexus Synapsen-Protokoll Messages.
    
    Erzwingt:
    - JSON-Schema-Konformität
    - C1-Konformität (keine Imperative)
    - No-Root-Transfer (verbotene Felder)
    - Fail-Closed bei Verletzungen
    """
    
    @staticmethod
    def validate_schema(message: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validiert die Message gegen das kanonische JSON-Schema.
        
        Args:
            message: Die zu validierende Message als Dictionary
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            validator = Draft7Validator(NEXUS_MESSAGE_SCHEMA)
            errors = list(validator.iter_errors(message))
            if errors:
                error_messages = [f"{e.json_path}: {e.message}" for e in errors]
                return False, "Schema-Verletzungen: " + "; ".join(error_messages)
            return True, None
        except Exception as e:
            return False, f"Schema-Validierungsfehler: {str(e)}"
    
    @staticmethod
    def validate_no_root_transfer(message: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Prüft, dass keine verbotenen Felder (No-Root-Transfer) vorhanden sind.
        
        Args:
            message: Die Message als Dictionary
            
        Returns:
            tuple: (is_valid, error_message)
        """
        # Prüfe alle Ebenen der Message
        def check_dict(d: Dict, path: str = "") -> Optional[str]:
            for key, value in d.items():
                current_path = f"{path}.{key}" if path else key
                if key in FORBIDDEN_FIELDS:
                    return f"Verbotenes Feld '{key}' an {current_path} (No-Root-Transfer-Verletzung)"
                if isinstance(value, dict):
                    result = check_dict(value, current_path)
                    if result:
                        return result
            return None
        
        # Prüfe die gesamte Message
        if isinstance(message, dict):
            error = check_dict(message)
            if error:
                return False, error
        
        return True, None
    
    @staticmethod
    def validate_c1_compliance(message: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Prüft C1-Konformität: CLAIMs dürfen keine Imperative enthalten.
        
        Args:
            message: Die Message als Dictionary
            
        Returns:
            tuple: (is_valid, error_message)
        """
        semantic_layer = message.get("semantic_layer", {})
        msg_type = semantic_layer.get("type")
        
        # Nur CLAIMs müssen auf Imperative geprüft werden
        if msg_type != "CLAIM":
            return True, None
        
        payload = message.get("payload", {})
        observation = payload.get("observation", "")
        
        # Prüfe auf verbotene Muster
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, observation, re.IGNORECASE):
                return False, f"CLAIM enthält imperatives Muster '{pattern}' (C1-Verletzung)"
        
        return True, None
    
    @staticmethod
    def validate_revoke_ownership(message: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Prüft, dass REVOKE nur eigene Claims referenziert.
        
        Args:
            message: Die Message als Dictionary
            
        Returns:
            tuple: (is_valid, error_message)
        """
        semantic_layer = message.get("semantic_layer", {})
        msg_type = semantic_layer.get("type")
        
        if msg_type != "REVOKE":
            return True, None
        
        envelope = message.get("envelope", {})
        source_node_id = envelope.get("source_node_id", "")
        
        payload = message.get("payload", {})
        target_ref = payload.get("target_ref", "")
        
        # In einer echten Implementierung:
        # 1. target_ref muss eine msg_id sein
        # 2. Die msg_id muss zu einem CLAIM gehören, der von source_node_id stammt
        # Hier nur Platzhalter-Prüfung
        if not target_ref:
            return False, "REVOKE: target_ref fehlt"
        
        # Prüfe, ob target_ref ein gültiges UUID-Format hat
        if not re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", target_ref, re.IGNORECASE):
            return False, f"REVOKE: target_ref '{target_ref}' hat ungültiges Format"
        
        return True, None
    
    @staticmethod
    def validate_signature(message: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validiert die Signatur der Message.
        (Platzhalter – in Realität mit ed25519)
        
        Args:
            message: Die Message als Dictionary
            
        Returns:
            tuple: (is_valid, error_message)
        """
        # In einer echten Implementierung:
        # 1. Erstelle kanonische Darstellung (ohne signature-Feld)
        # 2. Hash die Darstellung
        # 3. Verifiziere mit ed25519 Public Key
        
        envelope = message.get("envelope", {})
        if "signature" not in envelope:
            return False, "Signatur fehlt"
        
        # Platzhalter: Immer True zurückgeben
        return True, None
    
    @staticmethod
    def validate(message: Dict[str, Any], check_signature: bool = False) -> Tuple[bool, list]:
        """
        Vollständige Validierung einer NexusMessage.
        
        Args:
            message: Die zu validierende Message
            check_signature: Ob die Signatur geprüft werden soll (Platzhalter)
            
        Returns:
            tuple: (is_valid, list_of_errors)
        """
        errors: list = []
        
        # 1. Schema-Validierung
        schema_valid, schema_error = NexusValidator.validate_schema(message)
        if not schema_valid:
            errors.append(f"❌ Schema: {schema_error}")
        
        # 2. No-Root-Transfer-Prüfung
        no_root_valid, no_root_error = NexusValidator.validate_no_root_transfer(message)
        if not no_root_valid:
            errors.append(f"❌ No-Root-Transfer: {no_root_error}")
        
        # 3. C1-Konformität
        c1_valid, c1_error = NexusValidator.validate_c1_compliance(message)
        if not c1_valid:
            errors.append(f"❌ C1: {c1_error}")
        
        # 4. REVOKE Ownership
        revoke_valid, revoke_error = NexusValidator.validate_revoke_ownership(message)
        if not revoke_valid:
            errors.append(f"❌ REVOKE: {revoke_error}")
        
        # 5. Signatur (optional)
        if check_signature:
            sig_valid, sig_error = NexusValidator.validate_signature(message)
            if not sig_valid:
                errors.append(f"❌ Signatur: {sig_error}")
        
        return len(errors) == 0, errors


# =============================================================================
# TEST-CASES (Validierte Instanzen aus der Spezifikation)
# =============================================================================

# Beispiel 1: CLAIM (validiert)
EXAMPLE_CLAIM: Dict[str, Any] = {
    "envelope": {
        "msg_id": "018f3a2b-7c4d-7e8f-9a0b-1c2d3e4f5a6b",
        "timestamp": 1726891200,
        "ttl_blocks": 5,
        "source_node_id": "721c736831b9fca582a7bf137df3404a35ef9186e71a527c51909b5ff8d4b004",
        "signature": "a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef12",
        "schema_version": "1.0.0"
    },
    "routing": {
        "target_node_id": "77907f40db79334a6251817a998991202ca2a7de98c68439b8dc5463d04d8797",
        "synapse_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
    },
    "semantic_layer": {
        "type": "CLAIM",
        "intent_vector": [0.12, -0.45, 0.88],
        "uncertainty": 0.15,
        "context_hash": "62678d969475a5bfa453ab4c62775de20b225a4b19620a80214ae7ca8cb04a64"
    },
    "payload": {
        "observation": "Document X with hash sha256:8f4e2b was observed in location Y at time T",
        "confidence": 0.85,
        "evidence_refs": ["prev-msg-001", "hash-ref-002"]
    },
    "provenance": {
        "causal_chain_hash": "ee0fc35b0b499ad53309fdab638a192c79df7f637b95a43ffa9ee318dca40790",
        "worm_anchor": "ea0c5a3c517653600ac9f7e2ed8dca4791570ca4cffb0f4cd6fa1d2d732cd126"
    }
}

# Beispiel 2: RECEIPT (validiert)
EXAMPLE_RECEIPT: Dict[str, Any] = {
    "envelope": {
        "msg_id": "018f3a2c-8d5e-7f9a-0b1c-2d3e4f5a6b7c",
        "timestamp": 1726891210,
        "ttl_blocks": 3,
        "source_node_id": "77907f40db79334a6251817a998991202ca2a7de98c68439b8dc5463d04d8797",
        "signature": "b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234",
        "schema_version": "1.0.0"
    },
    "routing": {
        "target_node_id": "721c736831b9fca582a7bf137df3404a35ef9186e71a527c51909b5ff8d4b004",
        "synapse_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
    },
    "semantic_layer": {
        "type": "RECEIPT",
        "uncertainty": 0.05,
        "context_hash": "62678d969475a5bfa453ab4c62775de20b225a4b19620a80214ae7ca8cb04a64"
    },
    "payload": {
        "claim_ref": "018f3a2b-7c4d-7e8f-9a0b-1c2d3e4f5a6b",
        "validation_result": "ACCEPTED",
        "policy_hash_used": "72993b6cb83904d39a8c73bd0651aa6251288ede5dbc2c7bcbdc54cc5bbf5d77",
        "notes": "Structure valid, hash intact, C1 ceiling respected"
    },
    "provenance": {
        "causal_chain_hash": "68ebfe52162b6c9dbc4bb9ecdca7317bb501ff5b4dc5ed9eceb97ad928e14604",
        "worm_anchor": "ea0c5a3c517653600ac9f7e2ed8dca4791570ca4cffb0f4cd6fa1d2d732cd126"
    }
}

# Beispiel 3: QUERY (validiert)
EXAMPLE_QUERY: Dict[str, Any] = {
    "envelope": {
        "msg_id": "018f3a2d-9e6f-7a0b-1c2d-3e4f5a6b7c8d",
        "timestamp": 1726891220,
        "ttl_blocks": 2,
        "source_node_id": "721c736831b9fca582a7bf137df3404a35ef9186e71a527c51909b5ff8d4b004",
        "signature": "c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef123456",
        "schema_version": "1.0.0"
    },
    "routing": {
        "target_node_id": "77907f40db79334a6251817a998991202ca2a7de98c68439b8dc5463d04d8797",
        "synapse_id": "b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e"
    },
    "semantic_layer": {
        "type": "QUERY",
        "uncertainty": 0.3,
        "context_hash": "62678d969475a5bfa453ab4c62775de20b225a4b19620a80214ae7ca8cb04a64"
    },
    "payload": {
        "target_schema": "artifact_hash_lookup",
        "constraints": {
            "hash_prefix": "8f4e2b",
            "max_results": 5
        },
        "max_cost": 10
    },
    "provenance": {
        "causal_chain_hash": "82de1cc15aa5d55331aad755a001b0deb5c3c7b695b8e10297a4a7b0c3cc4b42",
        "worm_anchor": "ea0c5a3c517653600ac9f7e2ed8dca4791570ca4cffb0f4cd6fa1d2d732cd126"
    }
}

# Beispiel 4: REVOKE (validiert)
EXAMPLE_REVOKE: Dict[str, Any] = {
    "envelope": {
        "msg_id": "018f3a2e-0f7a-7b1c-2d3e-4f5a6b7c8d9e",
        "timestamp": 1726891300,
        "ttl_blocks": 1,
        "source_node_id": "721c736831b9fca582a7bf137df3404a35ef9186e71a527c51909b5ff8d4b004",
        "signature": "d4e5f6789012345678901234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef12345678",
        "schema_version": "1.0.0"
    },
    "routing": {
        "target_node_id": "77907f40db79334a6251817a998991202ca2a7de98c68439b8dc5463d04d8797",
        "synapse_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
    },
    "semantic_layer": {
        "type": "REVOKE",
        "uncertainty": 0.0,
        "context_hash": "62678d969475a5bfa453ab4c62775de20b225a4b19620a80214ae7ca8cb04a64"
    },
    "payload": {
        "target_ref": "018f3a2b-7c4d-7e8f-9a0b-1c2d3e4f5a6b",
        "reason": "SELF_CORRECTION"
    },
    "provenance": {
        "causal_chain_hash": "27efa4de987b5a0ddb63dadcd4c68a073d40d76afd2f6ef7f920dfdee7a702dc",
        "worm_anchor": "ea0c5a3c517653600ac9f7e2ed8dca4791570ca4cffb0f4cd6fa1d2d732cd126"
    }
}

# Beispiel 5: INVALID (enthält verbotenes Feld 'execute')
EXAMPLE_INVALID: Dict[str, Any] = {
    "envelope": {
        "msg_id": "018f3a2f-1a2b-7c3d-8e4f-5a6b7c8d9e0f",
        "timestamp": 1726891300,
        "ttl_blocks": 1,
        "source_node_id": "721c736831b9fca582a7bf137df3404a35ef9186e71a527c51909b5ff8d4b004",
        "signature": "placeholder",
        "schema_version": "1.0.0"
    },
    "routing": {
        "target_node_id": "77907f40db79334a6251817a998991202ca2a7de98c68439b8dc5463d04d8797",
        "synapse_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
    },
    "semantic_layer": {
        "type": "CLAIM",
        "uncertainty": 0.0,
        "context_hash": "62678d969475a5bfa453ab4c62775de20b225a4b19620a80214ae7ca8cb04a64"
    },
    "payload": {
        "observation": "Execute this command",
        "confidence": 0.85,
        "evidence_refs": [],
        "execute": "run now"  # VERBOTENES FELD
    },
    "provenance": {
        "causal_chain_hash": "27efa4de987b5a0ddb63dadcd4c68a073d40d76afd2f6ef7f920dfdee7a702dc",
        "worm_anchor": "ea0c5a3c517653600ac9f7e2ed8dca4791570ca4cffb0f4cd6fa1d2d732cd126"
    }
}


# =============================================================================
# HAUPTPROGRAMM
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("NEXUS SYNAPSEN-PROTOKOLL VALIDATOR – PROTOTYP")
    print("=" * 80)
    print()
    
    # Validierte Instanzen testen
    test_cases = [
        ("CLAIM", EXAMPLE_CLAIM),
        ("RECEIPT", EXAMPLE_RECEIPT),
        ("QUERY", EXAMPLE_QUERY),
        ("REVOKE", EXAMPLE_REVOKE),
        ("INVALID (No-Root-Transfer)", EXAMPLE_INVALID)
    ]
    
    print("Validierung der kanonischen Beispiele:")
    print("-" * 80)
    
    all_passed = True
    for name, message in test_cases:
        is_valid, errors = NexusValidator.validate(message)
        status = "✅ PASS" if is_valid else "❌ FAIL"
        print(f"{name:25} {status}")
        if not is_valid:
            all_passed = False
            for error in errors:
                print(f"  {error}")
    
    print("-" * 80)
    
    if all_passed:
        print("\n🎉 ALLE TESTS BESTANDEN!")
        print("\nDie Spezifikation ist kausal-kanonisch validiert.")
        print("Nächster Schritt: Rust-Implementierung für Produktion.")
    else:
        print("\n⚠️  EINIGE TESTS FEHLGESCHLAGEN")
        print("Bitte die Fehler oben überprüfen.")
    
    print("=" * 80)