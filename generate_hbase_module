#/bin/bash
#
# Generate the HBase Thrift API using latest
# thrift specification from hbase trunk
#


error() {
	printf "ERROR: $*\n" >&2
	exit 1
}

TMPDIR=`mktemp -d` 
OUTDIR=$(dirname $0)/hbase

pushd $TMPDIR >/dev/null

echo "Grabbing latest Hbase.thrift"
wget 'https://svn.apache.org/repos/asf/hbase/trunk/src/main/resources/org/apache/hadoop/hbase/thrift/Hbase.thrift' -O Hbase.thrift -q || {
	error "Could not download Hbase.thrift, aborting."
}
thrift  --gen py Hbase.thrift

popd >/dev/null

mkdir -p $OUTDIR
cp  $TMPDIR/gen-py/hbase/*.py $OUTDIR

echo "All done"
