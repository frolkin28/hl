package hadoop;
import java.util.*;
import java.io.IOException;
import java.io.IOException;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.util.*;
public class ProcessUnits {
    //Mapper class
    public static class E_EMapper extends MapReduceBase implements
    Mapper < LongWritable, /*Input key Type */
        Text, /*Input value Type*/
        Text, /*Output key Type*/
        FloatWritable > /*Output value Type*/ {
            //Map function
            public void map(LongWritable key, Text value,
                OutputCollector < Text, FloatWritable > output,
                Reporter reporter) throws IOException {
                String line = value.toString();
                String lasttoken = null;
                StringTokenizer s = new StringTokenizer(line, "\t");
                String year = s.nextToken();
                while (s.hasMoreTokens()) {
                    lasttoken = s.nextToken();
                    float val = Float.parseFloat(lasttoken);
                    output.collect(new Text(year), new FloatWritable(val));
                }
            }
        }
    //Reducer class
    public static class E_EReduce extends MapReduceBase implements
    Reducer < Text, FloatWritable, Text, FloatWritable > {
        //Reduce function
        public void reduce(Text key, Iterator < FloatWritable > values,
            OutputCollector < Text, FloatWritable > output, Reporter reporter)
        throws IOException {
            float maxavg = 30;
            float n = 0;
            float sum = 0;
            while (values.hasNext()) 
            { 
               float val = values.next().get();

               sum += val;
               n++;
            }
            float avg = sum / n;

            if (avg > maxavg) {
                output.collect(key, new FloatWritable(avg));
            }
        }
    }

    //Main function
    public static void main(String args[]) throws Exception {
        JobConf conf = new JobConf(ProcessUnits.class);
        conf.setJobName("max_eletricityunits");
        conf.setOutputKeyClass(Text.class);
        conf.setOutputValueClass(FloatWritable.class);
        conf.setMapperClass(E_EMapper.class);
        conf.setCombinerClass(E_EReduce.class);
        conf.setReducerClass(E_EReduce.class);
        conf.setInputFormat(TextInputFormat.class);
        conf.setOutputFormat(TextOutputFormat.class);
        FileInputFormat.setInputPaths(conf, new Path(args[0]));
        FileOutputFormat.setOutputPath(conf, new Path(args[1]));
        JobClient.runJob(conf);
    }
}
