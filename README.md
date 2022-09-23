# **cherryGinkgoPhenology**
<a href="https://github.com/rebootcat/cherryGinkgoPhenology">
    <img src="https://img.shields.io/github/stars/rebootcat/cherryGinkgoPhenology.svg?colorA=orange&colorB=orange&logo=github"
         alt="GitHub stars">
  </a>
  <a href="https://github.com/rebootcat/cherryGinkgoPhenology/issues">
        <img src="https://img.shields.io/github/issues/rebootcat/cherryGinkgoPhenology.svg"
             alt="GitHub issues">
  </a>
  <a href="https://github.com/rebootcat/cherryGinkgoPhenology/">
        <img src="https://img.shields.io/github/last-commit/rebootcat/cherryGinkgoPhenology.svg">
  </a>
  <a href="https://github.com/rebootcat/cherryGinkgoPhenology/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/rebootcat/cherryGinkgoPhenology.svg"
             alt="GitHub license">
</a>


This repository accompanies the manuscript **"Cherry blossom and ginkgo leaf coloration phenology dataset of China from 2009 to 2019 extracted from big data"** by Shenghong Wang, Haolong Liu, Xinyue Qin, Junhu Dai and **Jun Liu** *. All necessary Python scripts and data to reproduce included results are provided.  

<img src="https://firebasestorage.googleapis.com/v0/b/firescript-577a2.appspot.com/o/imgs%2Fapp%2Frebootcat%2FQ2lX64ANBd.png?alt=media&token=e1234703-1441-4e99-af76-85f4fb19a390" width="800" title="data records of cherry blossom and ginkgo leaf coloration">

   		  
## Abstract
Ground-based phenological observation data are the most accurate phenological monitoring data currently available. Making effective use of available information on social media to retrieve phenological data is of considerable value in alleviating the lack of phenological data in regions with missing observation sites. In this study, a logistic curve fitting method was developed to extract phenological data on specific species from social media data. After verifying the relationship between the site observation data and the temperature, timing data for two typical phenological phenomena in China, namely cherry blossom flowering in spring and ginkgo leaf coloration in autumn were reconstructed and published. The data availability is from 2010 to 2019 in 176 cities and 2009 to 2018 in 155 cities. This dataset is an effective supplement for existing phenological data, and this method also provides a reference for obtaining phenological data for specific species.  


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
- **Weibo data**: The Weibo data were obtained from the API (application programming interface) provided by the Sina Weibo(http://openapi.sc.weibo.com). According to the term "4.2 Party B's rights and obligations" of  contract, "party B shall not allow a third party to use commercial data obtained through this agreement by any means such as gift, sale, authorization, etc." So we are prohibited to provide any detail of the raw data to open access here. For repeat this work, please contact businessapi@staff.weibo.com for support. The api document uesd for this work is available at http://openapi.sc.weibo.com/api/detail?t=search/statuses/limited. The Business Data Service Package Tariffs as of December 2020 are provided below.  

|plan|quota of content data|service life|Package usage fee(CNY)|Off package usage fee(CNY)|  
| ---- | ---- | ---- | ---- | ---- |  
|A|20 million|one year|60,000|2.8 / thousands|  
|B|100 million|one year|250,000|1.7 / thousands| 
|C|500 million|one year|800,000|1.3 / thousands| 

- **Observation data**: The phenological data used for data validation were obtained from the "Chinese Phenological Observation Network" (http://www.cpon.ac.cn).
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