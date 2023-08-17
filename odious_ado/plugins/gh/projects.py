import os
import pprint

import github

from odious_ado.settings import BaseConfig

from github import Github
import github3
from github3.projects import Project
import json

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


# PVT_kwDOB3mz7c4AUIpb


# "id": "PVTF_lADOB3mz7c4AUIpbzgM3PuM",
# "name": "Repository",
# "project": {
#     "id": "PVT_kwDOB3mz7c4AUIpb"
# }

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


    # {'organization': {'projectV2': {'id': 'PVT_kwDOB3mz7c4AUIpb'}}}
    # {'node': {'fields': {'nodes': [{'id': 'PVTF_lADOB3mz7c4AUIpbzgM3Ptw',
    #                                 'name': 'Title'},
    #                                {'id': 'PVTF_lADOB3mz7c4AUIpbzgM3Pt0',
    #                                 'name': 'Assignees'},
    #                                {'id': 'PVTSSF_lADOB3mz7c4AUIpbzgM3Pt4',
    #                                 'name': 'Status',
    #                                 'options': [{'id': 'f75ad846', 'name': 'Todo'},
    #                                             {'id': '47fc9ee4',
    #                                              'name': 'In Progress'},
    #                                             {'id': '98236657', 'name': 'Done'},
    #                                             {'id': '603cef85', 'name': 'pee'},
    #                                             {'id': 'a4bb9822',
    #                                              'name': 'poop'}]},
    #                                {'id': 'PVTF_lADOB3mz7c4AUIpbzgM3Pt8',
    #                                 'name': 'Labels'},
    #                                {'id': 'PVTF_lADOB3mz7c4AUIpbzgM3PuA',
    #                                 'name': 'Linked pull requests'},
    #                                {'id': 'PVTF_lADOB3mz7c4AUIpbzgM3PuI',
    #                                 'name': 'Reviewers'},
    #                                {'id': 'PVTF_lADOB3mz7c4AUIpbzgM3PuM',
    #                                 'name': 'Repository'},
    #                                {'id': 'PVTF_lADOB3mz7c4AUIpbzgM3PuQ',
    #                                 'name': 'Milestone'},
    #                                {'id': 'PVTF_lADOB3mz7c4AUIpbzgM5T2g',
    #                                 'name': 'asdfasdfasd'}]}}}

    dbd: list = []

    # for node in data["node"]["fields"]["nodes"]:
    #     if node.get("name", "").lower() == 'status':
    #         if node.get('name', "").lower() == 'title':
    #         # for opt in node.get('options', []):
    #         #     if opt.get('name', "").lower() == 'poop':
    #
    #                 pprint.pprint(node)
    #                 print('-------------------------------')
    #                 # pprint.pprint(opt)
    #
    #                 dbd.append({"project_id": project_id, "item_id": "35976933", "field_id": node['id'], "new_value": "death"})
    #     else:
    #         continue

    dbd.append(
        {"project_id": "PVT_kwDOB3mz7c4AUIpb",
         "item_id": "PVTI_lADOB3mz7c4AUIpbzgIm-CY",
         "field_id": "PVTSSF_lADOB3mz7c4AUIpbzgM3Pt4",
         "opt_id": "603cef85",
         # "field_id": "PVTF_lADOB3mz7c4AUIpbzgM3Ptw",
         "new_value": "death"
         }
    )

    # gh_client.

    # update_field(dbd)


    #      mutation ($project_id: ID! $item_id: ID! $field_id: ID!, $new_value: !String) {
    # o = auth.organization('nerds-run')

    # o.project(id=data.get("id"))
    # for p in o.projects():
    #     print(p)

    # a = auth.repository('nerds-run', 'odious-ado')

    # print(a.has_projects)
    # print(a.projects().as_dict)


    # print(a.projects().totalCount)
    # for z in iter(a.projects()):
    #     print(json.dumps(z.as_dict))
    # settings = BaseConfig.get_settings()
    #
    # repo = gh_client.get_repo(settings.GITHUB_REPOSITORY)
    # projects = repo.get_projects(state="open")
    # print(dir(projects))
    #
    # print(projects.totalCount)
    # org = gh_client.get_organization("nerds-run")
    #
    # n = org.get_projects(state="open")
    #
    #
    # p = gh_client.get_project(id=3)
    #
    #
    #
    #
    # print(n.totalCount)
    # print(dir(n.get_page))

    # for project in projects:
    #     print(project)



    # project = gh_client.get_project(id=2)

    # print(repo.get_projects(state="open").totalCount)
    # projects = repo.get_projects(state='open')
    #
    # for p in projects:
    #     print(p)

    # for c in blah.get_columns():
    #     print(c)

    # for col in project.get_columns():
    #     print(col)


    # print(project.get_columns)
    # print(repo.has_projects)




    # print(projects.totalCount)
    # return projects
    return project_id


def get_project(gh_client, project_id: int):
    settings = BaseConfig.get_settings()
    repo = gh_client.get_repo(settings.GITHUB_REPOSITORY)
    projects = repo.get_projects()

    return projects


# def some_bs(gh_client, dnd, ):
#     query = """
#     query IssueStatus($owner: String!, $repo: String!, $viewer: String!, $per_page: Int = 10) {
# 		repository(owner: $owner, name: $repo) {
# 			hasIssuesEnabled
# 			assigned: issues(filterBy: {assignee: $viewer, states: OPEN}, first: $per_page, orderBy: {field: UPDATED_AT, direction: DESC}) {
# 				totalCount
# 				nodes {
# 					...issue
# 				}
# 			}
# 			mentioned: issues(filterBy: {mentioned: $viewer, states: OPEN}, first: $per_page, orderBy: {field: UPDATED_AT, direction: DESC}) {
# 				totalCount
# 				nodes {
# 					...issue
# 				}
# 			}
# 			authored: issues(filterBy: {createdBy: $viewer, states: OPEN}, first: $per_page, orderBy: {field: UPDATED_AT, direction: DESC}) {
# 				totalCount
# 				nodes {
# 					...issue
# 				}
# 			}
# 		}
#     }`
#     """


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


    # single_select = """
    # mutation {
    #   updateProjectV2ItemFieldValue(
    #     input: {
    #       projectId: "PROJECT_ID"
    #       itemId: "ITEM_ID"
    #       fieldId: "FIELD_ID"
    #       value: {
    #         singleSelectOptionId: "OPTION_ID"
    #       }
    #     }
    #   )
    #   {
    #     projectV2Item {
    #      id
    #   }
    # }
    # """

  #   not_pretty = """
  #   mutation turtle {
  # updateProjectV2ItemFieldValue(
  #   input: {
  #     projectId: "PVT_kwDOB3mz7c4AUIpb"
  #     itemId: "PVTI_lADOB3mz7c4AUIpbzgIm-CY"
  #     fieldId: "PVTSSF_lADOB3mz7c4AUIpbzgM3Pt4"
  #     value: {
  #       singleSelectOptionId: "a4bb9822"
  #     }
  #   }
  # )
  # {
  #   projectV2Item {
  #    id
	# }
  # }}
  #
  #   """


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


    # response = requests.post(
    #     "https://api.github.com/graphql",
    #     json={"query": not_pretty},
    #     headers=headers,
    #     timeout=60,
    # )

    # pprint.pprint(response.json())

    # Check for errors in the GraphQL response
    # if response.status_code != 200 or "errors" in response.json():
    #     pprint.pprint(response.json())
    #
    #     raise ValueError("GraphQL query failed")
    #
    # data = response.json()["data"]

    # pprint.pprint(data)

    # id_thing = data['repository']['issue']['id']


    # esponse = requests.post(
    #     "https://api.github.com/graphql",
    #     json={"query": more_ghey},
    #     headers=headers,
    #     timeout=60,
    # )
    headers = {"Authorization": f"Bearer {BaseConfig.get_settings().GITHUB_ACCESS_TOKEN}"}
    pprint.pprint(dnd)

    for dumb in dnd:
        pprint.pprint(dumb)
        # Send the GraphQL request
        response = requests.post(
            "https://api.github.com/graphql",
            json={"query": ghey, "variables": dumb},
            headers=headers,
            timeout=60,
        )

        # Check for errors in the GraphQL response
        if response.status_code != 200 or "errors" in response.json():

            pprint.pprint(response.json())

            raise ValueError("GraphQL query failed")

        data = response.json()["data"]

        pprint.pprint(data)


#


# def add_issue_to_project():
#     q: str = """
#     mutation ($project_id: ID! $content_id: ID!) {
#         addProjectV2ItemById(
#             input: {
#                 projectId: $project_id contentId: $content_id}
#         )
#         {
#         item {
#             id
#         }
#     }
#     }
#     """
#     headers = {"Authorization": f"Bearer {BaseConfig.get_settings().GITHUB_ACCESS_TOKEN}"}
#
#     things = {
#         "project_id": "PVT_kwDOB3mz7c4AUIpb",
#         "content_id": "I_kwDOKHh5ys5ug85j"
#     }
#
#     response = requests.post(
#         "https://api.github.com/graphql",
#         json={"query": q, "variables": things},
#         headers=headers,
#         timeout=60,
#     )
#
#     # Check for errors in the GraphQL response
#     if response.status_code != 200 or "errors" in response.json():
#         pprint.pprint(response.json())
#
#         raise ValueError("GraphQL query failed")
#
#     data = response.json()["data"]
#
#
#     print("========================================================================================================")
#     pprint.pprint(data)
#
#     #PVTI_lADOB3mz7c4AUIpbzgIm - CY'P'addProjectV2ItemById': {'item': {'id': 'PVTI_lADOB3mz7c4AUIpbzgIm-CY'}}}






