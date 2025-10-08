# GTD Field Reference

## Essential Fields for Analysis

### Temporal
- `iyear`, `imonth`, `iday`: Date components
- `date`: Formatted date string

### Geographic
- `country`, `country_txt`: Country code and name
- `region`, `region_txt`: Region code and name
- `provstate`: Province/state
- `city`: City name
- `latitude`, `longitude`: Coordinates

### Incident Characteristics
- `attacktype1_txt`: Attack methodology
- `targtype1_txt`: Target category
- `weaptype1_txt`: Weapon category
- `success`: Attack success (1=yes, 0=no)
- `suicide`: Suicide attack (1=yes, 0=no)

### Casualties
- `nkill`: Number killed
- `nwound`: Number wounded
- `nkillus`, `nwoundus`: US casualties
- `nkillter`, `nwoundte`: Terrorist casualties

### Perpetrators
- `gname`: Group name
- `gsubname`: Group subname
- `gname2`, `gname3`: Additional groups (if multiple)

### Details
- `summary`: Incident description
- `motive`: Stated motive
- `weapdetail`: Weapon details
- `target1`: Specific target entity

## Data Quality Indicators
- `doubtterr`: Doubt about terrorism classification
- `multiple`: Part of coordinated attack
- `ishostkid`: Hostage/kidnapping involved
