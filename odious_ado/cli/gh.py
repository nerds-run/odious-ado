import csv
import json
import os

import click
from github import Github

from odious_ado.settings import BaseConfig


###
# Github Sub Commands
###
@click.group()
@click.pass_context
def github(ctx):
    """
    Github utility commands
    """
    settings = BaseConfig.get_settings()
    ctx.ensure_object(dict)
    ctx.obj['client']: Github = Github(settings.GITHUB_ACCESS_TOKEN)

    pass


@github.command('pull-request-comment')
@click.pass_context
def pull_request_comment(ctx):
    repo = ctx.obj['client'].get_repo('nerds-run/odious-ado')

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
    pass


@github.group()
@click.argument('org_name', metavar="Required: <Github Organization Name>",  nargs=1, required=True)
@click.pass_context
def org(ctx, org_name: str):
    """
    Github Organization utilities
    """
    ctx.obj['organization'] = ctx.obj['client'].get_organization(org_name)

    pass


@org.group()
@click.pass_context
def members(ctx):
    """
    Github organization member utilities
    """
    ctx.obj['members'] = ctx.obj['organization'].get_members()
    pass


@members.command('ls')
@click.option(
    '--csv',
    'csv_',
    is_flag=True,
    help="The export option only supports csv."
)
@click.pass_context
def ls(ctx, csv_: bool):
    """
    List the members of the Github organization. Can be exported to CSV.
    """
    users: [{str: str}] = []
    with click.progressbar(ctx.obj['members'], label="retrieving organization's members") as items:
        for m in items:
            users.append({
                'login': m.login,
                'email': m.email,
                'created_at': str(m.created_at),
                'updated_at': str(m.updated_at)
            })

    if csv_ is True:
        csv.register_dialect('excel', delimiter=',', quoting=csv.QUOTE_NONE)
        with open('github_members.csv', 'w', newline='') as csv_file:
            header_values: [str] = ['login', 'email', 'created_at', 'updated_at']
            csv_writer = csv.DictWriter(csv_file, fieldnames=header_values)
            csv_writer.writeheader()

            for user in users:
                csv_writer.writerow(user)
    else:
        click.echo(json.dumps(users))

