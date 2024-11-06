# ansible

## Ad-hoc
```
ansible all --limit 'DB' -i inventory/prod -m shell -a "sudo cat /etc/shadow | grep dbuser" -J -v
```

# Get password hash for using in user module

python3 -c "from passlib.hash import sha512_crypt; import getpass; print(sha512_crypt.using(rounds=5000).hash(getpass.getpass()))"
