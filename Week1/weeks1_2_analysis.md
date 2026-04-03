# Weeks 1–2 Dataset Exploration Summary

## Datasets
- `CRMLSListing202401.csv` (Listing 2024-01)
- `CRMLSListing202402.csv` (Listing 2024-02)
- `CRMLSSold202401.csv` (Sold 2024-01)
- `CRMLSSold202402.csv` (Sold 2024-02)

## Basic Shape
| Dataset | Rows | Columns |
| --- | ---: | ---: |
| Listing 2024-01 | 27,454 | 84 |
| Listing 2024-02 | 27,447 | 84 |
| Sold 2024-01 | 17,976 | 80 |
| Sold 2024-02 | 19,925 | 78 |

## Key Field Availability (Missing %)
Percent of missing values for key fields present in each dataset.

### Listing 2024-01
| Field | Missing % |
| --- | ---: |
| `ListPrice` | 0.27% |
| `ClosePrice` | 27.15% |
| `LivingArea` | 13.52% |
| `BedroomsTotal` | 13.10% |
| `BathroomsTotalInteger` | 9.26% |
| `PropertyType` | 0.00% |
| `ListAgentFullName` | 0.01% |
| `ListOfficeName` | 0.00% |
| `DaysOnMarket` | 0.00% |

### Listing 2024-02
| Field | Missing % |
| --- | ---: |
| `ListPrice` | 0.26% |
| `ClosePrice` | 37.55% |
| `LivingArea` | 13.76% |
| `BedroomsTotal` | 13.39% |
| `BathroomsTotalInteger` | 9.23% |
| `PropertyType` | 0.00% |
| `ListAgentFullName` | 0.01% |
| `ListOfficeName` | 0.00% |
| `DaysOnMarket` | 0.00% |

### Sold 2024-01
| Field | Missing % |
| --- | ---: |
| `ListPrice` | 0.19% |
| `ClosePrice` | 0.00% |
| `LivingArea` | 8.61% |
| `BedroomsTotal` | 8.35% |
| `BathroomsTotalInteger` | 5.98% |
| `PropertyType` | 0.00% |
| `ListAgentFullName` | 0.01% |
| `ListOfficeName` | 0.00% |
| `DaysOnMarket` | 0.00% |

### Sold 2024-02
| Field | Missing % |
| --- | ---: |
| `ListPrice` | 0.19% |
| `ClosePrice` | 0.00% |
| `LivingArea` | 8.04% |
| `BedroomsTotal` | 7.60% |
| `BathroomsTotalInteger` | 5.34% |
| `PropertyType` | 0.00% |
| `ListAgentFullName` | 0.01% |
| `ListOfficeName` | 0.00% |
| `DaysOnMarket` | 0.00% |

## Numeric Field Summary
Count, mean, median, min, and max for key numeric fields found.

### Listing 2024-01
| Field | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- |
| ListPrice | 27,381.00 | 935,864.54 | 599,000.00 | 1.00 | 110,000,000.00 |
| ClosePrice | 20,001.00 | 785,357.35 | 620,000.00 | 0.00 | 38,450,000.00 |
| LivingArea | 23,743.00 | 1,881.86 | 1,577.00 | 0.00 | 43,560.00 |
| BedroomsTotal | 23,857.00 | 3.08 | 3.00 | 0.00 | 62.00 |
| BathroomsTotalInteger | 24,913.00 | 2.45 | 2.00 | 0.00 | 72.00 |
| DaysOnMarket | 27,454.00 | 33.07 | 20.00 | -58.00 | 812.00 |

### Listing 2024-02
| Field | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- |
| ListPrice | 27,376.00 | 959,670.03 | 625,000.00 | 0.75 | 70,000,000.00 |
| ClosePrice | 17,141.00 | 860,819.37 | 670,000.00 | 0.00 | 117,500,000.00 |
| LivingArea | 23,669.00 | 1,894.20 | 1,600.00 | 0.00 | 104,410.00 |
| BedroomsTotal | 23,772.00 | 3.09 | 3.00 | 0.00 | 43.00 |
| BathroomsTotalInteger | 24,913.00 | 2.45 | 2.00 | 0.00 | 43.00 |
| DaysOnMarket | 27,447.00 | 26.75 | 17.00 | -13.00 | 2,539.00 |

### Sold 2024-01
| Field | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- |
| ListPrice | 17,942.00 | 721,018.17 | 549,000.00 | 1.40 | 32,000,000.00 |
| ClosePrice | 17,976.00 | 730,220.80 | 540,000.00 | 1.30 | 417,255,000.00 |
| LivingArea | 16,428.00 | 1,768.09 | 1,538.00 | 0.00 | 27,396.00 |
| BedroomsTotal | 16,475.00 | 3.02 | 3.00 | 0.00 | 46.00 |
| BathroomsTotalInteger | 16,901.00 | 2.38 | 2.00 | 0.00 | 44.00 |
| DaysOnMarket | 17,976.00 | 46.74 | 28.00 | -36.00 | 4,049.00 |

### Sold 2024-02
| Field | count | mean | median | min | max |
| --- | --- | --- | --- | --- | --- |
| ListPrice | 19,887.00 | 774,348.35 | 594,000.00 | 1.25 | 39,500,000.00 |
| ClosePrice | 19,925.00 | 770,611.13 | 590,000.00 | 0.00 | 31,900,000.00 |
| LivingArea | 18,324.00 | 1,779.35 | 1,560.50 | 0.00 | 61,821.00 |
| BedroomsTotal | 18,410.00 | 3.03 | 3.00 | 0.00 | 36.00 |
| BathroomsTotalInteger | 18,861.00 | 2.42 | 2.00 | 0.00 | 175.00 |
| DaysOnMarket | 19,925.00 | 43.82 | 20.00 | -13.00 | 3,451.00 |

## Listing vs. Sold Columns
- Common columns: 73
- Listing-only columns: 11
- Sold-only columns: 9

### Sample Listing-only Columns
`BuyerOfficeName.1`, `CloseDate.1`, `DaysOnMarket.1`, `Latitude.1`, `ListAgentFirstName.1`, `ListAgentLastName.1`, `ListPrice.1`, `LivingArea.1`, `Longitude.1`, `PropertyType.1`, `UnparsedAddress.1`

### Sample Sold-only Columns
`BasementYN`, `BuyerAgentAOR`, `Flooring`, `ListAgentAOR`, `OriginatingSystemName`, `OriginatingSystemSubName`, `PoolPrivateYN`, `ViewYN`, `WaterfrontYN`
## Data Counts
Listed total rows: 853,416
Sold total rows: 591,246

### Listed Monthly Row Counts
| File | Rows |
| --- | --- |
| CRMLSListing202401.csv | 27,454 |
| CRMLSListing202402.csv | 27,447 |
| CRMLSListing202403.csv | 32,282 |
| CRMLSListing202404.csv | 36,503 |
| CRMLSListing202405.csv | 38,796 |
| CRMLSListing202406.csv | 35,894 |
| CRMLSListing202407.csv | 36,340 |
| CRMLSListing202408.csv | 35,305 |
| CRMLSListing202409.csv | 34,625 |
| CRMLSListing202410.csv | 34,730 |
| CRMLSListing202411.csv | 25,128 |
| CRMLSListing202412.csv | 19,417 |
| CRMLSListing202501.csv | 37,469 |
| CRMLSListing202502.csv | 33,983 |
| CRMLSListing202503.csv | 38,492 |
| CRMLSListing202504.csv | 40,187 |
| CRMLSListing202505.csv | 40,271 |
| CRMLSListing202506.csv | 26,399 |
| CRMLSListing202507.csv | 27,345 |
| CRMLSListing202508.csv | 25,210 |
| CRMLSListing202509.csv | 26,923 |
| CRMLSListing202510.csv | 27,586 |
| CRMLSListing202511.csv | 20,677 |
| CRMLSListing202512.csv | 18,773 |
| CRMLSListing202601.csv | 35,302 |
| CRMLSListing202602.csv | 31,762 |
| CRMLSListing202603.csv | 39,116 |

### Sold Monthly Row Counts
| File | Rows |
| --- | --- |
| CRMLSSold202401.csv | 17,976 |
| CRMLSSold202402.csv | 19,925 |
| CRMLSSold202403.csv | 23,276 |
| CRMLSSold202404.csv | 24,640 |
| CRMLSSold202405.csv | 26,487 |
| CRMLSSold202406.csv | 24,328 |
| CRMLSSold202407.csv | 26,240 |
| CRMLSSold202408.csv | 24,558 |
| CRMLSSold202409.csv | 21,267 |
| CRMLSSold202410.csv | 23,274 |
| CRMLSSold202411.csv | 20,279 |
| CRMLSSold202412.csv | 20,241 |
| CRMLSSold202501.csv | 18,738 |
| CRMLSSold202502.csv | 18,702 |
| CRMLSSold202503.csv | 21,445 |
| CRMLSSold202504.csv | 23,262 |
| CRMLSSold202505.csv | 23,154 |
| CRMLSSold202506.csv | 22,883 |
| CRMLSSold202507.csv | 23,646 |
| CRMLSSold202508.csv | 22,972 |
| CRMLSSold202509.csv | 22,443 |
| CRMLSSold202510.csv | 23,233 |
| CRMLSSold202511.csv | 19,088 |
| CRMLSSold202512.csv | 20,538 |
| CRMLSSold202601.csv | 16,487 |
| CRMLSSold202602.csv | 19,060 |
| CRMLSSold202603.csv | 23,104 |
