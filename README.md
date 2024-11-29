In /etc/apt/apt.conf.d/99hash-update, add /home/lichenaut/CodiumProjects/miotsec-final/update.sh

Make sure all bash scripts are executable.

Example cron: 0 \* \* \* \* /.../routine.sh >> /.../activity.log 2>&1
