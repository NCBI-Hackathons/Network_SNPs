<?php
#reads a dbgap association file, parses it, filters it, formats it and outputs data in 5 column bed file (ex entry: chr2	128169898	128169899	A	G) chromosome, start, stop for the snp, reference and variant allele.
 
set_time_limit(0);
#setting the memory limit

ini_set("memory_limit","100000M");
error_reporting(E_ALL & ~E_NOTICE);

#gets dbgap file name from user in command line - $php dbvartofunseq.php dbgapdata.txt
#$csvfile=file("done/ck_genbank_gene_ontology_t.csv", FILE_IGNORE_NEW_LINES);
$filename=$_SERVER['argv'];

#print_r($filename);
#echo $filename[1];

$csvfile=file($filename[1],FILE_IGNORE_NEW_LINES);
#print_r($csvfile);
#$csvfile=file("/home/ubuntu/graphanalytics/funseq2/funseq2-1.2/phs000182data.txt", FILE_IGNORE_NEW_LINES);


foreach($csvfile as $csv)
{
#$csvnoq=str_replace('"','',$csv);
#echo $csv,"\n";
#filter out comments, header column, empty lines
if($csv[0]!=="#")
	{
	$csvline=explode('	',$csv);
#	print_r($csvline);
	
#	echo count($csvline);

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


#print_r($biogrid);
#echo chr.$csvline[2],"\t",$csvline[3],"\t",$csvline[3]+1,"\t",$csvline[7],"\t",$csvline[8],"\n";

}

?>
