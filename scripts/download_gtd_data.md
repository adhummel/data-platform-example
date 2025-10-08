# GTD Data Acquisition Guide

## Step 1: Request Access

1. Visit the GTD website: https://www.start.umd.edu/gtd/contact/
2. Fill out the data request form with:
   - Your name and email
   - Institution (can be "Independent Researcher")
   - Purpose: "Academic research and data platform development"
3. Agree to terms of use (non-commercial research)

## Step 2: Download Data

1. You'll receive download link via email (usually within 24 hours)
2. Download the Excel file: `globalterrorismdb_YYYY_Jan2023.xlsx`
3. File size: ~200MB

## Step 3: Place Data

```bash
# Create directory if needed
mkdir -p data/raw

# Move downloaded file
mv ~/Downloads/globalterrorismdb_*.xlsx data/raw/globalterrorismdb.xlsx
```

## Alternative: Sample Dataset

For initial development/testing, you can create a sample dataset:

```python
# Run this to create a sample GTD dataset
python scripts/create_sample_gtd.py
```

## Data Structure Preview

The GTD Excel file contains:
- **Sheet 1**: Main incident data (200k+ rows, 135+ columns)
- Key fields: eventid, iyear, imonth, iday, country_txt, region_txt, 
  city, latitude, longitude, attacktype1_txt, targtype1_txt, 
  weaptype1_txt, nkill, nwound, gname, summary

## Data Quality Notes

- Some incidents have missing coordinates
- Casualty counts may be estimates
- Group attribution can be uncertain
- Always check the 'doubtterr' field for uncertain classifications
