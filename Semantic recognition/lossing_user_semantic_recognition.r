##路径设置，数据敏感不提供
reviewpath <- "path" 
completepath <- list.files(reviewpath, pattern = "*.txt$", full.names = TRUE)


##批量读入文本  
read.txt <- function(x) {  
  des <- readLines(x)                   #每行读取  
  return(paste(des, collapse = ""))     #没有return则返回最后一个函数对象  
}  
review <- lapply(completepath, read.txt)  

##文章名字
docname <- list.files(reviewpath, pattern = "*.txt$")
reviewdf <- as.data.frame(cbind(docname, unlist(review)),stringsAsFactors = F)   
colnames(reviewdf) <- c("id", "msg")

reviewdf$msg <- gsub(pattern = " ", replacement ="", reviewdf$msg)  #gsub是字符替换函数，去空格  
reviewdf$msg <- gsub("\t", "", reviewdf$msg) #有时需要使用\\\t    
reviewdf$msg <- gsub(",", "，", reviewdf$msg)#文中有英文逗号会报错，所以用大写的“，”  
reviewdf$msg <- gsub("~|'", "", reviewdf$msg)#替换了波浪号（~）和英文单引号（'），它们之间用“|”符号隔开，表示或的关系  
reviewdf$msg <- gsub("\\\"", "", reviewdf$msg)#替换所有的英文双引号（"），因为双引号在R中有特殊含义，所以要使用三个斜杠（\\\）转义 


sentence <- as.vector(reviewdf$msg) #文本内容转化为向量sentence  
  
sentence <- gsub("[[:digit:]]*", "", sentence) #清除数字[a-zA-Z]  
sentence <- gsub("[a-zA-Z]", "", sentence)   #清除英文字符  
sentence <- gsub("\\.", "", sentence)      #清除全英文的dot符号  
sentence <- sentence[!is.na(sentence)]   #清除对应sentence里面的空值（文本内容），要先执行文本名  
sentence <- sentence[!nchar(sentence) < 2] #`nchar`函数对字符计数，英文叹号为R语言里的“非”函数 

--------------------------------------------------------------------government start-------------------------------------------------------------
#数据读取,数据敏感不提供
nlp_test_data=read.csv('data.csv',stringsAsFactors=F,header = T)

#数值删除
removeNumbers = 
    function(x){ 
    ret = gsub("[0-9]","",x) 
    return(ret)
    }
    
#字符删除
removeLiters = 
    function(x){ 
    ret = gsub("[a-z|A-Z]","",x) 
    return(ret)
    }   

#各种操作符处理,\s表示空格,\r表示回车,\n表示换行
removeActions = 
    function(x){
    ret = gsub("\\s|\\r|\\n", "", x)
    return(ret)
    }    
    
nlp_test_data$article=removeNumbers(nlp_test_data$article)
nlp_test_data$article=removeLiters(nlp_test_data$article)

#jieba 分词,去除停顿词
library(jiebaR)
tagger<-worker(stop_word="C:/Program Files/R/R-3.3.3/library/jiebaRD/dict/stop_words.utf8")
words=list()
for (i in 1:nrow(nlp_test_data)){
    tmp=tagger[nlp_test_data[i,2]]
    words=c(words,list(tmp))
}

#词长统计
whole_words_set=unlist(words)
whole_words_set_rank=data.frame(table(whole_words_set))

whole_words_set_dealed=c()
for (i in 1:nrow(whole_words_set_rank)){
    tmp=nchar(as.character(whole_words_set_rank[i,1]))
    whole_words_set_dealed=c(whole_words_set_dealed,tmp)
}
whole_words_set_dealed=cbind(whole_words_set_rank,whole_words_set_dealed)
whole_words_set_dealed=whole_words_set_dealed[whole_words_set_dealed$whole_words_set_dealed>1&whole_words_set_dealed$whole_words_set_dealed<5,]
whole_words_set_dealed=whole_words_set_dealed[order(whole_words_set_dealed$Freq,decreasing=T),]

#words的删除异常值,排序
whole_words_set_sequence=words
for (i in 1:88){
    for (j in 1:length(words[[i]])){
    tmp=ifelse(nchar(words[[i]][j])>1 & nchar(words[[i]][j])<5,words[[i]][j],'')
    whole_words_set_sequence[[i]][j]=tmp
    }
}
for (i in 1:88){
    whole_words_set_sequence[[i]]=whole_words_set_sequence[[i]][whole_words_set_sequence[[i]]!='']
}
----------------------------------------------------------tf-idf排序--------------------------------------------------------------------------
#tf-idf实现，tdidf为重要性，whole_words_set_sequence为对应的词名
#tfidf_partone 为对应的tf
tdidf_partone=whole_words_set_sequence
for (i in 1:88){
tmp1=as.data.frame(prop.table(table(whole_words_set_sequence[[i]])))
tdidf_partone[[i]]=tmp1    
}

#tdidf_partfour 为对应的idf
tdidf_parttwo=unique(unlist(whole_words_set_sequence))
tdidf_max=length(tdidf_parttwo)
tdidf_partthree=tdidf_parttwo
for (i in 1:tdidf_max){
tmp=0
aimed_word=tdidf_parttwo[i]
    for (j in 1:88){
    tmp=tmp+sum(tdidf_parttwo[i] %in% whole_words_set_sequence[[j]])
    }
tdidf_partthree[i]=log(as.numeric(88)/(tmp+1))
}
tdidf_partfour=cbind(tdidf_parttwo,tdidf_partthree)
tdidf_partfive=tdidf_partone
colnames(tdidf_partfour)<-c('Var1','Freq1')
for (i in 1:88){
tdidf_partfive[[i]]=merge(tdidf_partone[[i]],tdidf_partfour,by=c("Var1"))
}

#计算tf-idf结果，并排序key_word
tdidf_partsix=tdidf_partfive
for (i in 1:88){
tmp=tdidf_partfive[[i]][,2:3]
tdidf_partsix[[i]][,2]=as.numeric(tmp[,1])*as.numeric(tmp[,2])
tdidf_partsix[[i]]=tdidf_partsix[[i]][order(tdidf_partsix[[i]][,2],decreasing=T),][]
}

key_word=c()
for (i in 1:88){
tmp=tdidf_partsix[[i]][1:5,1]
key_word=rbind(key_word,as.character(tmp))
}

-----------------------------------------------------------------i-entory---------------------------------------------------------------------




#整合数据
well_dealed_data=cbind(as.character(nlp_test_data[,1]),key_word)
names=as.data.frame(table(key_word))[,1]
names_count=length(names)
names=as.matrix(names,names_count,1)
feature_matrix=matrix(rep(0,names_count*88),88,names_count)
for (i in 1:names_count){
    for(j in 1:88){
    feature_matrix[j,i]=ifelse(names[i] %in% key_word[j,],1,0)
    }
}

#art=1,literature=-1,标签0-1化
feature_matrix=cbind(well_dealed_data[,1],feature_matrix)
feature_matrix[feature_matrix[,1]=='art',1]='1'
feature_matrix[feature_matrix[,1]=='literature',1]='-1'

feature_matrix=as.data.frame(feature_matrix)

num=1:(ncol(feature_matrix)-1)
value_name=paste("feature",num) 
value_name=c('label',value_name)
colnames(feature_matrix)=value_name

#feature0-1化
for (i in 1:ncol(feature_matrix)){
feature_matrix[,i]=as.factor(as.numeric(as.character(feature_matrix[,i])))
}


-----------------------------------------------------------------数据特征整合处理完成---------------------------------------------------------------------
n_index=sample(1:nrow(feature_matrix),round(0.7*nrow(feature_matrix)))
train_feature_matrix=feature_matrix[n_index,]
test_feature_matrix=feature_matrix[-n_index,]

------------------------------------------------------##bp nerual networks
library(nnet)
nn <- nnet(label~., data=train_feature_matrix, size=2, decay=0.01, maxit=1000, linout=F, trace=F)   

#train数据集效果
nn.predict_train = predict(nn,train_feature_matrix,type = "class")
result_combind_train=cbind(as.numeric(as.character(train_feature_matrix$label)),nn.predict_train)
correction_train=nrow(result_combind_train[result_combind_train[,1]==result_combind_train[,2],])/nrow(result_combind_train)

#test数据集效果(最优：0.8076923)  
nn.predict_test = predict(nn,test_feature_matrix,type = "class")
result_combind_test=cbind(as.numeric(as.character(test_feature_matrix$label)),nn.predict_test)
correction_test=nrow(result_combind_test[result_combind_test[,1]==result_combind_test[,2],])/nrow(result_combind_test)



------------------------------------------------------##线性svm支持向量机

library(e1071)
svmfit <- svm(label~., data=train_feature_matrix, kernel = "linear", cost = 10, scale = FALSE) # linear svm, scaling turned OFF

#train数据集效果
svmfit.predict_train=predict(svmfit, train_feature_matrix, type = "probabilities")
result_combind_train=cbind(as.numeric(as.character(train_feature_matrix$label)),as.numeric(as.character(svmfit.predict_train)))
correction_train=nrow(result_combind_train[result_combind_train[,1]==result_combind_train[,2],])/nrow(result_combind_traizn)

#test数据集效果(最优：0.8076923)  
svmfit.predict_test = predict(svmfit,test_feature_matrix,type = "class")
result_combind_test=cbind(as.numeric(as.character(test_feature_matrix$label)),as.numeric(as.character(svmfit.predict_test)))
correction_test=nrow(result_combind_test[result_combind_test[,1]==result_combind_test[,2],])/nrow(result_combind_test)


------------------------------------------------------##贝叶斯分类器
library(e1071)
sms_classifier <- naiveBayes(train_feature_matrix[,-1], train_feature_matrix$label)

#train数据集效果
sms.predict_train=predict(sms_classifier, train_feature_matrix)
result_combind_train=cbind(as.numeric(as.character(train_feature_matrix$label)),as.numeric(as.character(sms.predict_train)))
correction_train=nrow(result_combind_train[result_combind_train[,1]==result_combind_train[,2],])/nrow(result_combind_train)

#test数据集效果(最优：0.8076923)
sms.predict_test = predict(sms_classifier,test_feature_matrix)
result_combind_test=cbind(as.numeric(as.character(test_feature_matrix$label)),as.numeric(as.character(sms.predict_test)))
correction_test=nrow(result_combind_test[result_combind_test[,1]==result_combind_test[,2],])/nrow(result_combind_test)

------------------------------------------------------##randomforest
library(randomForest)
randomForest=randomForest(train_feature_matrix[,-1], train_feature_matrix$label)

#train数据集效果
rf.predict_train=predict(randomForest, train_feature_matrix)
result_combind_train=cbind(as.numeric(as.character(train_feature_matrix$label)),as.numeric(as.character(rf.predict_train)))
correction_train=nrow(result_combind_train[result_combind_train[,1]==result_combind_train[,2],])/nrow(result_combind_train)

#test数据集效果(最优：0.7692308)
rf.predict_test = predict(randomForest,test_feature_matrix)
result_combind_test=cbind(as.numeric(as.character(test_feature_matrix$label)),as.numeric(as.character(rf.predict_test)))
correction_test=nrow(result_combind_test[result_combind_test[,1]==result_combind_test[,2],])/nrow(result_combind_test)


