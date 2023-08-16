import yaml
from pprint import pprint
from client import AdoClient

def Get_ADO_State(ADO_ID):
    # Get State
    work_items = AdoClient.get_work_item_client
    for i in work_items:
        if i.fields["System.Id"] == ADO_ID:
            State = i.fields["System.State"]
    return State

def Set_ADO_State(ADO_ID, State):
    # Get Current ADO State
    ADO_State = Get_ADO_State(ADO_ID)
    # Import mapping, to see if the state needs to be set

    # If needed, set the ADO state
    return "Success"

def Sync_gh_status_to_ADO_state(gh_ID,ADO_ID):
    # Get ADO item state
    ADO_state = Get_ADO_State(ADO_ID)
    # Get gh issue statues
    gh_status = get_gh_status(gh_ID)
    # Import the yaml to map state to status as a library
    mapping = yaml.load(open('StateMapping.yml', 'r'))

    # Use library to set ADO item status
    Set_ADO_State(ADO_ID, State)