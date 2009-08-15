
d=`pwd`
export PYTHONPATH=$d/src/:$d/import/:.:/usr/local/lib/python
echo $PYTHONPATH

cd import
nosetests
