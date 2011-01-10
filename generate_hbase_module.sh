#/bin/bash
#
# Generate the HBase Thrift API using latest
# thrift specification from hbase trunk
#


error() {
	printf "ERROR: $*\n" >&2
	exit 1
}
cleanup() {
	echo "Cleaning up temporary artifacts..."
	if [ -n "$TMPDIR" ] && [ -d "$TMPDIR" ];
	then
		rm -rf ${TMPDIR}
	fi
}

TMPDIR=`mktemp -d` 
OUTDIR=$(dirname $0)/hbase

pushd $TMPDIR >/dev/null

echo "Grabbing latest Hbase.thrift..."
wget 'https://svn.apache.org/repos/asf/hbase/trunk/src/main/resources/org/apache/hadoop/hbase/thrift/Hbase.thrift' -O Hbase.thrift -q || {
	error "Could not download Hbase.thrift, aborting."
}

echo "Generating hbase python module from Hbase.thrift..."
thrift  --gen py Hbase.thrift || {
	error "Could not generate Hbase python bindings from Hbase.thrift, aborting."
}

popd >/dev/null

rm -rf $OUTDIR
mkdir -p $OUTDIR
cp  $TMPDIR/gen-py/hbase/*.py $OUTDIR

cleanup
echo "All done"
