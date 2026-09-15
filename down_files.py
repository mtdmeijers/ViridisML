
import requests
from tqdm import tqdm
import os
from datetime import datetime, timedelta

# Configuration
BASE_URL = "https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/"
DATA_DIR = "data"
PRODUCT = "AQUA_MODIS"  # or "TERRA_MODIS"
TEMPORAL_RESOLUTION = "8D"  # 8-day composite, or "MO" for monthly
SPATIAL_RESOLUTION = "4km"  # or "9km"
VARIABLE = "CHL.chlor_a"

def generate_file_url(date_str, end_date_str=None):
    """
    Generate NASA OceanData URL for MODIS chlorophyll-a file.
    
    Args:
        date_str: Start date in YYYYMMDD format
        end_date_str: End date in YYYYMMDD format (for 8D composites)
    
    Returns:
        URL string
    """
    if end_date_str:
        filename = f"{PRODUCT}.{date_str}_{end_date_str}.L3m.{TEMPORAL_RESOLUTION}.{VARIABLE}.{SPATIAL_RESOLUTION}.nc"
    else:
        filename = f"{PRODUCT}.{date_str}.L3m.{TEMPORAL_RESOLUTION}.{VARIABLE}.{SPATIAL_RESOLUTION}.nc"
    
    return BASE_URL + filename, filename

def download_file(url, output_path, auth=None):
    """
    Download a file with progress bar.
    
    Args:
        url: URL to download
        output_path: Local path to save file
        auth: Tuple of (username, password) for authentication (optional)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create session for potential authentication
        session = requests.Session()
        if auth:
            session.auth = auth
        
        response = session.get(url, stream=True, timeout=60)
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '').lower()
            first_chunk = b''
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(output_path, 'wb') as f:
                if total_size > 0:
                    with tqdm(total=total_size, unit='B', unit_scale=True, desc=os.path.basename(output_path)) as pbar:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                if not first_chunk:
                                    first_chunk = chunk[:100]  # Check first 100 bytes
                                f.write(chunk)
                                pbar.update(len(chunk))
                else:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            if not first_chunk:
                                first_chunk = chunk[:100]
                            f.write(chunk)
            
            # Validate file is not HTML error page
            if first_chunk.startswith(b'<') or b'html' in first_chunk.lower() or b'error' in first_chunk.lower():
                os.remove(output_path)  # Delete the HTML file
                print(f"  ⚠️  Got HTML error page instead of NetCDF file")
                return False
            
            # Check file size - NetCDF files should be > 100KB typically
            if os.path.getsize(output_path) < 100000:  # Less than 100KB is suspicious
                os.remove(output_path)
                print(f"  ⚠️  File too small ({os.path.getsize(output_path)} bytes), likely invalid")
                return False
            
            return True
        else:
            print(f"Failed to download {url}, status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        if os.path.exists(output_path):
            os.remove(output_path)
        return False

def download_date_range(start_date, end_date):
    """
    Download files for a date range (8-day composites).
    
    Args:
        start_date: Start date as datetime object
        end_date: End date as datetime object
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    
    current_date = start_date
    downloaded = 0
    failed = 0
    
    while current_date <= end_date:
        # Calculate 8-day period end
        period_end = current_date + timedelta(days=7)
        if period_end > end_date:
            period_end = end_date
        
        date_str = current_date.strftime("%Y%m%d")
        end_date_str = period_end.strftime("%Y%m%d")
        
        url, filename = generate_file_url(date_str, end_date_str)
        output_path = os.path.join(DATA_DIR, filename)
        
        if os.path.exists(output_path):
            print(f"{filename} already exists, skipping...")
            current_date = period_end + timedelta(days=1)
            continue
        
        print(f"\nDownloading: {filename}")
        if download_file(url, output_path):
            downloaded += 1
        else:
            failed += 1
        
        current_date = period_end + timedelta(days=1)
    
    print(f"\nDownload complete: {downloaded} files downloaded, {failed} failed")

def download_sample_files(num_files=4):
    os.makedirs(DATA_DIR, exist_ok=True)
    base_date = datetime(2023, 6, 1)  # June 2023
    downloaded = 0
    failed = 0
    
    print(f"Downloading {num_files} sample files from 2023...")
    print("=" * 60)
    
    for i in range(num_files):
        # Calculate 8-day period starting from base_date
        period_start = base_date + timedelta(days=i*8)
        period_end = period_start + timedelta(days=7)
        
        date_str = period_start.strftime("%Y%m%d")
        end_date_str = period_end.strftime("%Y%m%d")
        
        url, filename = generate_file_url(date_str, end_date_str)
        output_path = os.path.join(DATA_DIR, filename)
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
            print(f"✓ {filename} already exists and is valid")
            downloaded += 1
            continue
        
        print(f"\nDownloading: {filename}")
        if download_file(url, output_path):
            downloaded += 1
        else:
            failed += 1
            # Try alternative: monthly composite if 8-day fails
            if i == 0:  # Only suggest on first failure
                print("  💡 Tip: If downloads fail, the files may not be available yet.")
                print("     Try downloading from: https://oceandata.sci.gsfc.nasa.gov/")
    
    print("=" * 60)
    print(f"Download complete: {downloaded} successful, {failed} failed")
    
    if failed > 0 and downloaded == 0:
        print("\n⚠️  All downloads failed. Possible reasons:")
        print("   1. Files don't exist at those dates")
        print("   2. NASA server is down or slow")
        print("   3. Network connectivity issues")
        print("\n💡 Try manual download from: https://oceandata.sci.gsfc.nasa.gov/")
    
    return downloaded > 0

def download_from_file_list(file_path='aqua_modis_dl.txt'):
    """
    Download files from a text file containing URLs (one per line).
    Supports authentication via environment variables or prompt.
    
    Args:
        file_path: Path to text file with URLs
    
    Returns:
        Number of successfully downloaded files
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return 0
    
    # Read URLs from file
    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if len(urls) == 0:
        print(f"❌ No URLs found in {file_path}")
        return 0
    
    print(f"📋 Found {len(urls)} URLs in {file_path}")
    
    # Check for authentication
    auth = None
    username = os.environ.get('EARTHDATA_USERNAME')
    password = os.environ.get('EARTHDATA_PASSWORD')
    
    if username and password:
        auth = (username, password)
        print(f"🔐 Using authentication from environment variables")
    else:
        print("⚠️  No authentication found in environment variables")
        print("   Set EARTHDATA_USERNAME and EARTHDATA_PASSWORD if downloads fail")
        print("   Or login manually at: https://oceandata.sci.gsfc.nasa.gov/")
    
    print("=" * 60)
    
    downloaded = 0
    failed = 0
    skipped = 0
    
    for i, url in enumerate(urls, 1):
        # Extract filename from URL
        filename = os.path.basename(url)
        output_path = os.path.join(DATA_DIR, filename)
        
        # Check if file already exists and is valid
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            if file_size > 100000:  # Valid NetCDF should be > 100KB
                print(f"[{i}/{len(urls)}] ✓ {filename} already exists ({file_size/1024/1024:.1f} MB)")
                skipped += 1
                downloaded += 1  # Count as success
                continue
            else:
                # Remove invalid file
                os.remove(output_path)
        
        print(f"\n[{i}/{len(urls)}] Downloading: {filename}")
        if download_file(url, output_path, auth=auth):
            file_size = os.path.getsize(output_path)
            print(f"  ✓ Successfully downloaded ({file_size/1024/1024:.1f} MB)")
            downloaded += 1
        else:
            failed += 1
            if not auth and i == 1:
                print("  💡 Tip: If downloads fail, you may need authentication.")
                print("     Set EARTHDATA_USERNAME and EARTHDATA_PASSWORD environment variables")
    
    print("\n" + "=" * 60)
    print(f"Download Summary:")
    print(f"  ✅ Successfully downloaded: {downloaded}")
    print(f"  ⏭️  Already existed (skipped): {skipped}")
    print(f"  ❌ Failed: {failed}")
    print("=" * 60)
    
    return downloaded

if __name__ == "__main__":
    import sys
    
    print("MODIS Chlorophyll-a Data Downloader")
    print("=" * 60)
    print(f"Product: {PRODUCT}")
    print(f"Resolution: {SPATIAL_RESOLUTION}")
    print(f"Temporal: {TEMPORAL_RESOLUTION}")
    print("=" * 60)
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        # Download from file list
        file_path = sys.argv[2] if len(sys.argv) > 2 else 'aqua_modis_dl.txt'
        download_from_file_list(file_path)
    elif len(sys.argv) > 1 and sys.argv[1] == "sample":
        # Quick sample download
        download_sample_files(num_files=4)
    elif len(sys.argv) > 1 and sys.argv[1] == "custom":
        # Custom date range
        start = datetime(2023, 1, 1)
        end = datetime(2023, 3, 31)  # First quarter of 2023
        print(f"Date range: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
        print("=" * 60)
        download_date_range(start, end)
    else:
        # Default: download from file list if it exists, otherwise sample
        if os.path.exists('aqua_modis_dl.txt'):
            print("📋 Found aqua_modis_dl.txt - downloading from file list")
            print("=" * 60)
            download_from_file_list('aqua_modis_dl.txt')
        else:
            print("Usage:")
            print("  python down_files.py list [file.txt]  # Download from URL list file")
            print("  python down_files.py sample           # Download 4 sample files")
            print("  python down_files.py custom           # Download custom date range")
            print("\nRunning sample download...")
            print("=" * 60)
            download_sample_files(num_files=4)
