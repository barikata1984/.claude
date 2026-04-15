# Robotics Venue Reference

Use this file when the survey topic falls in robotics, robot learning, manipulation,
or closely adjacent fields (e.g., computer vision for robotics, sim-to-real transfer,
physical property estimation, human-robot interaction).

---

## Tier 1 — Primary venues (exhaustive coverage required)

### Journals
| Venue | Full name | Publisher | Notes |
|-------|-----------|-----------|-------|
| RA-L | IEEE Robotics and Automation Letters | IEEE | Target journal for this workflow. Check every volume since 2022. |
| IJRR | International Journal of Robotics Research | SAGE | Highest-impact robotics journal. |
| Science Robotics | Science Robotics | AAAS | High-profile, selective. |
| T-RO | IEEE Transactions on Robotics | IEEE | Long-form methods papers. |

### Conferences
| Venue | Full name | Notes |
|-------|-----------|-------|
| CoRL | Conference on Robot Learning | Primary venue for robot learning. Check 2022–present. |
| ICRA | IEEE International Conference on Robotics and Automation | Largest robotics conference. High volume — filter by relevance. |
| IROS | IEEE/RSJ International Conference on Intelligent Robots and Systems | Second-largest. Similar scope to ICRA. |
| RSS | Robotics: Science and Systems | Small, highly selective. Strong on manipulation and learning. |

---

## Tier 2 — Secondary venues (high-impact papers only)

### ML/AI conferences with strong robotics tracks
| Venue | Notes |
|-------|-------|
| NeurIPS | Robot learning, sim-to-real, physical reasoning papers appear regularly. |
| ICML | Learning-based control, reinforcement learning. |
| ICLR | Representation learning for robotics. |
| CoRL Workshop | Co-located workshops often contain early-stage relevant work. |

### Computer vision conferences (when perception is central)
| Venue | Notes |
|-------|-------|
| CVPR | 3D understanding, pose estimation, object detection. |
| ICCV | Similar scope to CVPR. Biennial. |
| ECCV | European counterpart to CVPR/ICCV. |

---

## Tier 3 — Foundational venues (seminal works only)

ICRA/IROS/IJRR proceedings from before 2016, plus any classic manipulation or
control papers regardless of venue (e.g., early work on grasp planning, impedance
control, visual servoing).

---

## Search strategy notes

**For RA-L specifically**: RA-L papers are often presented at ICRA or IROS.
A paper may appear in the RA-L journal volume but be listed in proceedings as
"RA-L + ICRA 2024" — treat these as a single publication and use the RA-L DOI.

**OpenAlex / Semantic Scholar filters**:
```bash
# Filter by venue in search scripts
python scripts/search_semantic_scholar.py --query "TOPIC" --venue "IEEE Robotics and Automation Letters" --year-from 2022
python scripts/search_openalex.py --query "TOPIC" --venue "CoRL" --year-from 2022
```

**Venue-specific arXiv search**:
```
# CoRL proceedings are on OpenReview; also appear on arXiv
https://openreview.net/group?id=robot-learning.org/CoRL/2024/Conference

# ICRA / IROS / RSS papers often appear on arXiv before publication
site:arxiv.org "ICRA 2024" TOPIC
site:arxiv.org "CoRL 2024" TOPIC
```

**Publisher DOI resolution**:
- RA-L DOIs follow the pattern: `10.1109/LRA.YYYY.XXXXXXX`
- ICRA DOIs follow the pattern: `10.1109/ICRA.YYYY.XXXXXXX`
- RSS papers: use the RSS proceedings DOI from `roboticsproceedings.org`
- CoRL papers: use the OpenReview URL if no publisher DOI is available
