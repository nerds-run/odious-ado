import os
import pprint

import github

from odious_ado.settings import BaseConfig


import github3
import requests


auth = github3.login(token=BaseConfig.get_settings().GITHUB_ACCESS_TOKEN)


ORG_QUERY:str = """
query($organization: String! $number: Int!){
    organization(login: $organization){
      projectV2(number: $number) {
        id
      }
    }
}
"""


def list_projects(gh_client):
    global auth

    whatever = {"organization": "nerds-run", "number": 3}

    # Remove the type:discussions filter from the search query
    # search_query = search_query.replace("type:discussions ", "")
    # Set the variables for the GraphQL query
    # variables = {"query": search_query}

    # Send the GraphQL request
    headers = {"Authorization": f"Bearer {BaseConfig.get_settings().GITHUB_ACCESS_TOKEN}"}

    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": ORG_QUERY, "variables": whatever},
        headers=headers,
        timeout=60,
    )

    # Check for errors in the GraphQL response
    if response.status_code != 200 or "errors" in response.json():
        pprint.pprint(response.json())

        raise ValueError("GraphQL query failed")

    data = response.json()["data"]

    pprint.pprint(data)

    project_id = data['organization']['projectV2']['id']
    more_bs: str = """
    query($project_id: ID!){  
        node(id: $project_id) {
        ... on ProjectV2 {
          fields(first: 20) {
            nodes { 
              ... on ProjectV2Field {
                id
                name
              }
              ... on ProjectV2IterationField {
                id
                name
                configuration {
                  iterations {
                    startDate
                    id
                  }
                }
              }
              ... on ProjectV2SingleSelectField {
                id
                name
                options {
                  id
                  name
                }
              }
            }
          }
        }
      }
    }
    """


    pprint.pprint(data['organization']['projectV2'])
    poo = {"project_id": project_id}
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": more_bs, "variables": poo},
        headers=headers,
        timeout=60,
    )

    # Check for errors in the GraphQL response
    if response.status_code != 200 or "errors" in response.json():
        pprint.pprint(response.json())

        raise ValueError("GraphQL query failed")

    data = response.json()["data"]

    pprint.pprint(data)

    return project_id


def get_project(gh_client, project_id: int):
    settings = BaseConfig.get_settings()
    repo = gh_client.get_repo(settings.GITHUB_REPOSITORY)
    projects = repo.get_projects()

    return projects


def update_field(dnd):
    # ($project_id: ID! $item_id: ID! $field_id: ID!)             fieldId: "PVTF_lADOB3mz7c4AUIpbzgM3Ptw"  $field_id: ID!
    # optionId: $opt_id  $opt_id: ID!
    ghey: str = """
    mutation  ($project_id: ID! $field_id: ID! $item_id: ID! $new_value: String!)  {
        updateProjectV2ItemFieldValue(
          input: {
            projectId: $project_id
            itemId: $item_id
            fieldId: $field_id
            value: {
                text: $new_value
            }
          }
        ) {
          projectV2Item {
            id
          }
        }
      }
    """
    # 'options': [{'id': 'f75ad846', 'name': 'Todo'},
    #             {'id': 'a4bb9822', 'name': 'poop'},
    #             {'id': '603cef85', 'name': 'pee'},
    #             {'id': '47fc9ee4',
    #              'name': 'In Progress'},
    #             {'id': '98236657',
    #              'name': 'Done'}]},

    not_pretty = """
    mutation turtle {
        updateProjectV2ItemFieldValue(
        input: { 
            projectId: "PVT_kwDOB3mz7c4AUIpb"
            itemId: "PVTI_lADOB3mz7c4AUIpbzgIn0Oo"
            fieldId: "PVTSSF_lADOB3mz7c4AUIpbzgM3Pt4"
            value: {

              singleSelectOptionId: "a4bb9822"
           }
        }
    )
    {
        projectV2Item {
            id
        }
    }
    }

    """


    # more_ghey: str = """
    # mutation AddReactionToIssue {
    #     addReaction(input:{subjectId:"I_kwDOKHh5ys5ug85j",content:HOORAY}) {
    #         reaction {
    #             content
    #         }
    #         subject {
    #             id
    #         }
    #     }
    # }
    # """
    # value: {
    #   iterationId: $iteration_id
    # }
    # gh
    # api
    # graphql - f
    # query = 'p
    # mutation
    # {
    #     updateProjectV2ItemFieldValue(
    #         input: {
    #         projectId: "PROJECT_ID"
    #         itemId: "ITEM_ID"
    #         fieldId: "FIELD_ID"
    #         value: {
    #             text: "Updated text"
    #         }
    #     }
    # ) {
    #     projectV2Item
    # {
    #     id
    # }
    # }
    # }'
    # add_issue_to_project()
    # headers = {"Authorization": f"Bearer {BaseConfig.get_settings().GITHUB_ACCESS_TOKEN}"}
    # aaaaa = """
    # query FindIssueID {
    #     repository(owner:"nerds-run", name:"odious-ado") {
    #         issue(number:26) {
    #             id
    #         }
    #     }
    # }
    # """

    headers = {"Authorization": f"Bearer {BaseConfig.get_settings().GITHUB_ACCESS_TOKEN}"}
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": not_pretty},
        headers=headers,
        timeout=60,
    )

    pprint.pprint(response.json())

    # Check for errors in the GraphQL response
    if response.status_code != 200 or "errors" in response.json():
        pprint.pprint(response.json())

        raise ValueError("GraphQL query failed")

    data = response.json()["data"]

    pprint.pprint(data)
