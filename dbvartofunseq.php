<?php
#reads a dbgap association file, parses it, filters it, formats it and outputs data in 5 column bed file 
#(ex entry: chr2	128169898	128169899	A	G) chromosome, start, stop for the snp, reference and variant allele.
 
#setting the time limit
set_time_limit(0);

#setting the memory limit
ini_set("memory_limit","100000M");

#suppressing the notices
error_reporting(E_ALL & ~E_NOTICE);

#gets dbgap file name from user in command line - $php dbvartofunseq.php dbgapdata.txt
$filename=$_SERVER['argv'];

#get the file contents in to an array
$csvfile=file($filename[1],FILE_IGNORE_NEW_LINES);
#test print_r($csvfile);

#read through each of the snp entries
foreach($csvfile as $csv)
{
#filter out comments, header column, empty lines
if($csv[0]!=="#")
	{
	#separate column data
	$csvline=explode('	',$csv);
	if(count($csvline)>1)
		{
		if($csvline[0]!="SNP ID")
			{
			#filter out associations with pvalue >=0.0005
			if($csvline[1]<=0.0005)
				{
				#print_r($csvline);
				echo chr.$csvline[2],"\t",$csvline[3],"\t",$csvline[3]+1,"\t",$csvline[7],"\t",$csvline[8],"\n";
				}
			}
		}
	}
}

?>
