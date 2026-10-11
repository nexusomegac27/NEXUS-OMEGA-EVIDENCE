# R27-E · Externer Rückgabe-Slot (NEXUS-owned)

**Die Verzeichnisstruktur wird ausschließlich von NEXUS festgelegt.** Externe Agenten dürfen hier keine Unterordner, Namespaces oder frei erfundenen Dateinamen anlegen.

Maschinell verbindlich: `docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json`. Zulässig sind nur die sieben dort exakt bezeichneten `_R0`-Dateien. Der Slot ist zunächst nicht für fremde GitHub-Identitäten aktiviert (`external_actor_allowlist=[]`). Aktivierung erfordert eine registrierte GitHub-Identität und eine getrennte, tatsächlich geltende Review-/Branchregel. Ein Agent ohne authentifizierte GitHub-Schreibverbindung liefert seine Originaldateien zur quellenexakten AXIOM-Intake-Übertragung; dies wird niemals als agenteneigener SEND-Receipt ausgegeben.

**Create-only**: keine Überschreibung, Rename, Delete, Move, zusätzlichen Verzeichnisse, ZIPs, Binärdateien, Chatlogs, Tokens, Secrets oder personenbezogenen Rohdaten. Ein vollständiger Return umfasst alle sieben erlaubten Dateien in einem PR und ein detached Manifest über die anderen sechs. Der Manifest-SHA wird nachher separat im PR-Empfangskommentar gebunden (kein Selbsthash).

Strukturänderung nötig? `STRUCTURE_CHANGE_REQUEST` über den bestehenden Issue-/PR-Prozess, ohne Strukturmutation durch externe Agenten. `WWW_Extern` erzeugt nur passive, datensparsame Wake-Signale. `Nexus_Intern` verlangt echte, außerhalb des Eventobjekts überprüfte Berechtigung. Drei R27-Auth-Fälle bleiben ein Runtime-HOLD.

`CLAIM_CEILING=C1_DESCRIPTIVE_ONLY` · `RUNTIME=NOT_AUTHORIZED` · `NEW_WORKER=NO`.
