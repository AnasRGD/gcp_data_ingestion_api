# Batch Data Ingestion Process and exposition via API endpoint

## Project Overview :

This project consists of continually ingesting datas coming from CSV files. Once the data is available on a Data warehouse, Different endpoints must be exposed in order to provide either :
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

https://github.com/AnasRGD/gcp_data_ingestion_terraform


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
[felyx_assignement/reservations_to_bq/](https://github.com/AnasRGD/gcp_data_ingestion_api/tree/master/locations_to_bq)

For reservations : 
https://github.com/AnasRGD/gcp_data_ingestion_api/tree/master/reservations_to_bq

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





## 2nd Checkpoint : API endpoint from which this dataset can be retrieved in json format

_Prerequisite_ : Download Postman application to execute curl cmds.

### Step 1 : Create OAuth Credentials

Google uses OAuth 2.0 protocol for authentication and authorization. We need a valid key to send requests to BigQuery streaming API endpoints. 
We have to get OAuth 2.0 client credentials from Google cloud API console.
We need to make sure first that bigquery API is enabled.

![image](https://user-images.githubusercontent.com/68516240/174670368-74254405-60ff-4c3c-8b3f-179dc5efcc09.png)
Here the API is already enabled.


Then we need to click on 'Create Credentials'

![image](https://user-images.githubusercontent.com/68516240/174670502-c51da6e1-bd13-4053-be5a-f723537e4dab.png)


We choose “Create OAuth client ID” and apply the following settings : 

- Application Type: Web Application
- Name: Postman Client (Choose any names)
- Authorized redirect URIs: https://bigquery.googleapis.com

This will create OAuth ID. We will use these credentials (Client ID and Client Secret) in Postman to generate a token for every request to the BigQuery streaming API.

![image](https://user-images.githubusercontent.com/68516240/174670775-b87d9cbd-6f6f-48c6-a398-ad375350153e.png)



### Step 2 : Generating Token in Postman

In the authorization section, click on “get new access token”. And then configure the following parameters : 

- Token Name: felyx-token
- Grant Type: Authorization Code
- Callback URL: https://bigquery.googleapis.com
- Auth URL: https://accounts.google.com/o/oauth2/auth
- Access Token URL: https://oauth2.googleapis.com/token
- Client ID: Copy Google cloud OAuth credentials from GCP console or from the json file downloaded from the OAuth console.
- Client Secret: Copy from Google cloud OAuth credentials console or from the json file downloaded from the OAuth console.
- Scope: https://www.googleapis.com/auth/bigquery
- Client Authentication: Send client credentials in body

3. Click on “request token”.

4. Then finally, We follow this link to list the content of a table in rows :

For Reservation table : 
GET https://bigquery.googleapis.com/bigquery/v2/projects/felyx-assignement/datasets/INTEGRATION_IN/tables/reservations/data

For location table : 
GET https://bigquery.googleapis.com/bigquery/v2/projects/felyx-assignement/datasets/INTEGRATION_IN/tables/location/data

5. Click “send” request to execute the call.

We can see the location table Data in JSON format.

![image](https://user-images.githubusercontent.com/68516240/174669778-e24c8c78-4d95-47a3-94f4-b52f1c340c41.png)




## Access to GCP project is available upon request

