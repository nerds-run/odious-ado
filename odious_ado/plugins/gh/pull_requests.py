import os
from github import Github
from odious_ado.settings import BaseConfig


def get_client():
    """
    """
    settings = BaseConfig.get_settings()

    client = Github(settings.GITHUB_ACCESS_TOKEN)

    return client


def pull_request_comment(client) -> str:
    repo = client.get_repo('nerds-run/odious-ado')

    pr = repo.get_pull(1)

    print(f"Pull Request: {pr.review_comments} Merge Commit ID: {pr.merge_commit_sha}")

    plan_output = """
        Odious ADO to the rescue!
    """

    # ${{steps.terraform_validate.outputs.stdout}}
    msg: str = f"""<h4>What will this header be 🖌 what will this value be</h4>
    <h4>Initialization ⚙️ starting up</h4>
    <h4>Validation 🤖 something goes here</h4>
    <h4>Plan 📖 `${{ pr.user.login }}`</h4>
    <details>
    <summary>Show Summary</summary>
    ```
    { plan_output }
    ```
    </details>
    <b>Pusher: @{ pr.user.login }, event: `${{ github.event_name }}`, Working Directory: `{os.getcwd()}`, Pull Request State: `{ pr.state }`</b>
    """

    pr.create_issue_comment(msg)

    return msg
