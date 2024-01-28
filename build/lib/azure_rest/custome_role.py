import requests, uuid

class CustomeRoleError(Exception):
    pass

def list_role(access_token, scope=None):
    '''
    This function is use to list the role assignment on scope or subsciption level 

    Args: 
        access_token (string): to authenticate the request
        scope (string)(optional): privide if want to list role on scope level

    Returns:
        Returns infromation about role in json format contanes name, id, allowed action, not allowed actions etc.
    '''
    if scope is None:
        list_custome_role = "https://management.azure.com/providers/Microsoft.Authorization/roleDefinitions?$filter=type+eq+'CustomRole'&api-version=2022-04-01"
    else:
        list_custome_role = f"https://management.azure.com/{scope}/providers/Microsoft.Authorization/roleDefinitions?$filter=type+eq+'CustomRole'&api-version=2022-04-01"

    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
    }

    try:
        response = requests.get(list_custome_role, headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as req_err:
        raise CustomeRoleError(f"Error during request: {req_err}")
    
    except ValueError as json_err:
        raise CustomeRoleError(f"Error decoding JSON response: {json_err}")
    
    except Exception as e:
        raise CustomeRoleError(f"Unexpected error: {e}")


def create_role(access_token, scope ,role_name, description, actions, assignableScopes, notActions=[]):
    '''
    Thes function will create a new custome role

    Args: 
        access_token (string): To authenticate the request
        scope (string): 
        role_name (string): name for role name
        description (string): short description about custome role created
        actions (list): add the actions that the role allows to be performed.
        assignableScope (list): list of scopes and groups
        notActions (list)(optional):  add the actions that are excluded from the allowed actions.

    Returns:
        Writen detailed information about newly created role in json
    '''
    roleDefinitionId = str(uuid.uuid4())
    
    create_role_endpoint = f'https://management.azure.com/{scope}/providers/Microsoft.Authorization/roleDefinitions/{roleDefinitionId}?api-version=2022-04-01'

    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
    }

    body = {
        "name": roleDefinitionId,
        "properties": {
            "roleName": role_name,
            "description": description,
            "type": "CustomRole",
            "permissions": [
            {
                "actions": actions,
                "notActions": notActions
            }
            ],
            "assignableScopes": assignableScopes
        }
    }

    try:
        response = requests.put(create_role_endpoint, headers=headers, json=body)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as req_err:
        raise CustomeRoleError(f"Error during request: {req_err}")
    
    except ValueError as json_err:
        raise CustomeRoleError(f"Error decoding JSON response: {json_err}")
    
    except Exception as e:
        raise CustomeRoleError(f"Unexpected error: {e}")

def update_role(access_token, scope ,role_name, description, roleDefinitionId, actions=[], assignableScopes=[], notActions=[]):
    '''
    This function will update the existing custome role 

    Args:
        access_token (string): To authenticate the request
        scope (string): 
        role_name (string): name for role name
        description (string): short description about custome role created
        roleDefinitionId (string): role definition id of wich you want to update
        actions (list): add the actions that the role allows to be performed.
        assignableScope (list): list of scopes and groups
        notActions (list)(optional):  add the actions that are excluded from the allowed actions.

    Returns:
        return the string as "Role updated successfuly"
    '''
    create_role_endpoint = f'https://management.azure.com/{scope}/providers/Microsoft.Authorization/roleDefinitions/{roleDefinitionId}?api-version=2022-04-01'

    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
    }

    body = {
        "name": roleDefinitionId,
        "properties": {
            "roleName": role_name,
            "description": description,
            "type": "CustomRole",
            "permissions": [
            {
                "actions": actions,
                "notActions": notActions
            }
            ],
            "assignableScopes": assignableScopes
        }
    }

    try:
        response = requests.put(create_role_endpoint, headers=headers, json=body)
        response = response.raise_for_status()
        return "Role updated successfuly"
    
    except requests.exceptions.RequestException as req_err:
        raise CustomeRoleError(f"Error during request: {req_err}")
    
    except ValueError as json_err:
        raise CustomeRoleError(f"Error decoding JSON response: {json_err}")
    
    except Exception as e:
        raise CustomeRoleError(f"Unexpected error: {e}")

def delete_role(access_token, scope, roleDefinitionId):
    '''
    Thes function delete the existing role

    Args: 
        access_token (string): To authenticate the request
        scope (string): 
        roleDefinitionId (string): role definition id of witch you want to delete

    Reterns:
        return information about deleted role 
    '''
    delete_role_endpoint = f'https://management.azure.com/{scope}/providers/Microsoft.Authorization/roleDefinitions/{roleDefinitionId}?api-version=2022-04-01'

    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
    }

    try:
        response = requests.delete(delete_role_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as req_err:
        raise CustomeRoleError(f"Error during request: {req_err}")
    
    except ValueError as json_err:
        raise CustomeRoleError(f"Error decoding JSON response: {json_err}")
    
    except Exception as e:
        raise CustomeRoleError(f"Unexpected error: {e}")
