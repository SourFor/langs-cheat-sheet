#!/bin/sh

if [-z "$1"]
      then
            echo "No arguments supplied"
            exit 1
fi

tempdir=$( mktemp -d ); \
      rsync -v --stats --progress -a --delete $tempdir/ /$1/; \
      rmdir $tempdir

SHORT_HOSTNAME=$(hostname -s)
# Определяем переменные для формирования письма
EMAIL_SUBJECT="Очистка каталога $1" 
EMAIL_SERVER="smtp://gw.example.net:25"
RECIPIENT="support@example.net"

EMAIL_BODY="$REPORT\n\n\nРабота скрипта по очистке остановлена. Очистка каталога $1 завершена. Проверьте результат\n"
EMAIL_SENDER="info@$SHORT_HOSTNAME.example.net"

# Формируем письмо и отправляем его
echo -e "$EMAIL_BODY" | mail -s "$EMAIL_SUBJECT" -r "$EMAIL_SENDER" -S mta="$EMAIL_SERVER" "$RECIPIENT"
