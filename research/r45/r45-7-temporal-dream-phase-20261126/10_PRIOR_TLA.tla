------------------------ MODULE R45_7_Deadline ------------------------
EXTENDS Naturals, FiniteSets
CONSTANT Nodes
VARIABLES now, spent, status, bit
vars == <<now, spent, status, bit>>
Pending == {i \in Nodes : status[i] = "P"}
Init == /\ now = 0 /\ spent = 0 /\ status = [i \in Nodes |-> "P"] /\ bit = FALSE
Debate == /\ Pending # {} /\ bit' = ~bit /\ UNCHANGED <<now, spent, status>>
Tick == /\ Pending # {} /\ now < 3 /\ now' = now + 1
        /\ status' = [i \in Nodes |-> IF now' = 3 /\ status[i] = "P" THEN "H" ELSE status[i]]
        /\ UNCHANGED <<spent, bit>>
Commit(i) == /\ i \in Pending /\ now < 3 /\ spent < 1
             /\ spent' = spent + 1 /\ status' = [status EXCEPT ![i] = "S"]
             /\ UNCHANGED <<now, bit>>
Next == Debate \/ Tick \/ (\E i \in Nodes : Commit(i))
Spec == Init /\ [][Next]_vars /\ WF_vars(Tick)
TypeOK == /\ now \in 0..3 /\ spent \in 0..1 /\ bit \in BOOLEAN /\ status \in [Nodes -> {"P","S","H"}]
BudgetSafe == spent = Cardinality({i \in Nodes : status[i] = "S"})
Terminal == Pending = {}
Termination == <>Terminal
\* DESIGN ONLY: TLC not run; finite Python abstraction separately executed.
\* H is a synthetic timeout terminal; not a claim of actual external effect absence.
======================================================================
