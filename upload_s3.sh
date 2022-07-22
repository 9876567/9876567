#!/bin/sh

set -e

aws configure --profile s3 <<-EOF > /dev/null 2>&1
${S3_ACCESS_KEY_ID}
${S3_SECRET_ACCESS_KEY}
auto
text
EOF

aws s3 cp db s3://$S3_BUCKET/ --profile s3 --no-progress --endpoint-url $S3_ENDPOINT --recursive

aws configure --profile s3 <<-EOF > /dev/null 2>&1
null
null
null
text
EOF