export KOSZ=$RANDOM
mkdir /var/kosz/$KOSZ/
echo Zapisano w $KOSZ
mv log.txt /var/kosz/$KOSZ/
mv db.json /var/kosz/$KOSZ/
mv ../users/*.json /var/kosz/$KOSZ/
