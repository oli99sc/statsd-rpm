git submodule init
git submodule update

DATE=`date +%Y%m%d`
STATSD_RPM_SHA=$(git show-ref HEAD)
cd statsd
STATSD_SHA=$(git show-ref HEAD)
cd ../is24-statsd
IS24_STATSD_SHA=$(git show-ref HEAD)
cd ..

echo $STATSD_SHA
echo $STATSD_RPM_SHA
echo $IS24_STATSS_SHA

mkdir -p statsd-$DATE
rsync -av statsd/ statsd-$DATE --exclude=.git
mkdir -p statsd-$DATE/redhat
cat is24-statsd/redhat/is24-statsd | sed -e "s#is24-##g" -e "s#is24 ##g" > statsd-$DATE/redhat/statsd
tar -cvzf statsd-$DATE.tar.gz statsd-$DATE
rm -rf statsd-$DATE
cat statsd.spec.in | sed -e "s/DATE/$DATE/" -e "s/RELEASE_ID/${STATSD_RPM_SHA:0:10}/" -e "s/STATSD_SHA/$STATSD_SHA/" -e "s/IS24_STATSD_SHA/$IS24_STATSD_SHA/" -e "s/STATSD_RPM_SHA/$STATSD_RPM_SHA/" > statsd.spec
mkdir -p ~/rpmbuild/SOURCES
mv statsd-$DATE.tar.gz ~/rpmbuild/SOURCES
rpmbuild -ba statsd.spec
rm statsd.spec 
