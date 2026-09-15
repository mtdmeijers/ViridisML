# Quick Start: Downloading Data

## The Problem
You're seeing "No data files found" because the `data/` directory is empty.

## Quick Solution (Easiest)

### Option 1: Download from Notebook (Recommended)
1. Open `chlorophyll.ipynb`
2. Find the cell labeled "Option A: Quick Download"
3. Uncomment the last line: `download_sample_files(num_files=4)`
4. Run that cell
5. Wait for downloads to complete (a few minutes)
6. Re-run the file listing cell to see your data

### Option 2: Download from Terminal
```bash
cd /Users/macpro/Desktop/oceanography
python down_files.py sample
```

This will download 4 sample files from recent dates.

### Option 3: Manual Download
1. Visit: https://oceandata.sci.gsfc.nasa.gov/
2. Click: **MODIS-Aqua** → **Level 3** → **Chlorophyll-a**
3. Select:
   - **Temporal**: 8-day composite
   - **Spatial**: 4km
   - **Date**: Pick a few recent dates (e.g., last 2-3 months)
4. Download files and save them to the `data/` folder

**File naming example:**
`AQUA_MODIS.20240101_20240108.L3m.8D.CHL.chlor_a.4km.nc`

## After Downloading

Once you have files in the `data/` directory:
1. Re-run the file listing cell in the notebook
2. You should see: "✅ Found X NetCDF files"
3. Continue with the visualization cells

## Troubleshooting

**Downloads failing?**
- Check internet connection
- NASA servers might be slow - try again later
- Some dates might not have data available

**Still no files?**
- Make sure files are in `data/` folder (not `data/data/`)
- Check file extensions are `.nc`
- Verify files aren't corrupted (try opening one with xarray)

## Need More Data?

To download a full year or specific date range, edit `down_files.py`:
```python
start = datetime(2023, 1, 1)
end = datetime(2023, 12, 31)
download_date_range(start, end)
```

Then run: `python down_files.py custom`

