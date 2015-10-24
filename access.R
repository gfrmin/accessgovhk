library(jsonlite)
library(data.table)
library(stringr)

ati <- data.table(fromJSON("ati.json"))

ati[,subdepartment := str_replace(subdepartment, "AAA", "")]
ati[,subdepartment := str_replace(subdepartment, department, "")]
ati[,fax := str_replace(fax, "\\(.*?\\) ", "")]
ati[,tel := str_replace(tel, "\\(.*?\\) ", "")]
# ati[,

teldir <- fread("https://hkdata.dataguru.hk/assets/teldir.csv")

setkey(ati, tel)
setkey(teldir, tel)
teldirati <- teldir[,list(tel,email)][ati]
setkey(teldirati, department, subdepartment, email)
teldirati <- unique(teldirati)

write.csv(teldirati, file = "teldirati.csv", row.names = FALSE)
