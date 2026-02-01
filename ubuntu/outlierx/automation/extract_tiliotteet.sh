tiliote_dir=~/Documents/outlierx/tiliote
mkdir -p ${tiliote_dir}/extracted
for file in ${tiliote_dir}/*.zip; do
    unzip -n "$file" -d ${tiliote_dir}/extracted
done

