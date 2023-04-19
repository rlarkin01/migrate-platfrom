# Platform Migration Tool

A proof of concept usage of the [Veracode APIs](https://docs.veracode.com/r/Veracode_APIs) to move the Application Profiles and Teams in a Commercial Platfrom account into the FedRAMPed Veracode Platform. Written in Python using an amended [veracode-api-py](https://github.com/veracode/veracode-api-py) library.

## Setup

This script uses [Python](https://www.python.org). Ensure you have python installed. 

    python --version
    pip --version

Clone or download/unzip this repo into a folder and then install the dependencies for this project:

    pip install -r requirements.txt

### Credentials and Permissions

This script requires two credentials: 
1. API Credentials for the Commercial account from which the Application profiles and associated data will be exported from noted in a credentials file as `[migratefrom]`. This account needs read access to all of elements that need to be migrated. 
    - the easiest way to do this is to give the user the Security Lead role 

2. API Credentials for the account to which the profiles above will be imported into, also in the same credentials file as `[migrateto]`. This user needs:
    - the Administrator role to create BUs and Teams
    - the Policy Administrator role to create Policies
    - and either the Creator or Security Lead role in order to create Applciations. 
 Read more on [Veracode Users and Permissions in the Doc Center](https://docs.veracode.com/r/c_role_permissions).

Save Veracode API credentials for both the origniation and destination accounts in a credentials file in your home folder `~/.veracode/credentials` like this (example of Commercial to FedRAMP):

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

    [migratefrom]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

    [migrateto]
    veracode_api_key_id = <vera01fi-YOUR_API_KEY_ID>
    veracode_api_key_secret = <vera01fi-YOUR_API_KEY_SECRET>

An example of how to generate credentials and create the Credentials file is also provided on the [Veracode Doc Center](https://docs.veracode.com/r/c_configure_api_cred_file)

## Run

Once setup is completed, run by calling in a Terminal or cmd window from the folder where this project was downloaded:

    python migrate-platform.py

## Note

At this time the script is not configured to transfer over Custom Fields on an Application Profile
