import re
str = "3-43工作经验"
ss= re.findall("\d+",str)
print(ss[0])
s1,s2=re.findall("(\d+)-(\d+)",str)[0]
print(s1,s2)

str1= "https://jobs.51job.com/suzhou-gyyq/107794939.html?s=01&t=0"
str2= "https://jobs.51job.com/suzhou/107794939.html?s=01&t=0"

ss=re.match(".*(suzhou.*/\d+.html.*\d+).*",str2)
print(ss.group(1))

str3 = "https://search.51job.com/list/070300,000000,0000,00,9,99,python,2,2.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
ss=re.match(".*(list\S+fare=).*",str3)
print(ss.group(1))

str = "5万以上"
min= re.findall("(\S+)万",str)[0]
print(min)

str = " 本科 "
ss=str.find("本科")
print(ss)
if str.find("大专")!=-1 or str.find(" 本科")!=-1 or str.find("硕士")!=-1 :
    print("哈哈哈")
str = "3-4年工作经验"
if str.find("-")!=-1:
    min,max = re.findall("(\d+)-(\d+)",str)[0]
    print(min,max)

str = "3年经验"
s=re.findall("(\d+)",str)[0]
print(s)