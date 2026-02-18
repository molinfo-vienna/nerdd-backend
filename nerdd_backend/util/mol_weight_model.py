from typing import Any, List

from nerdd_module import Model
from nerdd_module.preprocessing import Sanitize
from rdkit.Chem import Mol
from rdkit.Chem.rdMolDescriptors import CalcExactMolWt

__all__ = ["MolWeightModel"]


class MolWeightModel(Model):
    def __init__(self) -> None:
        super().__init__(preprocessing_steps=[Sanitize()])

    def _predict_mols(self, mols: List[Mol], multiplier: float) -> List[dict[str, float]]:
        return [{"weight": CalcExactMolWt(m) * multiplier} for m in mols]

    def _get_base_config(self) -> dict[str, Any]:
        return {
            "name": "mol_scale",
            "version": "0.1",
            "description": "Computes the molecular weight of a molecule",
            "job_parameters": [
                {"name": "multiplier", "type": "float"},
            ],
            "result_properties": [
                {"name": "weight", "type": "float"},
            ],
        }
