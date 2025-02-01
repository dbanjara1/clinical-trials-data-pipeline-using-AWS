import json
import boto3
import urllib.request
from urllib.parse import quote

# Set up DynamoDB table
dynamodb = boto3.resource('dynamodb')
table_name = 'clinicaltrialdata'  # Replace with your actual DynamoDB table name

def lambda_handler(event, context):
    # Extract the path from the event
    path = event.get('path', '')
    
    # Handle the /status path
    if path == '/status':
        return {
            'statusCode': 200,
            'body': json.dumps("API is up and running.")
        }
    
    # Handle the /clinical-trials path for fetching and storing data
    elif path == '/clinical-trials':
        # Extract the condition from query parameters
        condition = event.get('queryStringParameters', {}).get('condition', 'Diabetes')  # Default to 'Diabetes'
        # Encode the condition for URL
        encoded_condition = quote(condition)
        
        url = f"https://clinicaltrials.gov/api/v2/studies?query.cond={encoded_condition}&pageSize=100"
        
        print(f"Fetching studies for condition: {condition}")  # Debug statement

        try:
            # Make the HTTP GET request using urllib
            with urllib.request.urlopen(url) as response:
                raw_data = response.read().decode()
                print("Raw data fetched from ClinicalTrials.gov:", raw_data)  # Print the raw data for debugging
                data = json.loads(raw_data)
        except urllib.error.URLError as e:
            return {
                'statusCode': 500,
                'body': json.dumps(f"Error fetching data from ClinicalTrials.gov: {str(e)}")
            }
        
        # Access the list of studies directly from the data
        studies = data.get("studies", [])
        
        if not studies:
            print("No studies found for the given condition.")  # Debug statement

        # Process and store each study in DynamoDB
        table = dynamodb.Table(table_name)
        
        for study in studies:
            study_data = study.get("protocolSection", {})
            study_id = study_data.get("identificationModule", {}).get("nctId", "N/A")
            title = study_data.get("identificationModule", {}).get("briefTitle", "N/A")
            phase = study_data.get("designModule", {}).get("phases", [])
            conditions = study_data.get("conditionsModule", {}).get("conditions", ["N/A"])
            condition = conditions[0] if conditions else "N/A"  # Take the first condition or default to "N/A"
            design_info = study_data.get("designModule", {}).get("designInfo", {})
            study_type = study_data.get("designModule", {}).get("studyType", "N/A")
            observation_model = design_info.get("observationModel", "N/A")
            intervention_model = design_info.get("interventionModel", "N/A")
            time_perspective = design_info.get("timePerspective", "N/A")

            # Print debugging information
            print(f"Processing study: ID={study_id}, Title={title}, Condition={condition}")
                # Add study design data to the item dictionary
            item = {
                    "studyid": study_id,
                    "title": title,
                    "phase": phase,
                    "condition": condition,
                    "design":design_info,
                    "study_type": study_type,
                    "observation_model": observation_model,
                    "intervention_model": intervention_model,
                    "time_perspective": time_perspective
                }
            # Store data in DynamoDB
            table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps(f"Fetched and stored {len(studies)} studies for condition: {condition}.")
        }
    
    # Default response for unsupported paths
    else:
        return {
            'statusCode': 404,
            'body': json.dumps("Error: Unsupported path.")
        }
