# adom-sift

This is a project for conducting experiments with OpenCV SIFT (Scale-Invariant Feature Transform) algorithm.

SIFT paper: [Distinctive Image Features from Scale-Invariant Keypoints](https://link.springer.com/content/pdf/10.1023/B:VISI.0000029664.99615.94.pdf)

## Environment setup

Required Python version: 3.12+

1. Create virtual environment

```bash
python -m venv .venv
```

2. Activate virtual environment

Windows (PowerShell):

```powershell
. .\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## How to run

After installing just open one of the project notebooks and run cells

## Notebooks

* `introduction.ipynb` - basic SIFT workflow: load image, detect keypoints, compute descriptors, and visualize results.
* `experiments.ipynb` - our experiments **TODO**
