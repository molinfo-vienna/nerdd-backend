from nerdd_module import Model
from nerdd_module.preprocessing import Sanitize
from rdkit.Chem.rdMolDescriptors import CalcExactMolWt

__all__ = ["MolWeightModel"]


class MolWeightModel(Model):
    def __init__(self):
        super().__init__(preprocessing_steps=[Sanitize()])

    def _predict_mols(self, mols, multiplier):
        return [{"weight": CalcExactMolWt(m) * multiplier} for m in mols]

    def _get_base_config(self):
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
