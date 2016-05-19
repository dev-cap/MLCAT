# Move to data/graphs before running
cp -v csv/* ../../code/
cp -v ../json/* ../../code/
cd ../../code/
mkdir gexf dot png
echo "Executing graph_generate_dot.py"
python graph_generate_dot.py
rm *.csv
rm *.json
mv png/* ../data/graphs/png
mv dot/* ../data/graphs/dot
mv gexf/* ../data/graphs/gexf
rm -d png dot gexf
