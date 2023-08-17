import yaml
# from pprint import pprint
from client import AdoClient
from azure.devops.v7_1.work_item_tracking.models import JsonPatchOperation

def get_ADO_state(ADO_ID:int):
    # Get State
    Connector = AdoClient()
    ADO_Item = Connector.get_work_item_by_id(ADO_ID)
    State = ADO_Item.fields["System.State"]
    return State

def set_ADO_state(ADO_ID, State):
    # Get Current ADO State
    ADO_State = get_ADO_state(ADO_ID)
    # If state is different, set state
    if ADO_State != State:
        # TODO: Check to make sure state is valid by loading the mapping
        # Set up update payload
        update_doc = [ 
            JsonPatchOperation(
                op="add",
                path="/fields/System.State",
                value=State,
            )
        ]
        Connector = AdoClient()
        Connector.set_work_item_by_id(ADO_ID, update_doc)
    return
