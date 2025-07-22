# things-demo-tests

Setup:

UI Tests
------------------

1. Created account in ThingsDemo.io
2. Created a Device 'TemperatureMonitoring', for some tese cases I have used already existing Device like 'DemoDHT22 Demo Device'
3. Created a 'TemperatureMonitoring' Dashboard.
4. Added two Widgets
    a. Temperature 
    b. Time Series chart
5. Tried to update the tmperature in real time using curl command and visualized the data
6. Also tried setting the Threshold temperature but was not succssfull in setting the Alarms and other monitoring tools

For API and Model Based Tests
------------------------------

1. Here I have used already existing Device 'DHT22 Demo Device' all the queries are made on this device


CI Pipeline
------------

1. The code has been committed to github - https://github.com/meghanavish/things-demo-tests/actions/runs/15627981605
2. The tests have run successfully and pytest reports are generated
3. There is an issue running the UI tests which needs further debugging, however screenshots of the UI tests run locally is attached in the Output_Screenshots folder.
4. The Output_Screenshots folder also has the API and Model based test reports downloaded from github.


Improvements
-----------------

Some improvements that should be made here

1. Hard coded Device token and ID which could otherwise be retrieved dynamically and passed to the subsequent methods.
2. Invalid test case are not handled
3. JWT token is hard coded
4. The hardcode values like jet token could be passed as secrets from github
5. Conditions for token expiry has to be checked and regenerated if expired
and futher more.