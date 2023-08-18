import csv
import json
from pprint import pprint
import os

import click
from github import Github
from tabulate import tabulate

from odious_ado.settings import BaseConfig
from odious_ado.plugins import gh


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


@github.group("issues")
@click.pass_context
def issues(ctx):
    pass


@issues.command("ls")
@click.pass_context
def ls(ctx):
    settings = BaseConfig.get_settings()
    project_issues = gh.get_issues(ctx.obj['client'])

    for issue in project_issues:

        pprint(f"{issue.title} -- {issue.id}")


@issues.group("labels")
@click.pass_context
def issue_labels(ctx):
    pass


@issue_labels.command("apply")
@click.pass_context
def apply_labels(ctx):
    settings = BaseConfig.get_settings()
    issues = gh.get_issues(ctx.obj['client'])
    for issue in issues:
        # issue.
        issue.add_to_labels(f"{settings.ADO_ORG_ID}/{settings.OA_ADO_PROJECT_NAME}")


@issue_labels.command("sync")
@click.pass_context
def sync_labels(ctx):
    settings = BaseConfig.get_settings()
    client = ctx.obj['client']

    labels: dict = {
        "New": None,
        "Approved": "Todo",
        "Active": "In Progress",
        "Resolved": "Done",
        "Committed": "Todo",
        "Done": "Done",
        "Blocked": "In Progress",
        "Accepted": "Todo",
        "Closed": "Done",
        "Removed": None,
        "Archived": None
    }

    gh.create_labels(client, labels=labels)


@issues.command("status")
@click.option(
    "-u",
    "--update",
    help="update issues status in gh projects and ado",
    default=None,
    required=False,
    type=bool,
)
@click.pass_context
def issues_status(ctx, update: bool = False):
    settings = BaseConfig.get_settings()

    project_list = gh.list_projects(ctx.obj.get('client'))
    gh_org, repo = settings.GITHUB_REPOSITORY.split('/')
    gh_issues = gh.get_i_issues(organization=gh_org, repository_name=repo)

    pprint(project_list)
    print("-==-=--=-========-=-=-=-")
    pprint(gh_issues)
    print("-==-=--=-========-=-=-=-")
    # gh.change_issue_status(project_id="", item_id="", field_id="", opt_id="")


@github.group("projects")
@click.pass_context
def projects(ctx):
    pass


@projects.command("ls")
@click.pass_context
def ls(ctx):
    settings = BaseConfig.get_settings()
    _projects = gh.list_projects(ctx.obj['client'])

    if _projects is None:
        click.echo("No projects found.", color=True)
    else:
        for project in _projects:
            pprint(f"{projects.name} -- {project.id}")


@projects.command("sync")
@click.pass_context
def add_issues_to_project(ctx):
    client = ctx.obj.get('client')
    settings = BaseConfig.get_settings()
    gh_org, repo = settings.GITHUB_REPOSITORY.split('/')
    gh_issue_ids = gh.get_i_issue_ids(organization=gh_org, repository_name=repo)
    project_id = gh.list_projects(client)

    for issue_id in gh_issue_ids:
        gh.add_issue_to_project(project_id=project_id, content_id=issue_id)
        # gh.apply_label()
        # gh.apply_label(client, project_id, item_id=issue_id)


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

