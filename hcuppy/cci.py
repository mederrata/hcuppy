import hcuppy.utils as utils

class CCIEngine:

    def __init__(self):
        fn = "data/cci_icd10cm_2019_1.csv"
        self.dx2cci = utils.read_cci(fn)
        self.icd9to10_dx = utils.read_icd9to10_diagnosis("data/icd9to10_diagnosis.txt", "data/masterb10.csv")

    def _get_cci(self, dx_lst):
        """
        Returns CCI or a list of CCI for the given ICD code(s).
        Here, CCI stands for Chronic Condition Indicator..
        The original software can be found at 
        https://www.hcup-us.ahrq.gov/toolssoftware/
            chronic_icd10/chronic_icd10.jsp

        Parameters
        __________
        icd_lst: list of str, or str
                A list of ICD10 diagnosis codes.
                The output is  a list of corresponding CCIs.
                If this parameter is a scalar (not a list), then 
                the output will be a scalar.
        """


        output_type = "list"
        if not isinstance(dx_lst, list):
            output_type = "value"
            dx_lst = [dx_lst]
        
        dx_lst = [dx.strip().upper().replace(".","") for dx in dx_lst]
        cci_lst = []
        out_default = {"is_chronic": False,
                        "body_system": "na",
                        "body_system_desc": "na"}
        for dx in dx_lst:
            if dx not in self.dx2cci:
                cci_lst.append(out_default)
            else:
                cci_lst.append(self.dx2cci[dx])

        out = cci_lst
        if output_type == "value":
            out = cci_lst[0]
 
        return out

    def has_chronic(self, dx_lst):
        cci_lst = [cci for cci in self.get_cci(dx_lst)]
        return any(cci["is_chronic"] for cci in cci_lst)

    def is_chronic(self, dx, dx9_lst):
        cci = self.get_cci(dx, dx9_lst)
        return cci["is_chronic"]

    def get_cci(self, dx_lst=None, dx9_lst=None):
        """
        Returns CCI or a list of CCI for the given ICD code(s).
        Here, CCI stands for Chronic Condition Indicator..
        The original software can be found at 
        https://www.hcup-us.ahrq.gov/toolssoftware/
            chronic_icd10/chronic_icd10.jsp

        Parameters
        __________
        icd_lst: list of str, or str
                A list of ICD10 diagnosis codes.
                The output is  a list of corresponding CCIs.
                If this parameter is a scalar (not a list), then 
                the output will be a scalar.

        icd9_lst: list of str, or str
                A list of ICD9 diagnosis codes.
                The output is  a list of corresponding CCIs.
                If this parameter is a scalar (not a list), then 
                the output will be a scalar.
        """

        if dx9_lst is not None:
            if isinstance(dx9_lst, list):
                icd10 = [ self.icd9to10_dx.get(x, x) for x in dx9_lst ]
            else:
                icd10 = self.icd9to10_dx.get(dx9_lst, dx9_lst)
        else:
            return self._get_cci(dx_lst)
        return self._get_cci(icd10)
