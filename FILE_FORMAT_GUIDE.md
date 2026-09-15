# File Format Guide

## Required Format: NetCDF (.nc)

Your data files **must** be in NetCDF format with the `.nc` extension.

## File Requirements

### 1. File Type
- **Format**: NetCDF4 or HDF4
- **Extension**: `.nc`
- **Size**: Typically 2-10 MB (must be > 100 KB)
- **Can be opened with**: xarray, netCDF4 library

### 2. Required Structure

#### Variables (at least one):
- ✅ `chlor_a` (preferred - chlorophyll-a concentration)
- ✅ `chlorophyll` (alternative)
- ✅ `CHL` (alternative)
- ✅ `chlor` (alternative)

#### Coordinates (required):
- ✅ `lat` (latitude)
- ✅ `lon` (longitude)
- ✅ `time` (optional, but recommended for date information)

### 3. File Naming (for MODIS data)

**8-day composite:**
```
AQUA_MODIS.YYYYMMDD_YYYYMMDD.L3m.8D.CHL.chlor_a.4km.nc
```

**Example:**
```
AQUA_MODIS.20230601_20230608.L3m.8D.CHL.chlor_a.4km.nc
```

**Monthly composite:**
```
AQUA_MODIS.YYYYMM.L3m.MO.CHL.chlor_a.4km.nc
```

**Example:**
```
AQUA_MODIS.202306.L3m.MO.CHL.chlor_a.4km.nc
```

### 4. File Location

Place all `.nc` files in the `data/` directory:
```
oceanography/
└── data/
    ├── AQUA_MODIS.20230601_20230608.L3m.8D.CHL.chlor_a.4km.nc
    ├── AQUA_MODIS.20230609_20230616.L3m.8D.CHL.chlor_a.4km.nc
    └── ...
```

## How to Check Your Files

### Quick Check:
```bash
# Check file type
file data/*.nc

# Check file size
ls -lh data/*.nc
```

### In Python:
```python
import xarray as xr

# Try to open a file
ds = xr.open_dataset('data/your_file.nc')

# Check structure
print(ds.data_vars)  # Should include 'chlor_a'
print(ds.coords)     # Should include 'lat' and 'lon'
```

## Common Issues

### ❌ HTML Files (Error Pages)
- **Symptom**: Files are 9-11 KB, contain HTML
- **Cause**: Download failed, got error page instead
- **Fix**: Re-download with authentication or use manual download

### ❌ Wrong Format
- **Symptom**: xarray can't open file
- **Cause**: File is not NetCDF (might be CSV, HDF5, etc.)
- **Fix**: Download as NetCDF format

### ❌ Missing Variables
- **Symptom**: "chlor_a not found" error
- **Cause**: File has different variable names
- **Fix**: Code tries alternatives automatically, or rename variable

### ❌ Corrupted Files
- **Symptom**: File opens but data is invalid
- **Cause**: Incomplete download or file corruption
- **Fix**: Re-download the file

## Valid File Examples

✅ **Good:**
- `AQUA_MODIS.20230601_20230608.L3m.8D.CHL.chlor_a.4km.nc` (3.2 MB)
- `AQUA_MODIS.202306.L3m.MO.CHL.chlor_a.4km.nc` (8.5 MB)

❌ **Bad:**
- `data.html` (HTML error page)
- `chlorophyll_data.csv` (CSV format, not NetCDF)
- `AQUA_MODIS.20230601_20230608.L3m.8D.CHL.chlor_a.4km.nc` (9 KB - too small, likely HTML)

## Where to Get Valid Files

1. **NASA OceanData** (requires Earthdata login)
   - https://oceandata.sci.gsfc.nasa.gov/
   - Download as NetCDF

2. **ERDDAP** (no login required)
   - https://coastwatch.pfeg.noaa.gov/erddap/
   - Search "MODIS chlorophyll"
   - Download format: NetCDF

3. **Copernicus Marine Service**
   - https://marine.copernicus.eu/
   - Download as NetCDF

## Testing Your Files

Use the validation cell in the notebook to check if your files are valid:
- Run the "Validate File Format" cell
- It will check file size, structure, and required variables
- Shows detailed information about each file

