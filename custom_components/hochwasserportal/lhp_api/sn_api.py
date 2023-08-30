"""The Länderübergreifendes Hochwasser Portal API - Functions for Sachsen."""

from __future__ import annotations
from collections import namedtuple
from .api_utils import fetch_soup
import datetime


def init_SN(ident):
    """Init data for Sachsen."""
    try:
        # Get data
        soup = fetch_soup(
            "https://www.umwelt.sachsen.de/umwelt/infosysteme/hwims/portal/web/wasserstand-uebersicht"
        )
        karte = soup.find_all("div", class_="karteWrapper")[0]
        link = karte.find_all("a", href="wasserstand-pegel-" + ident[3:])[0]
        # Parse data
        name = link.find_next("span", class_="popUpTitleBold").getText().strip()
        url = (
            "https://www.umwelt.sachsen.de/umwelt/infosysteme/hwims/portal/web/"
            + link["href"]
        )
        Initdata = namedtuple("Initdata", ["name", "url"])
        return Initdata(name, url)
    except Exception as err_msg:
        Initdata = namedtuple("Initdata", ["err_msg"])
        return Initdata(err_msg)


def parse_SN(ident):
    """Parse data for Sachsen."""
    try:
        # Get data
        soup = fetch_soup(
            "https://www.umwelt.sachsen.de/umwelt/infosysteme/hwims/portal/web/wasserstand-uebersicht"
        )
        karte = soup.find_all("div", class_="karteWrapper")[0]
        link = karte.find_all("a", href="wasserstand-pegel-" + ident[3:])[0]
        # Parse data
        if "meldePegel" in link.attrs["class"]:
            stage_colors = {
                "#b38758": 0,
                "#c5e566": 0,
                "#ffeb3b": 1,
                "#fb8a00": 2,
                "#e53835": 3,
                "#d400f9": 4,
            }
            data = link.find_next("div", class_="popUpStatus")
            try:
                color = data.attrs["style"].split()[-1]
                if color in stage_colors:
                    stage = stage_colors[color]
                else:
                    stage = None
            except:
                stage = None
        else:
            stage = None
        head = link.find_next("span", string="Wasserstand:")
        data = head.find_next("span", class_="popUpValue")
        try:
            level = float(data.getText().split()[0])
        except:
            level = None
        head = link.find_next("span", string="Durchfluss:")
        data = head.find_next("span", class_="popUpValue")
        try:
            flow = float(data.getText().split()[0].replace(",", "."))
        except:
            flow = None
        head = link.find_next("span", string="Datum:")
        data = head.find_next("span", class_="popUpValue")
        try:
            last_update = datetime.datetime.strptime(
                data.getText().strip().split()[0], "%d.%m.%Y%H:%M"
            )
        except:
            self.last_update = None
        Cyclicdata = namedtuple("Cyclicdata", ["level", "stage", "flow", "last_update"])
        return Cyclicdata(level, stage, flow, last_update)
    except Exception as err_msg:
        Cyclicdata = namedtuple("Cyclicdata", ["err_msg"])
        return Cyclicdata(err_msg)