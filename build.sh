
DATE=`date +%Y%m%d`

mkdir -p statsd-$DATE
rsync -av statsd/ statsd-$DATE --exclude=.git
mkdir -p statsd-$DATE/redhat
cp redhat/statsd statsd-$DATE/redhat/
tar -cvzf statsd-$DATE.tar.gz statsd-$DATE
rm -rf statsd-$DATE
cat statsd.spec.in | sed -e "s/DATE/$DATE/" > statsd.spec
mkdir -p ~/rpmbuild/SOURCES
mv statsd-$DATE.tar.gz ~/rpmbuild/SOURCES
rpmbuild -ba statsd.spec
rm statsd.spec 
