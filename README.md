# qmtools

## The little things in life.

* **qmin**      : Make job inputs from xyz and log files. (i.e. crin2)
* **qdelall**   : delete Raijin jobs by name/status/queue/whatever. Uses regex.
* **pysub**     : submits jobs from input files. Written to be very easy to link to qmin, which I will do at some point. Also will eventually dual submit to Iodine.
* **retrieve**  : retrieve output from Raijin. Will potentially make a daemon for this.
* **review**    : print output of retrieve. Uses regex.
* **binlink**   : Save time simlinking! Links to $HOME/bin

Every one of these has a --help section. None have docstrings or comments.

## Examples:
```bash
