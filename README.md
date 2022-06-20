# Felyx Data Engineering Assignement

## Assignement Overview :

This assignement consists of continually ingesting datas coming from CSV files. Once the data is available on a Data warehouse, Different endpoints must be exposed in order to provide either :
  - List of all table rows in json format.
  - List of all table rows in csv format.
  - List of rides count per location.
  - And finally, a test file showing a unit test.
 
 
Here, the datas sources comes from two different sources :

1 - Reservation Data : 
This dataset contains information on some the reservations customers have made.

2 - Location Data :
This dataset contains information on locations.


## 1st Checkpoint : Data Ingestion

I will start first by loading the csv files into Bigquery. 
A basic architecture of loading a CSV data from GCS to BQ will be used. I will make an automated process using Cloud Function so that whenever there is a new file getting created in the GCS, an event triggers Cloud Function so the data gets loaded into BQ.

Herafter the steps i followed : 

First of all, i created a new GCP project and enabled BigQuery, Cloud Functions, and API Gateway APIS.


### Step 1 : Static ressources creation 
To make it more interesting, i decided to create all the static ressources (GCS buckets, roles, service accounts and Datasets) using Terraform.
Please find below the link to my Terraform repo : 




### Step 2 : Create a Cloud Function with a GCS Create event trigger 

**2.1 **: We start first by creating a Cloud Function with a GCS Event Trigger

![image](https://user-images.githubusercontent.com/68516240/174658641-a19b59a6-f05a-405a-8f77-a9b8ebaef1d5.png)

**2.2** : While creating a function, use the GCS as the trigger type and event as Finalize/Create. So that whenever there is a new file getting landed into our GCS bucket, Cloud function can detect this event and trigger a new run of our source code.
Once the trigger is selected, select the bucket you want to use as a trigger source. In this case we will select the bucket felyx-ar-integration-in since we will be uploading the file to this bucket once our function is ready. Hit Save.

**N.B** : Region must be set on an European Location so that the GDPR will be applicable 

![image](https://user-images.githubusercontent.com/68516240/174659063-61d210ce-bec6-4c70-8a64-6a5f73e02f2f.png)

**2.3** : Change the runtime configurations if needed. For this example, we will use the default values.

**2.4** : Click next and in the next page, select the runtime programming language you would like to use. For this example we will use Python 3.7.

The python code to automatically load the csv files into bq is available at : 

For location files : 
[felyx_assignement/reservations_to_bq/](https://github.com/AnasRGD/felyx_assignement/tree/master/locations_to_bq)

For reservations : 
https://github.com/AnasRGD/felyx_assignement/tree/master/reservations_to_bq

Once the functions are correctly deployed, we must have something like this : 

![image](https://user-images.githubusercontent.com/68516240/174661331-d09fc6b3-8023-4b0c-877b-f7138cdcb89d.png)


**_Disclaimer ! :_**
The schemas provided in the assignment do not match with the files as many rows are present in the csv file and not the schema ..


**2.5** : Testing the ingestion architecture

For the final part, let us upload the CSV file to the GCS bucket and watch the data load happen automatically.

![image](https://user-images.githubusercontent.com/68516240/174661940-43e8c967-99e0-4535-9ace-3355afc6b449.png)


We verify that the Function was successfully triggered and the function execution is successful.

![image](https://user-images.githubusercontent.com/68516240/174662083-1b0717c7-1705-4685-89f0-faeda8ec294e.png)

We navigate to the BQ Console and execute the following SQL to check the table contents.

SELECT * FROM `felyx-assignement.INTEGRATION_IN.reservations` 
ORDER BY row ASC
LIMIT 10

![image](https://user-images.githubusercontent.com/68516240/174662448-f661725e-e862-4e18-b562-d26f16de9127.png)





## Access to GCP project is available upon request

