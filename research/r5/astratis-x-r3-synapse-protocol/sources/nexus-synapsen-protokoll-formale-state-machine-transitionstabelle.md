stateDiagram-v2
    direction LR
    
    [*] --> NULL: Initialisierung
    
    %% ---------------------------------------------------------------------
    %% Handshake-Phase
    %% ---------------------------------------------------------------------
    NULL --> NEGOTIATING: Handshake-Request
    note left of NEGOTIATING
        Austausch der Policy-Hashes
        zwischen Sender und Empfänger
    end note
    
    NEGOTIATING --> ACTIVE: Policy-Hashes matchen
    NEGOTIATING --> NULL: Handshake fehlgeschlagen
    note right of ACTIVE
        Volle bidirektionale
        Kommunikation aktiv
    end note
    
    %% ---------------------------------------------------------------------
    %% Fail-Closed Transitions (Policy-Verletzungen)
    %% ---------------------------------------------------------------------
    ACTIVE --> DEGRADED: Layer-3-Verletzung
    note right of DEGRADED
        Policy prüft CLAIM → REJECTED
        Synapse degradiert, aber nicht zerstört
    end note
    
    DEGRADED --> QUARANTINED: 3x Verletzungen
    note left of QUARANTINED
        Nur noch QUERY und RECEIPT
        mit QUARANTINED-Status erlaubt
    end note
    
    %% ---------------------------------------------------------------------
    %% TTL & Lebenszyklus
    %% ---------------------------------------------------------------------
    ACTIVE --> DEPRECATED: TTL abgelaufen
    DEGRADED --> DEPRECATED: TTL abgelaufen
    QUARANTINED --> DEPRECATED: TTL abgelaufen
    
    DEPRECATED --> CONSERVED: WORM-Schreibvorgang
    note right of CONSERVED
        Unveränderlich in WORM gespeichert
        Historische Provenance erhalten
    end note
    
    CONSERVED --> TOMBSTONE: Metadaten löschen
    note left of TOMBSTONE
        Nur Hash existiert noch im Graph
        Vollständige Löschung der Metadaten
    end note
    
    TOMBSTONE --> [*]
    
    %% ---------------------------------------------------------------------
    %% Reset-Mechanismus (kein Auto-Reset!)
    %% ---------------------------------------------------------------------
    DEGRADED --> ACTIVE: Neuer Handshake
    note left of DEGRADED
        Erfordert:
        1. Neuen synapse_id
        2. Aktualisierte Policy-Hashes
        3. Expliziten Handshake
        
        KEIN automatischer Reset!
    end note
    
    %% ---------------------------------------------------------------------
    %% Fail-Closed Mechanismus (Detail)
    %% ---------------------------------------------------------------------
    state "Fail-Closed Detail" as fail_closed {
        [*] --> PolicyCheck
        PolicyCheck --> RejectClaim: Verletzung erkannt
        RejectClaim --> SendReceipt: REJECTED/QUARANTINED
        SendReceipt --> DegradeSynapse
        DegradeSynapse --> WriteAuditLog
        WriteAuditLog --> [*]
    }
    
    note top of fail_closed
        Trigger: Layer-3-Policy-Verletzung
        
        1. CLAIM verwerfen
        2. RECEIPT(REJECTED | QUARANTINED) senden
        3. Synapse-State := DEGRADED | QUARANTINED
        4. Audit-Log schreiben
        5. KEIN automatischer Reset
        
        → Air-Gap-Prinzip im Kleinen
    end note
    
    %% ---------------------------------------------------------------------
    %% Ressourcen-Erschöpfung (Selbstschutz)
    %% ---------------------------------------------------------------------
    ACTIVE --> DEGRADED: Ressourcenknappheit
    note right of ACTIVE
        Empfänger kann Synapse
        proaktiv degradieren
        (kein Fehler, sondern
        lokale Apoptose)
    end note
    
    %% ---------------------------------------------------------------------
    %% Styling
    %% ---------------------------------------------------------------------
    state "ACTIVE" as active <<active>>
    state "DEGRADED" as degraded <<degraded>>
    state "QUARANTINED" as quarantined <<quarantined>>
    state "CONSERVED" as conserved <<conserved>>
    state "TOMBSTONE" as tombstone <<tombstone>>
    
    classDef active fill:#90EE90,stroke:#32CD32
    classDef degraded fill:#FFD700,stroke:#FF8C00
    classDef quarantined fill:#FF6347,stroke:#DC143C
    classDef conserved fill:#ADD8E6,stroke:#1E90FF
    classDef tombstone fill:#D3D3D3,stroke:#808080
    
    class active active
    class degraded degraded
    class quarantined quarantined
    class conserved conserved
    class tombstone tombstone