import yaml
# from pprint import pprint
from odious_ado.plugins.ado.client import AdoClient
from azure.devops.v7_1.work_item_tracking.models import JsonPatchOperation

def get_ADO_effort(ADO_ID:int):
    # Get Effort
    Connector = AdoClient()
    ADO_Item = Connector.get_work_item_by_id(ADO_ID)
    Effort = ADO_Item.fields["Microsoft.VSTS.Scheduling.StoryPoints"]
    return Effort

def set_ADO_effort(ADO_ID, Effort):
    # Get Current ADO Effort
    ADO_Effort = get_ADO_effort(ADO_ID)
    # If Effort is different, set Effort
    if ADO_Effort != Effort:
        # Set up update payload
        update_doc = [ 
            JsonPatchOperation(
                op="add",
                path="/fields/Microsoft.VSTS.Scheduling.StoryPoints",
                value=Effort,
            )
        ]
        Connector = AdoClient()
        Connector.set_work_item_by_id(ADO_ID, update_doc)
    return