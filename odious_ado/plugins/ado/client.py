import os
import sys

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.work_item_tracking import WorkItemTrackingClient, CommentList, CommentCreate
from azure.devops.v7_1.work_item_tracking.models import Wiql
from azure.devops.v7_1.work_item_tracking.models import JsonPatchOperation

import pprint
# The following 2 lines are for Patrick to debug on his laptop.  Everyone else leave them commented out.  and yes, this is hella jank
#if "C:\\hackathon\\2023\\odious-ado" not in sys.path:
#   sys.path.append("C:\\hackathon\\2023\\odious-ado")
from odious_ado.settings import BaseConfig
# import odious_ado

class AdoClient:
    def __init__(self):

        settings = BaseConfig.get_settings()

        # Create a connection to the org
        self._credentials = BasicAuthentication('', settings.ADO_PAT)
        self._connection = Connection(base_url=settings.ADO_ORGANIZATION_URL, creds=self._credentials)

        # Get a client (the "core" client provides access to projects, teams, etc)
        self._core_client = self._connection.clients.get_core_client()
        self._work_item_client = WorkItemTrackingClient(
            base_url=f"{settings.ADO_ORGANIZATION_URL}",
            creds=self._credentials
        )

        # self._comments = CommentList(url="")

    @property
    def get_core_client(self):
        return self._core_client

    @property
    def get_work_item_client(self):
        # TODO: Change the following string formatting to not be less ass
        # TODO, this is currently broken, but I don't think we need to use it for our MVP, so abandoning in place
        wiql_query = f"""SELECT 
            [System.Id],
            [System.WorkItemType],
            [System.Title],
            [System.State],
            [System.Tags]
        FROM workitems
        WHERE
            [System.TeamProject] = '""" + os.getenv('OA_ADO_PROJECT_NAME', '') + """'
            AND [System.WorkItemType] IN ('User Story', 'Bug', 'Task')"""
        wit_client = self._connection.clients.get_work_item_tracking_client()
        query_wiql = Wiql(query=wiql_query)
        results = wit_client.query_by_wiql(query_wiql).work_items
        # Current issue is that while the results we get back are a list, if we want any useful information from them
        # beside IDs we need to iterate through the list here and grab the info we want to pass back up in a new list,
        # but it isn't working for some reason.  This is a very long comment

        # 2 different attempts at doing the above

        #work_items = []
        #for result in results:
        #    work_items.append[wit_client.get_work_items(int(result.id))]
        # work_items: list = (wit_client.get_work_items(int(result.id)) for result in results)
        return results
        
    def get_work_item_by_id(self,id:int):
        wit_client = self._connection.clients.get_work_item_tracking_client()
        work_item = wit_client.get_work_item(id)
        return work_item

    def set_work_item_by_id(self,id:int, update_package):
        wit_client = self._connection.clients.get_work_item_tracking_client()
        work_item = wit_client.update_work_item(update_package,id)
        return work_item
    # def get_comments(self):
    #     return self._comments

# def __get_aws_accounts():
#     client = boto3.client('organizations')
#
#     response = client.list_accounts()
#     aws_accounts: {str: str} = {}
#     for account in response.get('Accounts'):
#         if account.get('Status', 'suspended').lower() == 'active':
#             aws_accounts[account.get('Name')] = account.get('Id')
#
#     return aws_accounts