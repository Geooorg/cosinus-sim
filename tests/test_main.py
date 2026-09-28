from colorama import Fore, Style

from main import faerbe_raster


def test_faerbe_raster_faerbt_bekannte_symbole():
    raster = ["--+--", "..*..", "..o.."]
    gefaerbt = faerbe_raster(raster)
    assert gefaerbt[1] == f"..{Fore.RED}*{Style.RESET_ALL}.."
    assert gefaerbt[2] == f"..{Fore.BLUE}o{Style.RESET_ALL}.."


def test_faerbe_raster_laesst_achsen_und_leerzeichen_unveraendert():
    raster = ["--+--", "..*.."]
    gefaerbt = faerbe_raster(raster)
    assert gefaerbt[0] == "--+--"


def test_faerbe_raster_faerbt_ueberlappung_und_labels():
    raster = ["..X..", "..A..", "..B.."]
    gefaerbt = faerbe_raster(raster)
    assert gefaerbt[0] == f"..{Fore.MAGENTA}X{Style.RESET_ALL}.."
    assert gefaerbt[1] == f"..{Fore.RED}A{Style.RESET_ALL}.."
    assert gefaerbt[2] == f"..{Fore.BLUE}B{Style.RESET_ALL}.."
