# /usr/bin

# TODO this should be running in the environment
# sudo apt-get install swig

if [ $# != 2 ]
then 
	echo "usage your-replace_M2Crypto_setup.py your-virtual-environment-path(like env or env/ something)" 
	exit
fi
replace_file=$1
virtual_env=$2
virtual_env=${virtual_env%/}/
related="build/M2Crypto/setup.py" 
result=$`pip install M2Crypto`
setup_path=$virtual_env$related

if [ -f $setup_path ]
then
	echo "replace file"
	cp $replace_file $setup_path
	pip install M2Crypto
else
	echo "areally installed"
fi
