# SIFT Experiment Plan

## Dataset
Two images of the same arch (`ref.png` / `mod.png`), taken from slightly different lateral positions, Samsung S25 main camera, 4000×3000px, consistent lighting.
Two images from Sony a6400 at different focal lengths (26mm/50mm both f5.6), 6000×4000px, consistent lighting. Same building facade, the wider one has a lamp post partially occluding the view.
## Experiments
Three runs sharing an identical task suite, varying only the SIFT parameters:

| | Exp 1 — Baseline | Exp 2 — High sensitivity | Exp 3 — Speed-optimised |
|---|---|---|---|
| `nfeatures` | 0 (all) | 5000 | 500 |
| `nOctaveLayers` | 3 | 4 | 2 |
| `contrastThreshold` | 0.04 | 0.02 | 0.06 |
| `edgeThreshold` | 10 | 8 | 15 |
| `lowe_ratio` | 0.75 | 0.80 | 0.70 |

## Tasks (run per experiment)
1. **Two-image matching** — match ref to mod, visualise inlier correspondences
2. **Rotation & scale invariance** — match ref against synthetically warped versions (0°–180°, 0.4×–2.0×), plot inlier count as a degradation curve
3. **Homography estimation** — RANSAC-based homography, verify by projecting ref outline onto mod
4. **SIFT vs ORB comparison** — run ORB at equivalent feature counts alongside each experiment

## Metrics
- Keypoint count, good matches, RANSAC inlier count, inlier ratio, mean reprojection error (px), detection and matching runtime (ms)

## Goal
Understand how relaxing or tightening the contrast threshold and feature budget affects matching quality and geometric accuracy, and where SIFT's performance advantage over ORB diminishes.