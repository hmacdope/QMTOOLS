from .qminp import QMInp
from utils.other import indent

class QChemInp(QMInp):
    """
    QChem input files. Fairly sraightforward.
    I have no idea what nbo is.
    """

    ext = "in"
    program = "qchem"

    jobtype = "sp"
    jobtype2 = ""
    nbo = ""
    solvent_section = ""
    remsolv = ""
    backend = "XM"

    def ask_questions(self):
        super().ask_questions()
        self.ask("convergence")
        self.ask("backend")

    def make_coords(self):
        super().make_coords()
        self.coords = "".join([indent(x, n=4) for x in self.coords.split('\n')])

    def make_string_options(self):
        if self.optimize:
            self.jobtype = "opt"
            if self.calculate_frequencies:
                self.jobtype2 = "freq"

        if self.solvate:
            self.remsolv = f"SOLVENT_METHOD {self.solvent_model}"
            self.solvent_section = indent(f"\n$smx\n  solvent {self.solvent}\n$end")

    def make_file_lines(self):
        jobstr      = f"JOBTYPE               {self.jobtype}"
        theory      = f"METHOD                {self.theory}"
        basis       = f"BASIS                 {self.basis}"
        cc_backend  = f"CC_BACKEND            {self.backend}"
        mem_total   = f"MEM_TOTAL             60000"
        thresh      = f"SCF_CONVERGENCE       8"
        int_thresh  = f"THRESH                14"
        lin_dep_thr = f"BASIS_LIN_DEP_THRESH  8"
        purecart    = f"PURECART              1112"
        frag_method = f"FRGM_METHOD           STOLL"
        frag_lpcor  = f"FRGM_LPCORR           EXACT_SCF"
        eda_bsse    = f"EDA_BSSE              TRUE"
        scf_frg_pr  = f"SCF_PRINT_FRGM        TRUE"
        eda2        = f"EDA2                  1"
        eda_bsse    = f"EDA_BSSE              TRUE"
        eda_frz     = f"FRZ_ORTHO_DECOMP_CONV 14"

        if self.eda:
            self.jobtype = "EDA"
            self.jobid += '_eda'
            jobstr      = f"JOBTYPE               {self.jobtype}"
            rem_lines   = [jobstr,theory, basis, purecart, thresh, int_thresh, lin_dep_thr, eda2, eda_bsse, scf_frg_pr,frag_method,frag_lpcor,eda_frz, self.remsolv]
        elif self.bsse:
            self.jobtype = "BSSE"
            jobstr      = f"JOBTYPE               {self.jobtype}"
            self.jobid += '_bsse'
            rem_lines = [jobstr, theory, basis, purecart, thresh, int_thresh, lin_dep_thr, scf_frg_pr, self.remsolv]
        elif self.theory == "CCSD-T":
            rem_lines = [jobstr, theory, basis, cc_backend, self.remsolv, mem_total]
        else:
            rem_lines = [jobstr, theory, basis, thresh, int_thresh, lin_dep_thr, self.remsolv]
        
        rem_body = "".join([indent(x, n=4) for x in rem_lines])

        molspec = f"$molecule\n  {self.cm}\n{self.coords}$end\n"
        rem = f"\n$rem\n\n{rem_body}$end\n"

        self.file_lines = f"{molspec}{rem}{self.solvent_section}"
