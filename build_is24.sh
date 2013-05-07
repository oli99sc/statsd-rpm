git submodule init
git submodule update

DATE=`date +%Y%m%d`
STATSD_RPM_SHA=$(git show-ref HEAD --hash)
cd statsd
STATSD_SHA=$(git show-ref HEAD --hash)
cd ../is24-statsd
IS24_STATSD_SHA=$(git show-ref HEAD --hash)
cd ..

echo "statsd sha $STATSD_SHA"
echo "statds-rpm sha $STATSD_RPM_SHA"
echo "is24-statds sha $IS24_STATSD_SHA"

mkdir -p is24-statsd-$DATE
rsync -av is24-statsd/ is24-statsd-$DATE --exclude=.git
tar -cvzf is24-statsd-$DATE.tar.gz statsd-$DATE
rm -rf is24-statsd-$DATE
cat is24-statsd.spec.in | sed -e "s/DATE/$DATE/" -e "s/RELEASE_ID/${STATSD_RPM_SHA:0:10}/" -e "s/IS24_STATSD_SHA/$IS24_STATSD_SHA/" -e "s/STATSD_SHA/$STATSD_SHA/" -e "s/STATSD_RPM_SHA/$STATSD_RPM_SHA/" > is24-statsd.spec
mkdir -p ~/rpmbuild/SOURCES
mv is24-statsd-$DATE.tar.gz ~/rpmbuild/SOURCES
rpmbuild -ba is24-statsd.spec
rm is24-statsd.spec 
