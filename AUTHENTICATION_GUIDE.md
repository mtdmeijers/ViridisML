# Earthdata Authentication Guide

NASA OceanData requires authentication for downloading MODIS data files. This guide shows you how to set it up.

## Quick Start

### Option 1: Set Environment Variables (Recommended)

**On macOS/Linux:**
```bash
export EARTHDATA_USERNAME="your_username"
export EARTHDATA_PASSWORD="your_password"
python down_files.py list
```

**On Windows (Command Prompt):**
```cmd
set EARTHDATA_USERNAME=your_username
set EARTHDATA_PASSWORD=your_password
python down_files.py list
```

**On Windows (PowerShell):**
```powershell
$env:EARTHDATA_USERNAME="your_username"
$env:EARTHDATA_PASSWORD="your_password"
python down_files.py list
```

### Option 2: Interactive Prompt

Just run the script and it will prompt you:
```bash
python down_files.py list
```

You'll be asked to enter your username and password.

### Option 3: Create a .env file (Advanced)

Create a `.env` file in your project directory:
```
EARTHDATA_USERNAME=your_username
EARTHDATA_PASSWORD=your_password
```

Then load it before running:
```bash
source .env  # Linux/Mac
# or use python-dotenv package
```

## Getting Earthdata Credentials

1. **Create free account**: https://urs.earthdata.nasa.gov/
   - Click "Register"
   - Fill in your information
   - Verify your email
   - Takes about 2 minutes

2. **Login**: Use your username and password

## Security Notes

⚠️ **Important:**
- Never commit credentials to git
- Use environment variables instead of hardcoding
- The `.gitignore` file already excludes `.env` files

## Usage Examples

### Download from file list with authentication:
```bash
# Set credentials
export EARTHDATA_USERNAME="my_username"
export EARTHDATA_PASSWORD="my_password"

# Download all files from list
python down_files.py list aqua_modis_dl.txt
```

### Download without setting variables (will prompt):
```bash
python down_files.py list
# Enter username when prompted
# Enter password when prompted
```

## Troubleshooting

**"Authentication required but not provided"**
- Make sure you've set the environment variables
- Or run interactively to enter credentials

**"401 Unauthorized" or "403 Forbidden"**
- Check your username and password are correct
- Verify your Earthdata account is active
- Some files may require special permissions

**Downloads still failing?**
- Some files may not exist (check dates)
- Server may be slow or down
- Try downloading a few files manually first to test

## Alternative: Manual Download

If automated download continues to fail:
1. Login to: https://oceandata.sci.gsfc.nasa.gov/
2. Navigate to your files
3. Download manually
4. Place in `data/` directory

