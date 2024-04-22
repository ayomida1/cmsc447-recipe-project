from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, List

import requests
from lxml import html

from .models import Credentials, Grade, Profile

START_URL = "https://family.axioscloud.it/Secret/REStart.aspx?Customer_ID="
FAMILY_URL = "https://family.axioscloud.it/Secret/REFamily.aspx"

today = date.today()


@dataclass
class State:
    """State in an ASP.NET web application."""

    year: int
    period: str
    student_id: str

    viewstate: str = ""
    viewstategenerator: str = ""
    eventvalidation: str = ""

    def update_from(self, tree: html.HtmlElement):
        """Merge the state from a new tree."""
        self.viewstate = tree.xpath('//input[@id="__VIEWSTATE"]/@value')
        self.viewstategenerator = tree.xpath(
            '//input[@id="__VIEWSTATEGENERATOR"]/@value'
        )
        self.eventvalidation = tree.xpath(
            '//input[@id="__EVENTVALIDATION"]/@value'
        )


class Navigator:
    """Navigator for the Axios Family web application."""

    def __init__(
        self,
        credentials: Credentials,
        student_id: str,
        verbose: bool = False,
    ):
        self.credentials = credentials
        self.state = State(
            year=today.year if 9 <= today.month <= 12 else today.year - 1,
            period="FT01" if 9 < today.month < 2 else "FT02",
            student_id=student_id,
        )
        self.session = requests.Session()
        self.verbose = verbose

    def login(self) -> Profile:
        """Login to the Axios Family web application."""

        start_url = START_URL + self.credentials.customer_id

        # Get the login page
        resp = self.session.get(start_url)
        self.state.update_from(html.fromstring(resp.text))

        start_payload = {
            "__VIEWSTATE": self.state.viewstate,
            "__VIEWSTATEGENERATOR": self.state.viewstategenerator,
            "__EVENTVALIDATION": self.state.eventvalidation,
            "ibtnRE.x": 0,
            "ibtnRE.y": 0,
            "mha": "",
        }

        # I don't know why we need to do this is, but it's required
        resp = self.session.post(
            start_url, data=start_payload, headers=headers_for(start_url)
        )
        tree = html.fromstring(resp.text)
        self.state.update_from(tree)

        login_payload = {
            "__LASTFOCUS": "",
            "__EVENTTARGET": "",
            "__VIEWSTATE": self.state.viewstate,
            "__VIEWSTATEGENERATOR": self.state.viewstategenerator,
            "__EVENTVALIDATION": self.state.eventvalidation,
            "txtImproveDone": "",
            "txtUser": self.credentials.username,
            "txtPassword": self.credentials.password,
            "btnLogin": "Accedi",
        }

        # does the actual login
        resp = self.session.post(
            "https://family.axioscloud.it/Secret/RELogin.aspx",
            data=login_payload,
            headers=headers_for(start_url),
        )

        tree = html.fromstring(resp.text)
        self.state.update_from(tree)

        # look for the user name in the page, if it's not there,
        # we're not logged in
        name = tree.xpath('//span[@id="lblUserName"]')
        if not name:
            raise Exception("Login failed")

        customer_title = tree.xpath('//span[@id="lblCustomerTitle"]')
        customer_name = tree.xpath('//span[@id="lblCustomerName"]')

        return Profile(
            self.credentials.customer_id,
            name[0].text,
            customer_title[0].text,
            customer_name[0].text,
        )

    def list_grades(self) -> List[Grade]:
        """List the grades for the logged-in user."""

        payload = {
            "__LASTFOCUS": "",
            "__EVENTTARGET": "FAMILY",
            "__EVENTARGUMENT": "RED",
            "__VIEWSTATE": self.state.viewstate,
            "__VIEWSTATEGENERATOR": self.state.viewstategenerator,
            "__EVENTVALIDATION": self.state.eventvalidation,
            "ctl00$ContentPlaceHolderMenu$ddlAnno": self.state.year,
            "ctl00$ContentPlaceHolderMenu$ddlFT": self.state.period,
            "ctl00$ContentPlaceHolderBody$txtDataSelezionataCAL": today.strftime(
                "%d/%m/%Y"
            ),
            "ctl00$ContentPlaceHolderBody$txtFunctionSelected": "nothing",
            "ctl00$ContentPlaceHolderBody$txtAluSelected": self.state.student_id,
            "ctl00$ContentPlaceHolderBody$txtIDAluSelected": "0",
        }

        if self.verbose:
            print(payload)

        resp = self.session.post(
            FAMILY_URL,
            data=payload,
            headers=headers_for(FAMILY_URL),
        )

        tree = html.fromstring(resp.text)
        self.state.update_from(tree)

        rows = tree.xpath('//div[@id="votiEle"]/div/table/tbody/tr')
        grades = []
        for row in rows:
            grades.append(
                Grade(
                    date=datetime.strptime(
                        first(row.xpath("td[1]/text()")), "%d/%m/%Y"
                    ),
                    subject=first(row.xpath("td[2]/text()")),
                    kind=first(row.xpath("td[3]/text()")),
                    value=first(row.xpath("td[4]/span/text()")),
                    # target=first(row.xpath("td[5]/text()")),
                    comment=first(row.xpath("td[6]/text()")),
                    teacher=first(row.xpath("td[7]/text()")),
                )
            )

        return grades

    def select_student(self, student_id: str) -> None:
        """Select the student"""
        self.state.student_id = student_id

    def select_year(self, year: int, day=None) -> None:
        """Select the year"""
        day = day or date.today()
        if self.state.year == year:
            if self.verbose:
                print(
                    "optimization: year is unchanged, we can avoid making a network call"
                )
            return

        self.state.year = year

        payload = {
            "__LASTFOCUS": "",
            "__EVENTTARGET": "ctl00$ContentPlaceHolderMenu$ddlAnno",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": self.state.viewstate,
            "__VIEWSTATEGENERATOR": self.state.viewstategenerator,
            "__EVENTVALIDATION": self.state.eventvalidation,
            "ctl00$ContentPlaceHolderMenu$ddlAnno": self.state.year,
            "ctl00$ContentPlaceHolderMenu$ddlFT": self.state.period,
            "ctl00$ContentPlaceHolderBody$txtDataSelezionataCAL": day.strftime(
                "%d/%m/%Y"
            ),
            "ctl00$ContentPlaceHolderBody$txtFunctionSelected": "nothing",
            "ctl00$ContentPlaceHolderBody$txtAluSelected": self.state.student_id,
            "ctl00$ContentPlaceHolderBody$txtIDAluSelected": "0",
        }

        resp = self.session.post(
            FAMILY_URL,
            data=payload,
            headers=headers_for(FAMILY_URL),
        )

        tree = html.fromstring(resp.text)
        self.state.update_from(tree)

    def select_period(self, period: str) -> None:
        """Select the period"""

        if self.verbose:
            print("select_period", period)
        self.state.period = period

        payload = {
            "__LASTFOCUS": "",
            "__EVENTTARGET": "ctl00$ContentPlaceHolderMenu$ddlFT",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": self.state.viewstate,
            "__VIEWSTATEGENERATOR": self.state.viewstategenerator,
            "__EVENTVALIDATION": self.state.eventvalidation,
            "ctl00$ContentPlaceHolderMenu$ddlAnno": self.state.year,
            "ctl00$ContentPlaceHolderMenu$ddlFT": self.state.period,
            "ctl00$ContentPlaceHolderBody$txtDataSelezionataCAL": today.strftime(
                "%d/%m/%Y"
            ),
            "ctl00$ContentPlaceHolderBody$txtFunctionSelected": "nothing",
            "ctl00$ContentPlaceHolderBody$txtAluSelected": self.state.student_id,
            "ctl00$ContentPlaceHolderBody$txtIDAluSelected": "0",
        }

        resp = self.session.post(
            FAMILY_URL,
            data=payload,
            headers=headers_for(FAMILY_URL),
        )

        tree = html.fromstring(resp.text)
        self.state.update_from(tree)


def first(sequence, default_value: Any = ""):
    return sequence[0] if sequence else default_value


def headers_for(url: str) -> dict:
    return {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://family.axioscloud.it",
        "Referer": url,
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    }
