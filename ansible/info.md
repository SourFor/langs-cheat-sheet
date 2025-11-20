# ansible

## Ad-hoc
```
ansible all --limit 'DB' -i inventory/prod -m shell -a "sudo cat /etc/shadow | grep dbuser" -J -v
ansible all -i inventory/fin_srv_kafka.ini -m shell -a "sleep 60 ; sudo systemctl restart kafka" -J -v -f 1
```

## Get password hash for using in user module

python3 -c "from passlib.hash import sha512_crypt; import getpass; print(sha512_crypt.using(rounds=5000).hash(getpass.getpass()))"

## Check filter

```sh
ansible localhost -m debug -a msg="{{ (max_wal_size | regex_replace('[^0-9.]', '') | int * 10) ~ (max_wal_size | regex_replace('[0-9.]', '')) }}" -e max_wal_size=2Gb
```

## Check vars

```sh
ansible master -i inventory/db -m debug -a "var=hostvars[inventory_hostname]" -J
```

## python scripts

```sh
python3 ansible_vault_search_users.py --dir group_vars --vault-pass vault.txt -o ~/Documents/users.csv --csv

python3 delete_from_ansible_vault.py --dir group_vars --vault-pass vault.txt -r "username"
python3 delete_from_ansible_vault.py --dir /path/to/vault/files --vault-pass ~/.vault_pass.txt -f patterns.txt --check
```
