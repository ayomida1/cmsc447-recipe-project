import datetime

import click

from .models import Credentials
from .navigator import Navigator
from .result import GradesListResult, render

today = datetime.date.today()


@click.group()
@click.option("--username", "-u", required=True, envvar="AXIOS_USERNAME")
@click.option("--password", "-p", required=True, envvar="AXIOS_PASSWORD")
@click.option(
    "--customer-id", "-id", required=True, envvar="AXIOS_CUSTOMER_ID"
)
@click.option("--student-id", required=True, envvar="AXIOS_STUDENT_ID")
@click.option(
    "--year",
    required=True,
    default=today.year if 9 <= today.month <= 12 else today.year - 1,
    envvar="AXIOS_STUDENT_YEAR",
)
@click.option(
    "--period",
    required=True,
    default="FT01" if today.month in [1, 9, 10, 11, 12] else "FT02",
    envvar="AXIOS_STUDENT_PERIOD",
)
@click.option(
    "--output-format",
    type=click.Choice(["json", "ndjson", "text"], case_sensitive=False),
    default="text",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enables verbose mode",
    default=False,
    envvar="AXIOS_VERBOSE",
)
@click.version_option()
@click.pass_context
def cli(
    ctx: click.Context,
    username: str,
    password: str,
    customer_id: str,
    student_id: str,
    year: int,
    period: str,
    output_format: str,
    verbose: bool,
):
    """Command line utility to access https://family.axioscloud.it"""
    ctx.ensure_object(dict)
    ctx.obj["username"] = username
    ctx.obj["password"] = password
    ctx.obj["customer_id"] = customer_id
    ctx.obj["student_id"] = student_id
    ctx.obj["year"] = year
    ctx.obj["period"] = period
    ctx.obj["output_format"] = output_format
    ctx.obj["verbose"] = verbose


@cli.command(name="login")
@click.pass_context
def login(ctx: click.Context):
    nav = Navigator(
        Credentials(
            username=ctx.obj["username"],
            password=ctx.obj["password"],
            customer_id=ctx.obj["customer_id"],
        ),
        student_id=ctx.obj["student_id"],
    )

    profile = nav.login()

    click.echo(
        f"Logged in as {profile.name} ({profile.customer_title} {profile.customer_name})"
    )


@cli.group()
def grades():
    pass


@grades.command(name="list")
@click.pass_context
def list_grades(ctx: click.Context):
    nav = Navigator(
        Credentials(
            username=ctx.obj["username"],
            password=ctx.obj["password"],
            customer_id=ctx.obj["customer_id"],
        ),
        student_id=ctx.obj["student_id"],
    )

    nav.login()
    nav.select_year(ctx.obj["year"])
    nav.select_period(ctx.obj["period"])

    click.echo(
        render(
            GradesListResult(nav.list_grades()),
            output_format=ctx.obj["output_format"],
        )
    )
