import hcuppy.utils as utils

class CCSEngine:

    def __init__(self, mode="dx"):
        self.x2ccs = {}
        self.mode = mode
        if mode == "dx":
            fn = "data/ccs_dx_icd10cm_2019_1.csv"
            self.x2ccs = utils.read_ccs(fn)
        elif mode == "pr":
            fn = "data/ccs_pr_icd10pcs_2019_1.csv"
            self.x2ccs = utils.read_ccs(fn)
        elif mode == "pr-cpt":
            fn = "data/cpt2ccs.json"
            self.x2ccs = utils.read_cpt2ccs(fn)
        self.icd9to10_dx = utils.read_icd9to10_diagnosis("data/icd9to10_diagnosis.txt", "data/masterb10.csv")

    def _get_ccs(self, x_lst):
        """
        Returns CCS or a list of CCS for the given ICD code(s).
        Here, CCS stands for Clinical Classifications Software.
        The original software can be found at 
        https://www.hcup-us.ahrq.gov/toolssoftware/ccs10/ccs10.jsp

        Parameters
        __________
        x_lst: list of str, or str
                A list of ICD10 diagnosis or procedure codes.
                The output is a list of corresponding CCS categories.
                If this parameter is a scalar (not a list), then 
                the output will be a scalar.
        """

        output_type = "list"
        if not isinstance(x_lst, list):
            output_type = "value"
            x_lst = [x_lst]

        x_lst = [x.strip().upper().replace(".","") for x in x_lst]
        ccs_lst = []
        out_default = {"ccs": "na",
                        "ccs_desc": "na"}
        for x in x_lst:
            if x not in self.x2ccs:
                ccs_lst.append(out_default)
            else:
                ccs_lst.append(self.x2ccs[x])

        out = ccs_lst
        if output_type == "value":
            out = ccs_lst[0]
        return out

    def get_ccs(self, x_lst=None, x9_lst=None):
        """
        Returns CCS or a list of CCS for the given ICD code(s).
        Here, CCS stands for Clinical Classifications Software.
        The original software can be found at 
        https://www.hcup-us.ahrq.gov/toolssoftware/ccs10/ccs10.jsp

        Parameters
        __________
        x_lst: list of str, or str
                A list of ICD10 diagnosis or procedure codes.
                The output is a list of corresponding CCS categories.
                If this parameter is a scalar (not a list), then 
                the output will be a scalar.

        x9_lst: list of str, or str
                A list of ICD9 diagnosis or procedure codes.
                The output is a list of corresponding CCS categories.
                If this parameter is a scalar (not a list), then 
                the output will be a scalar.
        """
        if x_lst is not None:
            return self._get_ccs(x_lst)

        if isinstance(x9_lst, list):
            icd10 = [ self.icd9to10_dx.get(x, x) for x in x9_lst ]
        else:
            icd10 = self.icd9to10_dx.get(x9_lst, x9_lst)
        return self._get_ccs(icd10)