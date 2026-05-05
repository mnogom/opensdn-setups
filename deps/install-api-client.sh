#!/bin/bash -e

REPO="${1:-"https://github.com/OpenSDN-io/tf-api-client"}"
BRANCH="${2:-"R25.1"}"

FILENAME=$(basename -- "$0")
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR

rm -rf ./api-client
git clone $REPO api-client
cd api-client
git checkout $BRANCH
rm -rf ./.git
mkdir api-lib/vnc_api/gen
cp ./generateds/cfixture.py api-lib/vnc_api/gen/
cp ./generateds/generatedssuper.py api-lib/vnc_api/gen
HEAT_BUILDTOP="." uv run python3 ./generateds/generateDS.py -f -g ifmap-frontend -o api-lib/vnc_api/gen/resource schema/all_cfg.xsd
cd api-lib/
uv run python3 setup.py install
