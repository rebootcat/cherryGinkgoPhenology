# **cherryGinkgoPhenology**

This repository accompanies the manuscript **"Cherry blossom and ginkgo leaf coloration phenology dataset of China from 2009 to 2019 extracted from big data"** by Shenghong Wang, Haolong Liu, Xinyue Qin, Junhu Dai and **Jun Liu** *. All necessary Python scripts and data to reproduce included results are provided.  
   		  
## Abstract
Ground-based phenological observation data is the most accurate phenological monitoring data currently available. Making effective use of available information on social media to retrieve phenological data is of considerable value in alleviating the lack of phenological data in regions with missing observation sites. In this study, a logistic curve fitting method was developed to extract phenological data on specific species from social media data. After verifying the relationship between the site observation data and the temperature, timing data for two typical phenological phenomena in China, namely cherry blossom flowering in spring and ginkgo leaf coloration in autumn were reconstructed and published. The data availability is from 2010 to 2019 with 176 cities and 2009 to 2018 with 155 cities, respectively. This dataset is an effective supplement for existing phenological data, and this method also provides a reference for obtaining phenological data for specific species.  


## Disclaimer
The code in this repository represents one version of the code developed for the project and may yet undergo changes and revisions.

## Authors
The code was developed through collaboration between Shenghong Wang and Jun Liu.


## Contacts    
Shenghong Wang - wangshenghong@stu.scu.edu.cn     
Jun Liu -  liujun_igsnrr@126.com

## Usage
- The "logisticRegression" folder contains algorithms for keywords filter and plant viewing timing reconstruction.
- The "dataValidation" folder contains Python scripts for data validation using temperature data.

## Data access
- **Weibo data**: The Weibo data were obtained from Sina Weibo(https://open.weibo.com). Detailed data is not allowed for open access according to data use agreement. So we can not provide raw data here.
- **Observation data**: The phenological data used for data validation were obtained from the “Chinese Phenological Observation Network” (http://www.cpon.ac.cn).
- **Meteorological data**: The meteorological data were obtained from the "China surface Climate Data Log dataset (V3.0)" provided by the National Meteorological Science Data Center (http://data.cma.cn/).



## Requirements
- Database: 
  - Mysql: 5.7.33
  - Redis: 6.2.5
  - Mongo: 5.0.2
- Python: 3.6.3  
- Other attached packages: 
  - numpy: 1.13.1  
  - pandas: 0.20.3  
  - pymongo: 3.4.0  
  - PyMySQL: 0.7.9  
  - redis: 4.3.1  
  - scikit_learn: 1.1.2  
  - scipy: 0.19.1  