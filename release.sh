#!/usr/bin/env bash

ROOT_DIR=$(pwd)
TARGET_DIR=$ROOT_DIR/target
rm -rf $TARGET_DIR
mkdir -p $TARGET_DIR
TEMP_DIR=`mktemp -d`
echo Using temp dir $TEMP_DIR
cp __init__.py $TEMP_DIR
cp manifest.json $TEMP_DIR
mkdir $TEMP_DIR/cloze_anything
cp cloze_anything/__init__.py $TEMP_DIR/cloze_anything
pushd $TEMP_DIR
zip -r anki_cloze_anything.zip .
echo Moving package to $TARGET_DIR
mv anki_cloze_anything.zip $TARGET_DIR
popd
rm -rf $TEMP_DIR