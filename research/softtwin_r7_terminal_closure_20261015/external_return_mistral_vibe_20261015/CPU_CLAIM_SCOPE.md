# CPU_CLAIM_SCOPE — G8 Ausserhalb des Scopes

**CLAIM_CEILING:** C1_DESCRIPTIVE_ONLY · **G8-Verdikt:** SCOPE_EXCLUDED_NOT_AUTHORIZED

Es wird kein CPU-, Hostinger- oder sonstiger Performance-Claim erhoben; G8 ist nur fuer einen expliziten Performance-Claim Pflicht. Ein solcher Claim waere erst nach operator-autorisierter Produktionsschaltung mit OS-/Runtime-Identitaet, Lastmodell und kontrollierter Vergleichsmessung moeglich (CLOSE_P1 bleibt NOT_AUTHORIZED).

## DESIGN-Skizze (nicht ausgefuehrt, kein Claim)

- Baseline: die dokumentierten Grenzen von V0.4 (32 MiB Quelle, 128 MiB deklarierte Ausgabe, 512 Eintraege, Ratio 200) sind Deklarations-, keine Zeitgrenzen; 32+128 MiB beweisen keine begrenzte Rechenzeit (Erfordernis fuer ein spaeteres G8: CPU-Timeouts, cgroup/ulimit-Budgets, Messwiederholung).
- Referenzmessung der TS-Referenz-Implementierung ist hier nur ein grober Ordnungsmassstab: 3044 Faelle liefen in einer einzigen Sandbox-Sitzung deterministisch; es wird keine Zeit- oder Kostenmetrik daraus abgeleitet.
