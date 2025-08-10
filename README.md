# Malte's script collection

  * `bin`: scripts on the PATH on all machines
    * As of this writing, these were only really collected from many different
      sources, some of them ancient. Needs consolidation, love and care.
  * `bin-dmi-kibo`: scripts on the PATH on dmi-kibo (work desktop)
    * `backup-kibo`: nightly incremental backup
  * `bin-login-12`: scripts on the PATH on the grid login node
    * `autonice-check`: check if autonice is running
    * `autonice-start`: start autonice
    * `autonice-stop`: stop autonice
    * `q`: convenience wrapper for squeue (very old, wants update)
    * `qq`: like `q`, but shows more things (very old, wants update)
  * `bin-nils`: scripts on the PATH on nils (home server)
    * `reminder`: symbolic link to reminder script
    * `repo`: monkey-patched version of repo repository manager
  * `bin-pamster`: scripts on the PATH on pamster (home desktop)
    * `broadcast-command`: run a command on many machines
    * `broadcast-scripts`: pull scripts repository from many machines
    * `broadcast-yadm`: run yadm pull from many machines
    * `make-archive`: turn a directory into an encrypted SquashFS archive
  * `games`: scripts for games
    * `factorio`: calculate stuff for Factorio
    * `mini-settlers`: calculate stuff for Mini Settlers
  * `lib`: libraries and scripts that are part of my basic setup
    * `bash_completion.py`: bash completion for Python scripts
    * `bashtools.py`: bash escaping and unescaping
    * `combinatorics.py`: basic combinatorial functions
    * `myemail.py`: send emails
    * `myoptparse.py`: tweaked version of `optparse.OptionParser`
    * `pythonstartup.py`: Python startup script
    * `statistics.py`: basic statistical functions
    * `t.py`: task management script
  * `misc`: miscellaneous stuff
    * `dmics_competition.py`: find smallest formula representations for Boolean
      functions
    * `ssh.py`: ssh proxy script to conditionally use tunnels (needs python2.7)
