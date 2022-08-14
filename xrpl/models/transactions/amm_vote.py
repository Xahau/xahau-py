"""Model for AMMVote transaction type."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

from typing_extensions import Final

from xrpl.models.required import REQUIRED
from xrpl.models.transactions.transaction import Transaction
from xrpl.models.transactions.types import TransactionType
from xrpl.models.utils import require_kwargs_on_init

_MAX_TRADING_FEE: Final[int] = 65000


@require_kwargs_on_init
@dataclass(frozen=True)
class AMMVote(Transaction):
    """
    AMMVote is used for submitting a vote for the trading fee of an AMM Instance.

    Any XRPL account that holds LPTokens for an AMM instance may submit this
    transaction to vote for the trading fee for that instance.
    """

    amm_hash: str = REQUIRED  # type: ignore
    """
    AMMHash is a hash that uniquely identifies the AMM instance.
    """

    fee_val: int = REQUIRED  # type: ignore
    """
    FeeVal specifies the fee, in basis point.
    Valid values for this field are between 0 and 65000 inclusive.
    A value of 1 is equivalent to 1/10 bps or 0.001%, allowing trading fee
    between 0% and 65%.
    """

    transaction_type: TransactionType = field(
        default=TransactionType.AMM_VOTE,
        init=False,
    )

    def _get_errors(self: AMMVote) -> Dict[str, str]:
        return {
            key: value
            for key, value in {
                **super()._get_errors(),
                "fee_val": self._get_fee_val_error(),
            }.items()
            if value is not None
        }

    def _get_fee_val_error(self: AMMVote) -> Optional[str]:
        if self.fee_val > _MAX_TRADING_FEE:
            return f"Must not be greater than {_MAX_TRADING_FEE}"
        return None
