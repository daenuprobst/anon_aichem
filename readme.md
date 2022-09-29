# Reproduction steps

- `cd bibliometrics/openalex`
- `python download.py`
- `python process.py biology.pkl biology.csv maps_cache.txt`
- `python process.py chemistry.pkl chemistry.csv maps_cache.txt`
- `mkdir -p papers/biology`
- `mkdir -p papers/chemistry`
- `python pdf_downloader.py biology.csv papers/biology`
- `python pdf_downloader.py chemistry.csv papers/chemistry`
- Run analyses and create figures using notebooks
