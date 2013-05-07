git submodule init
git submodule update

DATE=`date +%Y%m%d`

mkdir -p statsd-$DATE
rsync -av statsd/ statsd-$DATE --exclude=.git
mkdir -p statsd-$DATE/redhat
cat is24-statsd/redhat/is24-statsd | sed -e "s#is24-##g" -e "s#is24 ##g" > statsd-$DATE/redhat/statsd
tar -cvzf statsd-$DATE.tar.gz statsd-$DATE
rm -rf statsd-$DATE
cat statsd.spec.in | sed -e "s/DATE/$DATE/" > statsd.spec
mkdir -p ~/rpmbuild/SOURCES
mv statsd-$DATE.tar.gz ~/rpmbuild/SOURCES
rpmbuild -ba statsd.spec
rm statsd.spec 
