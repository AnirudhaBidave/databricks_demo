import requests, uuid

class roleAssignmentError(Exception):
    pass

def assign_role(access_token, scope, roleDefinitionId, principalId):
    '''
    This function will assign custome or built-in role to user or groups

    Args: 
        access_token (string): to authenticate the request
        scope (string): scope at level to assign role
        roleDefinitionId (string): The fully qualified identifier of the role definition to be assigned.
        principalId (string): The unique identifier (object ID) of the user, group, 
                              or service principal to whom the role is being assigned.

    Returns:
        Return information about role assignment like properties ID name Etc in json format.
    '''

    roleAssignmentId = str(uuid.uuid4())

    assign_role_endpoint = f'https://management.azure.com/{scope}/providers/Microsoft.Authorization/roleAssignments/{roleAssignmentId}?api-version=2022-04-01'

    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
    }

    body = {
        "properties": {
            "roleDefinitionId": f"/{scope}/providers/Microsoft.Authorization/roleDefinitions/{roleDefinitionId}",
            "principalId": f"{principalId}"
        }
    }

    try:
        response = requests.put(assign_role_endpoint, headers=headers, json=body)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as req_err:
        raise roleAssignmentError(f"Error during request: {req_err}")
    
    except ValueError as json_err:
        raise roleAssignmentError(f"Error decoding JSON response: {json_err}")
    
    except Exception as e:
        raise roleAssignmentError(f"Unexpected error: {e}")
