# R20 scientific primary source register — reviewed 2026-11-09

| Source | Current evidence | Limit for OPPO male reference |
| --- | --- | --- |
| https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html | Official BP3D database CC BY 4.0 updated 2025-02-27 | Original release and R18 derivative license chain remain per-file OPEN |
| https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/README_e.html | Official updated license text and release history | Historical CC BY-SA 2.1 Japan citations cannot be erased |
| https://github.com/Z-Anatomy/Models-of-human-anatomy | Z-Anatomy derivative, CC BY-SA 4.0; own attribution cites historical BP3D 2.1 JP | Additional components may be NC/restricted; exclude until verified |
| https://humanatlas.io/3d-reference-library | Official HRA male/female organ atlas with ontology mapping | Overlay geometry not automatically registered to BP3D |
| https://www.nlm.nih.gov/research/visible/visible_human.html | Actual CT, MRI and cryosection data from one male/one female donor, male 1871 and female 5189 sections | Donor-specific data, not universal optimal human or ready mesh rig |
| https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53089158 | OpenSim marker-distance-based model scaling | Requires measured landmarks to describe individual body geometry |
| https://github.com/dlaidig/vqf | VQF C++/Python/MATLAB MIT 6D and 9D inertial orientation filter | Not tested on OPPO and not multi-segment human-pose observability |
| https://www.sciencedirect.com/science/article/pii/S156625352200183X | Laidig/Seel, Information Fusion 2023, DOI 10.1016/j.inffus.2022.10.014 | Independent dataset benchmark, no current Nexus accuracy claim |
| https://github.com/CognitionLabSNUC/open-anatomy-atlas | Open-source atlas implementation and reports of more detailed BodyParts3D sources | Secondary candidate; model license / source release / real GPU must be confirmed |
| https://www.nature.com/articles/s41592-024-02563-5 | 2025 multi-scale HuBMAP HRA scientific methods | Reference topology/ontology, not measurement of OPPO user |

Required atomized provenance: exact dataset version, byte hash, acquisition source, donor/reference, coordinate frame, millimetre/metre conversion, right/left, FMA/UBERON labels, method, transformation provenance, license terms, independent evidence and clinical nonvalidation warning. Do not import unlicensed mesh/weights.
