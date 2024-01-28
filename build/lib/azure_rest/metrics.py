import requests
from datetime import datetime, timedelta
import pandas as pd


class metrics_Error(Exception):
    pass

def res_metrics(access_token, scope, resource_info, metricNames, hours=None, days=None):
    '''
    This function will return metrics of resourses using the azure rest api

    Args: 
        access_token (string): Access token to authenticat request
        scope (string): You can pass the scope at Resource Group level
        resource_info (list): list resoure info [resourceProviderNamespace, resourceType, resourceName]
        metricName (string): type of metrics data (Transactions / Ingress / Egress)
        hours (int)(optional): number of hours (optional if days are provided)
        days (int): number of days (optional if hours are provided)

    Returns:
        It will return resource metrics with passed parameters in json format
    '''
# Condition to createa timr frame with hours granularity
    if hours is not None:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        start_time_str = start_time.isoformat() + "Z"
        end_time_str = end_time.isoformat() + "Z"
        timeRange = start_time_str + "/" + end_time_str
# condition to createa time frame with days granularity
    elif days is not None:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)
        start_time_str = start_time.isoformat() + "Z"
        end_time_str = end_time.isoformat() + "Z"
        timeRange = start_time_str + "/" + end_time_str

# extracting resource information from list
    resourceProviderNamespace = resource_info[0]
    resourceType = resource_info[1]
    resourceName = resource_info[2]
# headers to authenticat request 
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
# azure metrics url endpoint 
    metrics_url = f"https://management.azure.com/{scope}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}/providers/microsoft.insights/metrics?api-version=2018-01-01&metricnames={metricNames}&timespan={timeRange}"
# requesting response with get method 
    try:
        metrics_response = requests.get(metrics_url, headers=headers)
        metrics_response.raise_for_status()
        metrics_response = metrics_response.json()
        
        timeSpan = metrics_response['timespan']
        metricsType = metrics_response['value'][0]['name']['value']
        description = metrics_response['value'][0]['displayDescription']
        json_data = metrics_response['value'][0]['timeseries'][0]['data']

        df = pd.DataFrame(json_data)

        df['timeStamp'] = pd.to_datetime(df['timeStamp'])

        df_filtered = df[df['total'] != 0]

        return(f'resourceType: {resourceType}'+'\n'+f'resourceName: {resourceName}'+'\n'+f'Time span: {timeSpan}'+'\n'+f'Metrics type: {metricsType}'+'\n'+f'Description: {description}'+'\n'+f'{df_filtered}')
    
    except requests.exceptions.RequestException as req_err:
        raise metrics_Error(f"Error during request: {req_err}")
    
    except ValueError as json_err:
        raise metrics_Error(f"Error decoding JSON response: {json_err}")
    
    except Exception as e:
        raise metrics_Error(f"Unexpected error: {e}")
