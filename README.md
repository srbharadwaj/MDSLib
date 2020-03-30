**MDS API/SDK Library**

A common library to work with Cisco MDS switches.
This library will be useful for automating day to day tasks or developing new tools which involve Cisco MDS switches

Supported NXOS image: 8.4(2) and above

Python version: 3.6 and above

###### **Steps to run it:**
1) First create a virtual environment with python3

       virtualenv mytestlib -p python3

2) Activate the virtual env

       cd mytestlib/
       source bin/activate
       
3) Next download the zip file from the github (`mdsLib-master.zip`)
4) unzip the file

       unzip mdsLib-master.zip
           
5) under that folder you will see a `setup.py` file execute the `setup.py` file
       
       cd mdsLib-master/
       python setup.py install
       
6) Once successfully done issue `pip list` and you should see these packages installed
     
        
        >>> pip list
        Package    Version   
        ---------- ----------
        certifi    2019.11.28
        chardet    3.0.4     
        idna       2.8       
        mdslib     1.0       <---
        pip        20.0.1
        paramiko   2.7.1     <---
        requests   2.22.0    <---
        setuptools 45.1.0    
        urllib3    1.25.8    <---
        wheel      0.33.6  `