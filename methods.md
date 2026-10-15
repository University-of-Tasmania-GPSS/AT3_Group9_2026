# Methods

## Study Area and Research Design 

The study area for this project is the Greater Sydney Region, New South Wales (NSW), Australia, as seen in Figure 1. This region was selected due to the availability of sufficient crime data and socioeconomic statistics to support spatial and statistical analysis. 30 LGAs across the Greater Sydney area were selected for the analysis and can be seen in Figure 1. The study examines crime patterns across Local Government Areas (LGAs) between 2015 and 2025, focusing on drug offences, violent crime and property offences. The analysis explores the spatial distribution of crime and its relationship with unemployment, median income and high-school completion rates.

### Locality Map
:::{figure} Locality Map.jpg
:label: fig: local map

Locality Map of the Local Government Areas (LGA) of Greater Sydney that were used in this project 

:::


Three primary datasets were used to investigate the spatial and socioeconomic distribution of crime across selected Local Government Areas (LGAs) in Greater Sydney between January 2015 and December 2025. Crime incident data were obtained from the NSW Bureau of Crime Statistics and Research (BOCSAR), LGA boundary data from the Australian Bureau of Statistics (ABS), and socioeconomic indicators from the 2021 Australian Census.

The datasets were cleaned, aggregated and integrated into a common spatial dataset to enable comparisons between crime patterns and socioeconomic characteristics. The following tables summarise the source data, file formats and their roles in the analysis.



## Methodological Workflow

The Figure 2 summarises the research
workflow, from data collection and preparation
through to spatial and socioeconomic analysis.

```{mermaid}
flowchart TD
    A["1. Research question:<br/>Spatial distribution of crime and<br/>socioeconomic associations"]
    B["2. Data collection:<br/>BOCSAR crime records, ABS LGA boundaries<br/>and 2021 Census data"]
    C["3. Data preparation:<br/>Select 30 LGAs, group offence categories,<br/>aggregate monthly crime records for 2015–2025"]
    D["4. Data integration:<br/>Join crime and socioeconomic data<br/>to LGA polygons"]
    E["5A. Spatial analysis:<br/>Annual crime counts, population-adjusted rates<br/>and Getis–Ord Gi* hotspot analysis"]
    F["5B. Socioeconomic analysis:<br/>Correlations with income, unemployment<br/>and high-school completion"]
    G["6. Visualisation and interpretation:<br/>Crime distribution maps, hotspot patterns,<br/>correlations and changes over time"]

    A --> B --> C --> D
    D --> E
    D --> F
    E --> G
    F --> G

    classDef main fill:#244B36,color:#ffffff,stroke:#244B36,rx:15,ry:15
    classDef prep fill:#FFF3C4,color:#333333,stroke:#D4B94E,rx:15,ry:15
    classDef spatial fill:#F9DEDE,color:#333333,stroke:#B85450,rx:15,ry:15
    classDef socio fill:#DFEAF9,color:#333333,stroke:#547EAE,rx:15,ry:15

    class A,G main
    class B,C,D prep
    class E spatial
    class F socio

```
:::{figure}
:label: fig: flowchart

Flowchart of methodology used in this project 

:::

## Detailed Methodology

The following sections provide further details of the data preparation, socioeconomic statistical analysis and spatial hotspot analysis. Expand each section to explore the methodology.

% DATA COLLECTION AND PREPARATION
````{dropdown} Data Collection and Preparation

**Data sources**

Three primary datasets were used in this study:

| Dataset | Source | Purpose |
|---|---|---|
| Local Government Areas (2025) | Australian Bureau of Statistics (ABS) | Provided polygon geometries and geographic identifiers for the 30 selected LGAs. |
| Recorded Criminal Incidents by Month by LGA | NSW Bureau of Crime Statistics and Research (BOCSAR) | Provided monthly recorded crime counts for 2015–2025. |
| 2021 Census General Community Profile G01, G02 & G43 | Australian Bureau of Statistics (ABS) | Provided socioeconomic indicators for education, household income and labour force characteristics. |

**Crime classification**

Recorded offences were grouped into three categories:

- **Drug offences:** Possession, dealing, manufacturing and importing.
- **Violent crime:** Abduction and kidnapping, assault, coercive control, homicide, intimidation, stalking and harassment, sexual offences, and robbery.
- **Property offences:** Theft, arson and malicious damage to property.

**Data preparation**

Python was used to clean and integrate the datasets. 

The following libaries were used during this project:

```python
import geopandas as gpd
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plot
from scipy import stats
```

The workflow involved:

1. Selecting the 30 study-area LGAs using their geographic identifiers.
2. Filtering crime records to the selected LGAs and relevant offence categories.
3. Aggregating monthly crime records into annual counts for 2015 - 2025.
4. Extracting the relevant socioeconomic indicators from the 2021 Census.
5. Joining crime and socioeconomic attributes to the LGA polygons using matching geographic identifiers.
6. Checking for missing values, inconsistent identifiers and invalid geometries.

The resulting spatial dataset:
```python
SydneyLGAs_MGA202056_socioecon_crime_2015_2025.shp
```
provided a consistent geographic framework for mapping crime, calculating rates, identifying hotspots and examining socioeconomic associations.

````

% SPATIAL ANALYSIS
````{dropdown} Spatial Analysis

*Crime Counts*

Total recorded incidents were calculated for each LGA and crime category across 2015–2025 by summing the annual recorded crime counts over the study period. These totals were used to compare the overall count and spatial distribution of drug offences, violent crime and property offences. Python and Geopandas were used for this analysis.


*Crime Rates*

Crime rates were calculated to account for differences in population size between LGAs, allowing for more meaningful comparisons of crime levels across the study area. Python and Geopandas were used for this analysis.

$$ \text{Crime rate} = 
\frac{\text{Total recorded incidents (2015–2025)}} 
{\text{Population denominator}} 
\times 1000 
$$ 

This measure expresses recorded incidents per 1,000 residents over the study period for each LGA. 

The resulting spatial dataset:
```python
SydneyLGAs_SpatialCrimeAnalysis.shp
```
contained both crime rate and counts for each LGA and was used for visualisation of these results.


**Getis–Ord Gi* Hotspot Analysis**

The Getis–Ord statistics were used to examine the spatial concentration of crime rates across the selected LGAs. The analysis included the Global Getis–Ord (G) statistic, which measures overall spatial concentration, and the Local Getis–Ord (G_i^*) statistic, which identifies individual LGAs forming clusters of high or low crime-rate values (PySAL, 2018).

The analysis was conducted in Python uisng PySAL. The following libaries were used during the hotpsot analysis:
```python
from esda.getisord import G
from esda.getisord import G_Local
from libpysal import weights
```

Two statistics were computed per crime type (violent crime, property offences and drug offences):

1. **Global Getis–Ord G**

The Global Getis–Ord (G) statistic measures whether high or low values are spatially concentrated across the study area. The observed (G) statistic is compared with its expected value under spatial randomness. A Z-score and p-value are then used to assess whether the observed spatial concentration is statistically significant.

2. **Local Getis–Ord (G_i^*)**

The Local Getis–Ord (G_i^*) statistic identifies individual LGAs where crime rates are spatially clustered. It considers the value of the focal LGA and the values of its neighbouring LGAs.

The analysis used:

- **Input variables:** Crime rates per 1,000 residents for drug offences, violent crime and property offences.

- **Spatial weights:** Queen contiguity, where LGAs are neighbours if their polygons share an edge or vertex. Binary spatial weights assigned a value of 1 to neighbouring LGAs and 0 to non-neighbouring LGAs.

- **Statistics:** Both Global Getis–Ord G and Local Getis–Ord Gi* statistics were calculated. Global G assessed the overall spatial concentration of crime rates across the study area, while Local Gi* identified individual LGAs with clusters of high or low values.

- **Permutations:** 199 permutations were used for the Local Gi* analysis because larger permutation counts caused computational problems (computer used did not have enough processing capcity). A fixed random seed of 12345 was used to support reproducibility.

- **Significance threshold:** (p < 0.05), using permutation-based p-values for the Local Gi* analysis.

- **Classification:** LGAs were classified as hotspots, coldspots or not statistically significant based on their Local Gi* Z-scores and p-values.

The Local (G_i^*) analysis was performed separately for drug offences, violent crime and property offences, using crime rates per 1,000 residents. Statistical significance was assessed using 199 permutations, a fixed random seed of 12345 and a threshold of (p < 0.05). The Global (G) statistic used an analytical normal approximation to calculate its Z-score and p-value.

LGAs with statistically significant positive Local (G_i^*) Z-scores were classified as hotspots, indicating clusters of relatively high crime rates. LGAs with statistically significant negative Z-scores were classified as coldspots, indicating clusters of relatively low crime rates. LGAs that did not meet the significance threshold were classified as not statistically significant. The resulting classifications were mapped to compare spatial patterns across the three crime categories.

The resulting spatial dataset:
```python
SydneyLGAs_GetisOrd.shp
```
was used for visualisation of the hotspot results.
````


% SOCIOECON ANALYSIS
````{dropdown} Socioeconomic Statistical Analysis

The socioeconomic analysis investigated associations between crime and four indicators: time, year 12 completion in the adult population, household income and unemployment.

**Socioeconomic indicators**

- **Education:** Highest year of school completed, Year 12 or equivalent, sourced from 2021 Census Table G01.
- **Household income:** Median total weekly household income, sourced from 2021 Census Table G02.
- **Unemployment:** Selected labour force statistics, sourced from 2021 Census Table G43.

**Percentage Computation**

High-school completion and unemployment percentages were calculated for each LGA using data from the 2021 Australian Census. High-school completion was calculated by dividing the number of people whose highest year of school completion was Year 12 or equivalent by the total population aged 20 years and over, then multiplying by 100. The population aged 20 years and over was calculated by summing the Census age groups from 20–24 years to 85 years and over.

$$
\text{High-school completion (\%)} =
\frac{\text{People with Year 12 completion}}
{\text{Population aged 20 years and over}}
\times 100
$$

Unemployment percentage was calculated by dividing the number of unemployed people looking for work by the total labour force, then multiplying by 100. The total labour force was used as the denominator rather than the total population, as this measure relates to people participating in the labour force rather than the entire population, which includes children.

$$
\text{Unemployment (\%)} =
\frac{\text{Unemployed people looking for work}}
{\text{Total labour force}}
\times 100
$$

The calculated percentages and median weekly household income were joined to the LGA polygon dataset using matching geographic identifiers, allowing the socioeconomic indicators to be mapped and compared with crime patterns across the study area.



**Analytical approach**

The socioeconomic indicators were compared with drug offences, violent crime and property offences to investigate potential relationships between socioeconomic conditions and crime. The socioeconomic variables represent conditions recorded at the 2021 Census, while crime data span 2015–2025. Pearson's correlation coefficient is a value between -1 and 1 which quantifies how linear the relationship between 2 variables is. The signifigance threshold was a p value of 0.05. Pearson's correlation coefficent represents assosiations between datasets, not nessesarily causation. 

The analysis considered:
1. Associations between socioeconomic characteristics and crime rates across the selected LGAs. 
2. Relationships between changes in annual crime rates and time within individual LGAs.


**Socioeconomic Correlation Analysis**

Pearson's correlation coeffcient was calculated for each crime type (rate per 1000 people for each LGA) and each socioeconomic variable (for each LGA) resulting in r and p values.  

**Time Correlation Analysis**

Annual crime rates from 2015–2025 were plotted for individual LGAs to examine changes over time. SciPy was used to perform a Least Squares Analysis on the dataset to determine a linear (first order) line of best fit for the dataset. The slope value of this line of best fit was used to quantify the rate of change over time. Statistical significance was assessed using a threshold of \(p < 0.05\). LGAs which did not have a statistically signifigant change in crime rate over time were given a rate of change over time value of 0. 

The resulting spatial dataset:
```python
SydneyLGAs_MGA202056_socioecon_crime_2015_2025.shp
```
contained the relevant values and percentages for the three socioeconomic factors 
````

% MAPS AND GRAPHS
````{dropdown} Results Visualisation 

*Web Maps* 

Three interactive web maps were developed using Python and the Leafmap library to explore and communicate the spatial distribution of crime and its relationship with socioeconomic characteristics across Greater Sydney LGAs. The maps were developed using the streamlit-map-template (https://github.com/opengeos/streamlit-map-template) repository by OpenGeo, which provided the base template for the web applications. Leafmap was used to create the interactive maps and display the spatial datasets. Each map was published as an individual web application using Streamlit by connecting the relevant Python script from our GitHub repository. 

Python was used to create the map web code and the following libaries were imported during the creation of the web maps:

```python
import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import pandas as pd
from pathlib import Path
from folium.plugins import MeasureControl
```

The following three web maps were created: 

1. **Crime counts and rates:** The first map displayed recorded crime counts and crime rates per 1,000 residents for drug offences, violent crime and property offences. This allowed users to compare the count and population-adjusted distribution of each crime category across LGAs. 

2. **Crime hotspots:** The second map displayed the Local Getis–Ord Gi* hotspot classifications for each crime category, distinguishing hotspots, coldspots and areas that were not statistically significant. This enabled comparisons of spatial clustering patterns between crime types. 

3. **Crime trends and socioeconomic characteristics:** The third map explored recorded crime trends across Greater Sydney LGAs from 2015 to 2025. Interactive pop-ups displayed socioeconomic indicator values for each LGA from the 2021 Census, including household income, unemployment and high school completion rate. This allowed users to explore changes in crime alongside the socioeconomic characteristics of each area.


*Graphs*

Python was used to create all graphs using the following libaries:

```python
import numpy as np
from scipy import stats
import geopandas as gpd
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plot

Graphs were used to examine relationships between crime rates and socioeconomic indicators, including household income, unemployment and high-school completion. Additional time-series graphs illustrated changes in crime rates between 2015 and 2025, allowing comparisons between LGAs and investigation of trends within selected areas.
```

````

<div style="border-top: 1px solid #cccccc; margin-top: 35px; padding-top: 12px; font-size: 0.9em; color: #666;">
  GIS Project | Greater Sydney, New South Wales | 2015–2025 | M. Marshall & T. Powell
</div>










