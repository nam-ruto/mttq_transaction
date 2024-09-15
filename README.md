## Transaction Statement

**1. Project Structure**
```
├── .streamlit
│   ├── config.toml
│   └── secrets.toml
├── main.py
└── requirements.txt
```

**2. Dependencies**  
Make sure you install all required dependencies: ```pip install requirements.txt```  
There are 2 required packages you have to install if using PostgreSQL database:
```
psycopg2-binary==x.x.x
sqlalchemy==x.x.x
```

**3. Data**  
Data will be uploaded later. However, you can access data provided by MTTQVN [Account Statement](https://drive.google.com/file/d/18dIWiReYtJkyuQ_8vSBJWweGaD71rBpu/view?fbclid=IwY2xjawFTMKVleHRuA2FlbQIxMAABHf_DWcr9W_RZV5SjskTgjKOIcRd2fSSNRwtGNimH7E6zecT6CLezms40lA_aem_yILZmkLi3BmNbVRktpcvPw).  
Then, try to use [pdfplumber](https://pypi.org/project/pdfplumber/0.1.2/) to extract data from pdf file.  

Cheers😄
