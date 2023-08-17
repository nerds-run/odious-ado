import yaml
from pprint import pprint
from client import AdoClient

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
        print("do things")
    return "Success"

print(Get_ADO_State(921938))
