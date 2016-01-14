library(readr)
url='https://github.com/macarthur-lab/clinvar/raw/master/output/clinvar.tsv.gz'
w=readr::read_tsv(url)
w<-w %>% filter(grepl('LabCorp',all_submitters))
#traits are separated by semicolons
ttd<-stringr::str_split(w$all_traits,pattern = ';')

#there are several traits per row from str_split
ttd.l<-sapply(ttd,length)
#sample
ttd[[77]]

w$measureset_id

#how to put all 'all-traits' into single vector
traits <- unlist(ttd)

i=3
out=data.frame()
for (i in 1:length(ttd)) {
  print(i)
  #unlist(ttd[[i]])
  one<-data.frame(id=w[i,'measureset_id']
                  ,trait=unique(toupper(unlist(ttd[[i]]))))
  out<-rbind(out,one)
}

origOut=out
out<-left_join(out,w)
head(out,5)
tti<-as.data.frame(table(out$trait))
out$url = sprintf('http://www.ncbi.nlm.nih.gov/clinvar/variation/%s',out$measureset_id)
library(stringr)
#mytrait='ARRHYTHMIA'
for (mytrait in unique(out$trait)){
  print(mytrait)
  one=filter(out,trait==mytrait)
  print(nrow(one))
  if(nrow(one) >30) write_csv(one,path=paste0('result/',str_replace(mytrait,'/','~'),'.csv'))
}
