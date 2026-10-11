# Results
## Spatial Correlation Results (Molly)
<iframe src="https://at3group92026-rq8a73wjsafwnd7mhl5y2k.streamlit.app/?embed=true&refresh=20261010" width="100%" height="800" style="border: none;" allow="clipboard-write"> </iframe>

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 20px 0;
">

<strong>Key Insight</strong>

Your text goes here. Use this box to highlight an important finding, explain a concept, or introduce a section.

</div>

### Map 2
<iframe src="https://at3group92026-6tqnkabpc3aor2awnntgcy.streamlit.app/?embed=true&refresh=20261010" width="100%" height="800" style="border: none;" allow="clipboard-write"> </iframe>

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 20px 0;
">

<strong>Key Insight</strong>

Your text goes here. Use this box to highlight an important finding, explain a concept, or introduce a section.

</div>

### Map 3

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 20px 0;
">

<strong>Key Insight</strong>

Your text goes here. Use this box to highlight an important finding, explain a concept, or introduce a section.

</div>

# Socio Economic Correlation Results (Tara)
Note: Some scatter plots in this section have a line of best fit. This is to highlight the direction of correlation.

### Graph 1: Example Data with Sydney LGA
:::{figure} HighvsPO(SYD).png
:::

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 10px 0 40px;
">

This graph displays the relationship between property offences and year 12 completion. Sydney (labelled) stands out as an obvious outlier. This relationship with the Sydney LGA being an outlier due to its high crime rate occurs across all crime types. As such the following graphs will not include the Sydney LGA (see discussion for reasoning).

</div>

### Graph 2: Example Data without Sydney LGA
:::{figure} HighvsPO.png
:::

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 10px 0 40px;
">

Whilst this graph here does not display the strongest correlation out of all the relationships assessed in this analysis, it does show the greatest difference in the correlation p value between the dataset with the Sydney LGA and the dataset without the LGA. With the Sydney LGA, the relationship is not statistically signifigant but without the Sydney LGA it is (with an r value of -0.41, suggesting moderate negative correlation). 

</div>

### Graph 3: Example Data of High Correlation
:::{figure} HighvsVC.png
:::

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 10px 0 40px;
">

This graph displays the relationship with the strongest correlation (r = -0.74). This data displays that in greater Sydney, rates of violent crime and the percentage of residents who comeplete year 12 are strongly negatively correlated (as high school completion increases, violent crime decreases).

</div>

### Graph 3: Example Data of Moderate Correlation
:::{figure} UnemvsDO.png
:::

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 10px 0 40px;
">

This graph displays a relationship with moderate correlation (r = 0.40). This data displays that in greater Sydney, rates of drug offences and the rate of unemployment is moderatly positively correlated.

</div>

### Table 1: Pearson's Correlation Coefficients between Socioeconomic Factors and Crime Types
| Socioeconomic Factor | Violent Crime | Property Offences | Drug Offences |
|:---|:---:|:---:|:---:|
| Median Weekly Income ($) | -0.51 | -0.37 | Not Statistically Significant |
| Unemployment (%) | 0.44 | 0.36 | Not Statistically Significant |
| Year 12 Completion (%) | -0.44 | Not Statistically Significant | Not Statistically Significant |


### Table 2: Pearson's Correlation Coefficients between Socioeconomic Factors and Crime Types (Sydney LGA Removed)
| Socioeconomic Factor | Violent Crime | Property Offences | Drug Offences |
|:---|:---:|:---:|:---:|
| Median Weekly Income ($) | -0.67 | -0.48 | -0.41 |
| Unemployment (%) | 0.54 | 0.44 | 0.40 |
| Year 12 Completion (%) | -0.74 | -0.41 | Not Statistically Significant |

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 10px 0 40px;
">

TARA PUT SOME STUFF IN ABOUT THESE TABLES!!!!

</div>

# Time Correlation Results (Tara)

````{dropdown} Table 3: Crime Rate and Time Correlation (with Gradients)

| LGA | Drug Offences: Correlation Coefficient | Drug Offences: Gradient | Violent Crime: Correlation Coefficient | Violent Crime: Gradient | Property Offences: Correlation Coefficient | Property Offences: Gradient|
|:---|---:|---:|---:|---:|---:|---:|
| Bayside | -0.66 | -0.13 | 0.80 | 0.32 | -0.75 | -0.45 |
| Blacktown | 0.74 | 0.11 | 0.92 | 0.56 | -0.86 | -1.09 |
| Burwood | 0.62 | 0.19 | 0.88 | 0.66 | Not significant | 0 |
| Camden | -0.88 | -0.20 | 0.95 | 0.52 | Not significant | 0 |
| Campbelltown | -0.81 | -0.14 | 0.88 | 0.66 | -0.91 | -1.18 |
| Canada Bay | Not significant | 0 | 0.96 | 0.37 | -0.77 | -0.54 |
| Canterbury-Bankstown | Not significant | 0 | 0.78 | 0.36 | -0.85 | -0.65 |
| Cumberland | Not significant | 0 | 0.86 | 0.29 | -0.66 | -0.47 |
| Fairfield | Not significant | 0 | 0.72 | 0.22 | -0.91 | -0.80 |
| Georges River | Not significant | 0 | 0.67 | 0.11 | -0.63 | -0.41 |
| Hornsby | Not significant | 0 | 0.92 | 0.24 | -0.87 | -0.69 |
| Hunters Hill | Not significant | 0 | Not significant | 0 | -0.80 | -0.86 |
| Inner West | Not significant | 0 | 0.77 | 0.33 | -0.83 | -0.82 |
| Ku-ring-gai | Not significant | 0 | 0.94 | 0.21 | -0.90 | -0.57 |
| Lane Cove | Not significant | 0 | 0.87 | 0.25 | Not significant | 0 |
| Liverpool | Not significant | 0 | 0.89 | 0.69 | -0.77 | -0.71 |
| Mosman | Not significant | 0 | Not significant | 0 | -0.93 | -0.75 |
| North Sydney | -0.84 | -0.43 | Not significant | 0 | -0.92 | -0.88 |
| Northern Beaches | Not significant | 0 | 0.66 | 0.14 | -0.93 | -0.80 |
| Parramatta | 0.88 | 0.26 | 0.97 | 0.42 | Not significant | 0 |
| Penrith | -0.78 | -0.12 | 0.85 | 0.54 | -0.74 | -0.65 |
| Randwick | Not significant | 0 | 0.62 | 0.18 | -0.74 | -0.66 |
| Ryde | Not significant | 0 | 0.80 | 0.24 | Not significant | 0 |
| Strathfield | Not significant | 0 | 0.69 | 0.30 | Not significant | 0 |
| Sutherland | -0.62 | -0.14 | 0.77 | 0.33 | -0.90 | -0.80 |
| Sydney | 0.85 | -1.18 | Not significant | 0 | -0.65 | -1.59 |
| The Hills | -0.89 | -0.08 | 0.88 | 0.31 | -0.78 | -0.31 |
| Waverley | -0.74 | -0.41 | 0.74 | 0.20 | -0.78 | -0.89 |
| Willoughby | Not significant | 0 | 0.91 | 0.24 | -0.79 | -0.82 |
| Woollahra | -0.61 | -0.34 | 0.91 | 0.30 | -0.82 | -0.76 |
````
<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 10px 0 40px;
">

TARA PUT SOME STUFF IN ABOUT THESE TABLES!!!!

</div>

### Graph 4: Example Data of Strong Positive Correlation (Increase over Time)
:::{figure} paramatta.png
:::

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 10px 0 40px;
">

WRTIE STUFF HERE!!!!

</div>

### Graph 5: Example Data of Strong Negative Correlation (Decrease over Time)
:::{figure} NorthernBeaches.png
:::

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 10px 0 40px;
">

WRTIE STUFF HERE!!!!

</div>

### Graph 6: Example Data of No Correlation:
:::{figure} Will.png
:::

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 10px 0 40px;
">

WRTIE STUFF HERE!!!!

</div>

% Leave at the bottom
<div style="border-top: 1px solid #cccccc; margin-top: 35px; padding-top: 12px; font-size: 0.9em; color: #666;">
  GIS Project | Greater Sydney, New South Wales | 2015–2025
</div>

