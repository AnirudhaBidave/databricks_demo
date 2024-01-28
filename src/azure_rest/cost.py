import requests
import pandas as pd

class CostReportError(Exception):
    pass

def cost_rep(access_token, scope, granularity, filter_name, filter_value, type='ActualCost', timeframe= 'MonthToDate',sorting='descending', grouping='ResourceGroup', sort_by= 'Cost'):
    '''
    This function use Azure Cost Management API to programmatically access cost and usage 
    data for Azure resources 

    Args: 
        access_token (string): Access token to authenticat request
        scope (string): You can pass the scope at Subscription level or Resource Group level
        granularity (string): you can pass time granularity(PerHour / Daily / Weekly / Monthly)
        filter_name (string): filter_name for resource granularity(ResourceGroup / ResourceId etc)
        filter_value (string): filter_value ID or name of resource 
        type (string)(optional): type of cost data(ActualCost / Usage)
        timeFrame (string)(optional): time frame data
        sorting(string)(optional): sorting type (acending / desending)
        grouping(string)(optional): grouping by 
        sort_by(string)(optional): sorting by 

    Returns:
        DataFrame containing cost data in a structured format.
    '''
# url endpoint to request cost data in json format 
    cost_management_endpoint = f"https://management.azure.com/{scope}/providers/Microsoft.CostManagement/query?api-version=2023-11-01"
# header to authenticat request
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
    
# request payload with the filters, scope, granularity and sorting
    body =  {
        "type": type,
        "timeframe": timeframe, 
        "dataset": {
            "granularity": granularity,
            "aggregation": {
                "totalCost": {
                    "name": "Cost",
                    "function": "Sum"
                }
            },
            "sorting": [
                {
                    "direction": sorting,
                    "name": sort_by
                }
            ],
            "grouping": [
                {
                    "type": "Dimension",
                    "name": grouping
                },
            ],
            "filter": {
                "Dimensions": {
                    "name": filter_name,
                    "Operator": "In",
                    "values": filter_value
                },
            }
        }
    }
    
# requesting cost data with post method 
    try:
        response = requests.post(cost_management_endpoint, headers=headers, json=body)
        response.raise_for_status()
        response = response.json()

        json_data = response['properties']

        columns = [col["name"] for col in json_data["columns"]]

        df = pd.DataFrame(json_data["rows"], columns=columns)

        print(df)

    except requests.exceptions.RequestException as req_err:
        raise CostReportError(f"Error during request: {req_err}")
    
    except ValueError as json_err:
        raise CostReportError(f"Error decoding JSON response: {json_err}")
    
    except Exception as e:
        raise CostReportError(f"Unexpected error: {e}")
