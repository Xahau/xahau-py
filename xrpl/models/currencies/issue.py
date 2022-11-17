"""
Specifies an Issue.
This format is used for AMM and sidechain requests.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from xrpl.constants import HEX_CURRENCY_REGEX, ISO_CURRENCY_REGEX
from xrpl.models.base_model import BaseModel
from xrpl.models.required import REQUIRED
from xrpl.models.utils import require_kwargs_on_init


def _is_valid_currency(candidate: str) -> bool:
    return bool(
        ISO_CURRENCY_REGEX.fullmatch(candidate)
        or HEX_CURRENCY_REGEX.fullmatch(candidate)
    )


@require_kwargs_on_init
@dataclass(frozen=True)
class Issue(BaseModel):
    """
    Specifies an Issue.
    This format is used for AMM and sidechain requests.
    """

    currency: str = REQUIRED  # type: ignore
    """
    This field is required.

    :meta hide-value:
    """

    issuer: Optional[str] = None
    """
    The issuer of the currency. None if XRP is currency.
    """

    def _get_errors(self: Issue) -> Dict[str, str]:
        errors = super()._get_errors()
        if self.issuer is not None and self.currency.upper() == "XRP":
            errors["currency"] = "Currency must not be XRP when issuer is set"
        elif not _is_valid_currency(self.currency):
            errors["currency"] = f"Invalid currency {self.currency}"
        return errors
