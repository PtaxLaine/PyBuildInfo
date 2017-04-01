#!/bin/bash

build_dir='build'

if ! [[ -d $build_dir ]]
then
	mkdir $build_dir
	if [[ $? -ne 0 ]]
	then
		echo 'STOP'
		exit -1
	fi
fi

source_dir=$(pwd)

cd $build_dir
if [[ $? -ne 0 ]]
then
	echo 'STOP'
	exit -1
fi

cmake $source_dir
if [[ $? -ne 0 ]]
then
	echo 'STOP'
	exit -1
fi

cmake --build . --target buildInfoExample_RUN
if [[ $? -ne 0 ]]
then
	echo 'STOP'
	exit -1
fi

cd $source_dir
