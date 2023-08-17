import yaml
# from pprint import pprint
from client import AdoClient
from azure.devops.v7_1.work_item_tracking.models import JsonPatchOperation

def Get_ADO_State(ADO_ID:int):
    # Get State
    Connector = AdoClient()
    ADO_Item = Connector.get_work_item_by_id(ADO_ID)
    State = ADO_Item.fields["System.State"]
    return State

def Set_ADO_State(ADO_ID, State):
    # Get Current ADO State
    ADO_State = Get_ADO_State(ADO_ID)
    # If needed, set the ADO state
    if ADO_State != State:
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
        print("Success!")
    return

print(Get_ADO_State(921938))
Set_ADO_State(921938, "Resolved")
print(Get_ADO_State(921938))