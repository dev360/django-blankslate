#!/bin/bash
# Okay, I know this is ghetto. Please have mercy.
#
echo "What is the name of your project?"
read projectName

mkdir -p $projectName
cp -r blankslate/. $projectName

# Clean up garbage
find . -name "*.pyc" -exec rm -rf {} \;
find . -name "*.swp" -exec rm -rf {} \;

for i in `grep -irn "blankslate" "${projectName}/." |cut -d: -f1|grep ".py\|.js\|.html\|.example\|.txt"|uniq`; do
    sed -i "" -e "s/blankslate/${projectName}/g" $i;
    sed -i "" -e "s/Blankslate/${projectName}/g" $i;
done
