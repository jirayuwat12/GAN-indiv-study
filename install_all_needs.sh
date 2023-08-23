source ./env/bin/activate

for FILE in `find . -name 'requirements.txt'`
do
    pip install -r $FILE
done

deactivate