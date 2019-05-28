from .qminp import QMInp

class GaussianInp(QMInp):
    """
    For Gaussian input files.

    Note -- unsure when the z-matrix stuff is ever used.
    """
    ext = "com"
    program = "gaussian"

    grid = ""
    opt = ""
    freq = ""
    scrf = ""
    dovac = ""
    scrf_dovac = ""
    NBO_str = ""
    bsse_str = ""
    wfn_string = ""
    cb_cm = ""
    solvents = dict(
        water="h2o",
        Pentadecane="n-Pentadecane",
        Octanol="n-Octanol")

    @property
    def basis(self):
        return self._basis

    @basis.setter
    def basis(self, basis_set):
        self._basis = basis_set
        to_rass = {"6-31G*":"6-31Gd",
                    "6-31G(d)":"6-31Gd",
                    "6-31+G*": "6-31pGd",
                    "6-31+G(d)": "6-31pGd",
                    }
        try:
            self.rassolov_version = to_rass[self._basis]
            if self._ask_questions:
                self.askbool("rassolov")
            if self.rassolov:
                self.genbasis = self.rassolov_version
                self._basis = "Gen 6D"
            else:
                self.genbasis = self._basis

        except KeyError:
            self.rassolov_version = self._basis
            self.rassolov = None
            self.genbasis = self._basis

    def make_string_options(self):
        if self.theory not in ["csd", "qci", "mp2", "hf"]:
            self.grid = " INT(grid=ultrafine)"

        if self.solvate:
            self.gaussian_solvent = self.solvents[self.solvent]
            if self.dGsolv:
                self.dovac = ",dovac,self"
            self.scrf = f" SCRF=(SMD,Solvent={self.gaussian_solvent})"
            self.scrf_dovac = f" SCRF=(SMD,Solvent={self.gaussian_solvent}{self.dovac})"
        

        if self.optimize:
            if self.calcfc:
                self.opt = " OPT=CalcFC IOP(2/17=4)"
            else:
                self.opt = " OPT IOP(2/17=4)"

        if self.calculate_frequencies:
            self.freq = " Freq=Noraman"

        if self.zmat:
            self.ts = "(z-matrix)"
            self.tszm = ",z-matrix"

        if self.transition_state:
            self.ts = f"(TS,calcfc{self.tszm},noeigentest,maxcyc=200)"

        if self.NBO:
            self.NBO_str = 'Pop=NBO'
        
        if self.wfn:
            self.jobid += '_wfn'
            self.wfn_string = 'Density=Current Output=WFN'

        if self.bsse:
            if self.carboxybind:
                self.cb_cm = '-1,1 0,1 -1,1'
            self.jobid += '_bsse'
            self.bsse_str = 'Counterpoise=2'
            newlines = []
            crdsplit = self.coords.split('\n')
            prev_element = ''
            fragment = '1'
            for idx,line in enumerate(crdsplit):
                if len(line.split()) != 0:
                    toks = line.split()
                    element = toks[0]
                    if self.carboxybind:
                        if (prev_element == 'O') and (element == 'O'):
                            fragment = '2'
                            carboxy_idx = idx -1
                        prev_element = element
                    element += f'(Fragment={fragment})'
                    newline = [element] + toks[1::]
                    newline = '    '.join(newline)
                    newlines.append(newline)
            #correct the missing frag
            if self.carboxybind:
                 line_pull =  newlines[carboxy_idx]
                 rest = line_pull.split()[1:]
                 new_front = 'O(Fragment=2)    '
                 line = new_front + '    '.join(rest)
                 newlines[carboxy_idx] = line

            #newlines += ['\n']
            self.coords ='\n'.join(newlines) +'\n'

        

    def make_file_lines(self):
        basis = f"@/home/{self.REMOTE_DIR}/{self.RJ_UNAME}/Basis/{self.genbasis}.gbs/N\n"
        link = "\n--Link1--\n"
        header_ = f"%chk={self.jobid}.chk\n# {self.theory}/{self.basis} SCF={self.convergence}{self.grid}{self.opt} {self.NBO_str} {self.bsse_str} {self.wfn_string} "
        header_nopt = f"%chk={self.jobid}.chk\n# {self.theory}/{self.basis} SCF={self.convergence}{self.grid} {self.NBO_str} {self.bsse_str} {self.wfn_string} "
        geom = f"geom=check guess=read IOP(2/17=4)\n\n{self.jobid}\n\n{self.cm}\n\n"
        if self.carboxybind:
            molspec = f"\n\n{self.cb_cm}\n{self.coords}\n"
        else:
            molspec = f"\n\n{self.cm}\n{self.coords}\n"
        header = header_[:]
        footer = basis + "\n"
        if self.wfn:
            footer += f' {self.jobid}.wfn\n\n'
        if self.optimize:
            header += f"{self.scrf_dovac}\n"
            footer += f"{link}{header_nopt}{self.scrf}{self.freq}\n{geom}{basis}"
            if self.dGsolv:
                footer += f"{link}{header_}{self.scrf_dovac}\n{geom}{basis}"
        else:
            header += f"{self.scrf}\n"

        header += f"\n{self.jobid}"

        self.file_lines = header + molspec + footer
        
