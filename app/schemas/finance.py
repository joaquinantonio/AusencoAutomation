from dataclasses import dataclass, asdict
from typing import List, Dict, Any
@dataclass
class VarianceRow:
    account:str; actual:float; budget:float; variance_pct:float
@dataclass
class FinanceReport:
    period:str; highlights:List[str]; variance_table:List[VarianceRow]; risks:List[str]
    def to_json(self)->Dict[str,Any]:
        return {"period":self.period,"highlights":self.highlights,
                "variance_table":[asdict(v) for v in self.variance_table],"risks":self.risks}
