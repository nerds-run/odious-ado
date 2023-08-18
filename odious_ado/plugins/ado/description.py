import yaml
# from pprint import pprint
from client import AdoClient
from azure.devops.v7_1.work_item_tracking.models import JsonPatchOperation


def get_ADO_item_type(ADO_ID:int):
    Connector = AdoClient()
    ADO_Item = Connector.get_work_item_by_id(ADO_ID)
    work_item_type = ADO_Item.fields["System.WorkItemType"]
    return work_item_type


def get_ADO_description(ADO_ID:int):
    # Check item type
    item_type = get_ADO_item_type(ADO_ID)
    if item_type != 'User Story':
        return "Description only exists on Stories"
    # Get Description
    Connector = AdoClient()
    ADO_Item = Connector.get_work_item_by_id(ADO_ID)
    description = ADO_Item.fields["System.Description"]
    return description


def set_ADO_description(ADO_ID, State):
    item_type = get_ADO_item_type(ADO_ID)
    if item_type != 'User Story':
        return
    # Get Current ADO State
    ADO_description = get_ADO_description(ADO_ID)
    # If state is different, set state
    update_doc = [ 
        JsonPatchOperation(
            op="add",
            path="/fields/System.Description",
            value=State,
        )
    ]
    Connector = AdoClient()
    Connector.set_work_item_by_id(ADO_ID, update_doc)
    return
