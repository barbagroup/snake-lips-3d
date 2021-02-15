#!/usr/bin/env bash
# Provision a pool, ingress data, run a job,
# and delete job and pool (once the job is completed).
# cli: ./shipyard-driver.sh

read -p "Enter configuration directory: " configdir
echo
read -p "Enter directory for log files (press enter to use ./log_shipyard): " logdir
logdir=${logdir:-"log_shipyard"}
mkdir -p $logdir
echo

shipyard --version > $logdir/version.log 2>&1
printf "Provisioning pool of compute nodes ...\n"
shipyard pool add --configdir=$configdir --yes > $logdir/pool-add.log 2>&1
printf "Ingressing input data ...\n"
shipyard data ingress --configdir=$configdir > $logdir/data-ingress.log 2>&1
printf "Submitting job ...\n"
shipyard jobs add --configdir=$configdir > $logdir/jobs-add.log 2>&1
printf "Polling job until tasks are complete ...\n"
shipyard jobs tasks list --configdir=$configdir --poll-until-tasks-complete > $logdir/jobs-monitor.log 2>&1
printf "Deleting pool ...\n"
shipyard pool del --configdir=$configdir --yes > $logdir/pool-del.log 2>&1

printf "Done!\n"
