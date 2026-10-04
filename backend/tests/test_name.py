from datetime import date

from susiturkki.domain.birth import accepted_birth_year
from susiturkki.domain.name import display_name, require_given_name, split_name
from tests.conftest import at


def test_a_single_name_keeps_an_empty_family_name() -> None:
    assert split_name("Aino") == ("Aino", "")
    assert split_name("  Aino Korhonen ") == ("Aino", "Korhonen")
    assert display_name("Aino", "") == "Aino"
    assert display_name("Aino", "Korhonen") == "Aino Korhonen"


def test_given_name_is_required() -> None:
    assert require_given_name("  Aino ") == "Aino"
    assert _code(lambda: require_given_name("  ")) == "given_name_required"


def test_birth_year_stays_within_living_memory() -> None:
    assert accepted_birth_year(None, at(2026, 1, 1)) is None
    assert accepted_birth_year(2010, at(2026, 1, 1)) == 2010
    assert _code(lambda: accepted_birth_year(1899, at(2026, 1, 1))) == "birth_year_invalid"
    assert _code(lambda: accepted_birth_year(2027, at(2026, 1, 1))) == "birth_year_invalid"


def _code(call) -> str:
    try:
        call()
    except Exception as error:
        return error.code
    return ""
