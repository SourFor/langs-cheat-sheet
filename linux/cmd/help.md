# Linux

## diff
```
diff -r --new-file -x '.*galaxy_install_info' -x '.git' -c ~/github.com/SourFor/ansible-role-jenkins/ ~/github.com/SourFor/devops-infra/ansible/roles/jenkins/ > last.patch
```

## patch

For example, suppose the file name in the patch file is /gnu/src/emacs/etc/NEWS. Using -p0 gives the entire file name unmodified, -p1 gives gnu/src/emacs/etc/NEWS (no leading slash), -p4 gives etc/NEWS, and not specifying -p at all gives NEWS.([www.gnu.org](https://www.gnu.org/software/diffutils/manual/html_node/patch-Directories.html))

```
patch -p6 < last.patch
```

## rsync

```sh
rsync -a --exclude='.git' источник/ цель/
```
