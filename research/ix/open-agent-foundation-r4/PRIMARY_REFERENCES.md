# R4 primary reference anchors

These references are starting points for independent validation. They are not truth authorities and
do not select an implementation.

## W3C PROV

- PROV-O: https://www.w3.org/TR/prov-o/
- PROV publications / data model: https://www.w3.org/groups/wg/prov/publications/
- PROV semantics: https://www.w3.org/TR/prov-sem/

R4-B must test whether NEXUS correction, negative-knowledge, hash-custody and authorization semantics
survive an actual round-trip.

~~~text
PROV_COMPATIBLE != LOSSLESS_BY_DEFAULT
~~~

## Strong Kleene K3

R4-A must bind one exact Strong Kleene presentation before comparing it to NEXUS epistemic states.

- Stanford Encyclopedia of Philosophy, negation / K3 discussion:
  https://plato.stanford.edu/archives/spr2016/entries/negation/
- Open Logic Project:
  https://builds.openlogicproject.org/open-logic-complete.pdf

~~~text
BALANCED_TERNARY_NUMERIC_STATE != KLEENE_K3
KLEENE_K3 != NEXUS_EPISTEMIC_STATE_BY_DEFAULT
~~~

## Signed receipt baseline

- RFC 8032 / EdDSA: https://www.rfc-editor.org/info/rfc8032/

## Authorization-boundary references

- Cedar: https://docs.cedarpolicy.com/
- NVIDIA MAIW:
  https://github.com/NVIDIA-AI-Blueprints/Multi-Agent-Intelligent-Warehouse

These references motivate experiments only. They do not make R4 a Cedar, MAIW, PROV or K3
implementation by declaration.
