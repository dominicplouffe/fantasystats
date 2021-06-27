mongodump -d fantasy_data --host ip-172-31-10-116.us-east-2.compute.internal:27017 -o /data/backup/fs_$(date +\%Y\%m\%d)
tar -czvf /data/backup/fs_$(date +\%Y\%m\%d).tgz /data/backup/fs_$(date +\%Y\%m\%d)/fantasy_data
/usr/bin/s3cmd put /data/backup/fs_$(date +\%Y\%m\%d).tgz s3://fantasydataobj/backup/hd_$(date +\%Y\%m\%d).tgz
rm /data/backup/fs_$(date +\%Y\%m\%d).tgz
rm -r /data/backup/fs_$(date +\%Y\%m\%d)