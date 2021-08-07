library(fgsea)
library(dplyr)
library(tibble)
library(data.table)
library(ggplot2)
#Set work direction
setwd("E:\\published code\\fGSEA\\Data")
dir()
#Matrix(2,044 instances) and annotation files 
gene_symbol <- read.csv("Data\\gene_symbol_all_22268.csv")
sig_id <- read.csv("sigid_A549.csv",header=FALSE)
CD_anno_2 <- read.csv("A549_CD_all_20210629.csv")
result <-  as.data.frame(t(as.data.frame(c(1:8))))
colnames(result) <- c("pathway" ,"pval","padj","ES","NES","nMoreExtreme","size","leadingEdge" )
result <- result[-1,]
#signature genes (it was saved as ".gmt" file)
pathways <- gmtPathways("IAV_signature_genes.gmt")
#We're going to calculate ES score for each instance
for(j in c(1,2)){
  pathways_1 <- pathways[j]
  for(i in 2:2045 ){
    x1 <- CD_anno_2[,c(1,i)]
    x2 <- x1 %>% 
      group_by(pr_gene_symbo) %>% 
      summarise_all(mean)
    x3 <- deframe(as.data.frame(x2[order(x2[,2]),],colClasses = c("character", "numeric")))
    fgseaRes <- fgseaSimple(pathways_1, x3, nperm=1000,minSize=0, maxSize=700)
    class(fgseaRes)
    result <- rbind(result,fgseaRes)
    print(j)
    print(i)
  }
}
result_up <- result[c(1:2044),c(1:7)]
result_dn <- result[c(2045:4088),c(1:7)]
rownames(result_up) <- sig_id[,1]
rownames(result_dn) <- sig_id[,1]
result_up_down <- cbind(result_up,result_dn)
colnames(result_up_down) <- c("pathway_up","pval_up","padj_up","ES_up","NES_up","nMoreExtreme_up","size_up","pathway_down","pval_down" 
                          ,"padj_down","ES_down" , "NES_down" ,"nMoreExtreme_down","size_down" )
result_up_down$ES_up <- ifelse(result_up_down$pval_up>0.05,result_up_down$ES_up*0,result_up_down$ES_up)
result_up_down$ES_down <- ifelse(result_up_down$pval_down>0.05,result_up_down$ES_down*0,result_up_down$ES_down)
result_up_down <- mutate(result_up_down,
       ESchem=(ES_up - ES_down)/2)
result_Final_2 <- result_up_down[order(result_up_down[,15],decreasing=F),]
result_Final_2 <- as.matrix(result_Final_2)
rownames(result_Final_2) <- sig_id[,1] 
write.csv(result_Final_2,"fgsea_result.csv")























