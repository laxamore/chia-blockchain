from dataclasses import dataclass
from typing import List, TypeVar

from chia.consensus.cost_calculator import NPCResult
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.spend_bundle import SpendBundle
from chia.util.ints import uint32, uint64
from chia.util.streamable import Streamable, streamable

_T_MempoolItem = TypeVar("_T_MempoolItem", bound="MempoolItem")


@streamable
@dataclass(frozen=True)
class MempoolItem(Streamable):
    spend_bundle: SpendBundle
    fee: uint64
    npc_result: NPCResult
    cost: uint64
    spend_bundle_name: bytes32
    additions: List[Coin]
    removals: List[Coin]
    height_added_to_mempool: uint32

    def __lt__(self, other: _T_MempoolItem) -> bool:
        return self.fee_per_cost < other.fee_per_cost

    @property
    def fee_per_cost(self) -> float:
        return int(self.fee) / int(self.cost)

    @property
    def fee_per_k_cost(self) -> float:
        return 1000 * (int(self.fee) / int(self.cost))

    @property
    def name(self) -> bytes32:
        return self.spend_bundle_name
