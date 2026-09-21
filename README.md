# ViridisML

ViridisML is an ongoing work on a framework to detect chlorophyll-a concentrations in satellite ocean-color imagery and visualises the results as time-series maps and animations.

Chlorophyll-a is the primary pigment in phytoplankton and serves as a proxy for ocean productivity and ecosystem health. This project uses NASA MODIS-Aqua satellite data to build a pipeline that ingests, models, and visualises chlorophyll-a concentration over a region of interest.

## Project Status

| Component | Status |
|---|---|
| Data acquisition (NASA OceanData / MODIS-Aqua) |  Implemented |
| Regional extraction & preprocessing (xarray) |  Implemented |
| Visualisation (static frames, MP4/GIF animation, Kepler.gl export) |  Implemented |
| ConvLSTM for chlorophyll detection/prediction | In development |

The current codebase implements the data pipeline and visualisation layer end-to-end. The ML component — training a model to spot/predict chlorophyll-a concentration from satellite bands — is the active area of development; this README describes the intended pipeline and where model training fits in.

## How It Works

```
NASA OceanData (MODIS-Aqua L3) → NetCDF files → xarray preprocessing
        → [ ML model: concentration detection ] → visualisation (frames, animation, Kepler.gl)
```

1. **Download**: Pull MODIS-Aqua Level 3 chlorophyll-a NetCDF granules from NASA OceanData for a date range.
2. **Preprocess**: Open each granule with `xarray`, slice to a geographic region of interest, and align the time series.
3. **Model** *(in development)*: Train/apply an ML model over the satellite bands to identify and quantify chlorophyll-a concentration, producing a per-pixel prediction layer.
4. **Visualise**: Render each time step as a map (Cartopy, `viridis`/`turbo` colormaps), stitch frames into an MP4/GIF animation, and optionally export to Kepler.gl for interactive time-scrubbing.

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
pip install -r requirements.txt
```

Cartopy needs system-level geo libraries:

```bash
# macOS
brew install proj geos

# Ubuntu/Debian
sudo apt-get install libproj-dev proj-data proj-bin libgeos-dev

# Windows (use conda)
conda install -c conda-forge cartopy
```

A NASA Earthdata account is required for most downloads — see `AUTHENTICATION_GUIDE.md`.

## Usage

### 1. Download satellite data

```bash
python down_files.py list aqua_modis_dl.txt   # download from a URL list
python down_files.py sample                    # quick sample (4 files)
python down_files.py custom                    # a fixed date-range pull
```

Downloaded NetCDF granules land in `data/`. See `DOWNLOAD_INSTRUCTIONS.md` and `FIX_DOWNLOAD_ISSUE.md` if downloads return HTML instead of data (usually an auth issue).

### 2. Run the pipeline notebook

```bash
jupyter lab chlorophyll.ipynb
```

The notebook extracts the region of interest, generates per-timestep frames in `frames/`, and compiles them into an animation (`chlorophyll_animation.mp4`, with a matplotlib/GIF fallback).

### 3. Export for interactive visualisation (optional)

The notebook includes a Kepler.gl export step that writes a CSV/GeoJSON (e.g. `kepler_chlorophyll.geojson`) you can drop into [kepler.gl](https://kepler.gl/) for interactive, time-animated maps.

## Configuration

Region and rendering parameters are set in the notebook's configuration cell:

```python
# Region of interest (default: Red Sea)
lat_min, lat_max = 12, 30
lon_min, lon_max = 32, 44

# Rendering
cmap = 'turbo'          # or 'viridis'
vmin, vmax = 0.05, 5.0  # chlorophyll-a range, mg/m^3
dpi = 150
```

## Project Structure

```
ViridisML/
├── chlorophyll.ipynb          # Data extraction, (planned) model application, and visualisation
├── down_files.py               # MODIS-Aqua data downloader
├── check_environment.py        # Diagnoses local Python/package setup
├── aqua_modis_dl.txt            # URL list for batch downloads
├── requirements.txt             # Python dependencies
├── data/                        # Downloaded NetCDF granules (gitignored)
├── frames/                      # Rendered per-timestep PNG frames (gitignored)
├── AUTHENTICATION_GUIDE.md      # Earthdata login setup
├── DOWNLOAD_INSTRUCTIONS.md     # Data download walkthrough
├── FILE_FORMAT_GUIDE.md         # NetCDF variable/format reference
└── FIX_DOWNLOAD_ISSUE.md        # Troubleshooting failed downloads
```

## Data Source

- **NASA OceanData**: https://oceandata.sci.gsfc.nasa.gov/ (MODIS-Aqua, Level 3, `chlor_a`, 8-day composite, 4km)
- **Citation**: NASA Goddard Space Flight Center, Ocean Ecology Laboratory, Ocean Biology Processing Group. Moderate-resolution Imaging Spectroradiometer (MODIS) Aqua Chlorophyll Data; NASA OB.DAAC, Greenbelt, MD, USA.

## Documentation

- `AUTHENTICATION_GUIDE.md` — Earthdata account & credential setup
- `DOWNLOAD_INSTRUCTIONS.md` — step-by-step data acquisition
- `FILE_FORMAT_GUIDE.md` — NetCDF structure and variable reference
- `FIX_DOWNLOAD_ISSUE.md` — troubleshooting HTML-instead-of-NetCDF responses

## License

Project code is provided as-is for research and educational use. MODIS data is provided by NASA and subject to their data use policies.
