# Platform Migration Tool

A proof of concept usage of the [Veracode APIs](https://docs.veracode.com/r/Veracode_APIs) to move the Application Profiles and Teams in a Commercial Platfrom account into the FedRAMPed Veracode Platform. Written in Python using an amended [veracode-api-py](https://github.com/veracode/veracode-api-py) library.

This script assumes and has only been created to move profiles from a Commercial account into a FedRAMP location. It could concuptually work in reverse with minimal tweaking and testing that has not yet been done. 

## Setup

This script uses [Python](https://www.python.org). Ensure you have python installed. Clone or download/unzip this repo into a folder and then install the dependencies for this project:

    python --version
    pip --version
    pip install -r requirements.txt

This script requires two credentials: 
1. API Credentials for the Commercial account from which the Application profiles and associated data will be exported from noted in a credentials file as `[migratefrom]`

2. API Credentials for the account to which the profiles above will be imported into, also in the same credentials file as `[migrateto]`

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

An example of how to generate credentials and create the Credentials file is also provided on the [Veracode Help Center](https://docs.veracode.com/r/c_configure_api_cred_file)

## Run

Once setup is completed, run by calling in a Terminal or cmd window from the folder where this project was downloaded:

    python migrate-platform.py

## Note

At this time the script is not configured to transfer over Custom Fields on an Application Profile
