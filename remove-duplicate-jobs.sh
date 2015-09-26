#!/bin/bash

echo 'Remove duplicate Indeed Jobs'
mysql --user=lokerhubuser --password=lokerhubpassword2015! --database=lokerhubdb --execute="DELETE n1 FROM indeed_jobs n1, indeed_jobs n2 WHERE n1.id > n2.id AND n1.jobkey = n2.jobkey"
