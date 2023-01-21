hadoop fs -mkdir input_dir
hadoop fs -put /app/sample.txt input_dir
hadoop fs -ls input_dir/
hadoop jar /app/units.jar hadoop.ProcessUnits input_dir output_dir
hadoop fs -cat output_dir/part-00000
hdfs dfs -copyToLocal output_dir /app
