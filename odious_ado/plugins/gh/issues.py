import os
from pprint import pprint
from github import Github
import requests

from odious_ado.settings import BaseConfig


def apply_labels(gh_client, *args):
    settings = BaseConfig.get_settings()
    issues = gh_client.get_repo(settings.GITHUB_REPOSITORY).get_issues()

    for issue in issues:
        for a in args:
            apply_label(issue, a)


def apply_label(issue, label: str):
    issue.add_to_labels(f"{label}")


# f"{settings.ADO_ORG_ID}/{settings.ADO_ORG_ID}"

def get_issues(gh_client):
    settings = BaseConfig.get_settings()
    repo = gh_client.get_repo(settings.GITHUB_REPOSITORY)

    return repo.get_issues()


def get_i_issues(**kwargs):
    query = """
    query  new_issues ($organization: String!, $repository_name: String!) {
      repository(owner: $organization, name: $repository_name) {
        issues(last:20, states:OPEN) {
          edges {
            node {
              id
              title
              url
              labels(first:5) {
                edges {
                  node {
                    id
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
    """

    headers = {"Authorization": f"Bearer {BaseConfig.get_settings().GITHUB_ACCESS_TOKEN}"}
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": kwargs},
        headers=headers,
        timeout=60,
    )
    # Check for errors in the GraphQL response
    if response.status_code != 200 or "errors" in response.json():
        pprint(response.json())

        raise ValueError("GraphQL query failed")

    data = response.json()["data"]

    return data


def get_i_issue_ids(**kwargs):
    data = get_i_issues(**kwargs)
    why_does_graphql_suck = [i.get('id') for n in data['repository']['issues']['edges'] for i in n.values()]
    return why_does_graphql_suck


def get_issue_by_id(issues_is: str):
    pass


def create_labels(gh_client, labels: dict):
    """

    :param gh_client:
    :param labels:
    :return:
    """
    issues = get_issues(gh_client)

    for issue in issues:
        issue.edit(state="New")


def find_issue_by_number(**kwargs):
    # TODO name these like a normal human
    query: str = """
    query FindIssueID ($owner: String! $name: String! $issue_number: String!) {
        repository(owner: $owner, name: $name) {
            issue(number: $issue_number) {
                id
            }
        }
    }
    """
    headers = {"Authorization": f"Bearer {BaseConfig.get_settings().GITHUB_ACCESS_TOKEN}"}
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": kwargs},
        headers=headers,
        timeout=60,
    )

    # Check for errors in the GraphQL response
    if response.status_code != 200 or "errors" in response.json():
        pprint(response.json())

        raise ValueError("GraphQL query failed")

    data = response.json()["data"]

    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    pprint(data)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


def change_issue_status(**kwargs):
    query: str = """
    mutation ($project_id: ID! $item_id: ID! $field_id: ID! $opt_id: ID!) {
      updateProjectV2ItemFieldValue(
        input: {
          projectId: $project_id
          itemId: $item_id
          fieldId: $field_id
          value: { 
            singleSelectOptionId: $opt_id        
          }
        }
      )
      {
        projectV2Item {
         id
      }
    }
    """
    headers = {"Authorization": f"Bearer {BaseConfig.get_settings().GITHUB_ACCESS_TOKEN}"}
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": kwargs},
        headers=headers,
        timeout=60,
    )

    # Check for errors in the GraphQL response
    if response.status_code != 200 or "errors" in response.json():
        pprint(response.json())

        raise ValueError("GraphQL query failed")

    data = response.json()["data"]

    print("---------------------------------------------------------------------------------------------------------")
    pprint(data)
    print("---------------------------------------------------------------------------------------------------------")


def add_issue_to_project(append_label: bool = False, **kwargs):
    query: str = """
    mutation ($project_id: ID! $content_id: ID!) {
        addProjectV2ItemById(
            input: {
                projectId: $project_id contentId: $content_id
            }
        ) 
        {
            item {
                id
                type
                databaseId
            }
        }
    }
    """
    headers = {"Authorization": f"Bearer {BaseConfig.get_settings().GITHUB_ACCESS_TOKEN}"}

    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": kwargs},
        headers=headers,
        timeout=60,
    )

    # Check for errors in the GraphQL response
    if response.status_code != 200 or "errors" in response.json():
        pprint(response.json())

        raise ValueError("GraphQL query failed")

    data = response.json()["data"]

    print("========================================================================================================")
    pprint(data)
    print("========================================================================================================")

    return data['addProjectV2ItemById']['item']['databaseId'], data['addProjectV2ItemById']['item']['id']


def reaction_silliness(**kwargs):
    query: str = """
    mutation AddReactionToIssue {
        addReaction(input:{subjectId:"I_kwDOKHh5ys5ug85j",content:HOORAY}) {
            reaction {
                content
            }
            subject {
                id
            }
        }
    }
    """
    pass


def issues_with_database_index():
    settings = BaseConfig.get_settings()
    query: str = """
    query ($owner: String! $name: String!) {
      repository(owner: $owner, name: $name) {
        issues(states:OPEN, first: 50) {
          edges {
            node {
              id
              databaseId
              number
              projectCards {
                edges {
                  node {
                    id
                  }
                }
              }
    
              title
              url
              labels (first:50) {
                edges {
                  
                  node {
                    id
                    issues (first: 50) {
                      edges {
                        node {
                          id
                          number
                          databaseId
                            repository {
                                id
                            }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """

    headers = {"Authorization": f"Bearer {BaseConfig.get_settings().GITHUB_ACCESS_TOKEN}"}
    org, repo = settings.GITHUB_REPOSITORY.split('/')
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": {"owner": org, "name": repo}},
        headers=headers,
        timeout=60,
    )

    # Check for errors in the GraphQL response
    if response.status_code != 200 or "errors" in response.json():
        pprint(response.json())

        raise ValueError("GraphQL query failed")

    much = {}
    data = response.json()['data']['repository']['issues']['edges']
    for n in data:
        much[n['node']['databaseId']] = n['node']

    return much
