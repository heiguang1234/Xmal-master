# 开发者： Hei Guang
# 开发时间：2022/10/20 20:28
import csv
import os

if __name__ == '__main__':
    dir = '/Volumes/西数S770/2022_malware_feature'
    list=[]
    i = 0
    for file in os.listdir(dir):
        if "API" in file:
            i = i + 1
            try:
                with open(dir + os.sep + file, 'r', encoding='utf8') as fp:
                    line = fp.readline().split(';')[0]
                    while line:
                        if 'androidx' in line and line not in list:
                            with open("logsuccess.txt","a") as success:
                                success.write(line.replace('/','.').strip('L')+"\n")
                            list.append(line)
                            print(line)
                        line = fp.readline().split(';')[0]
                fp.close()
            except Exception as e:
                with open("logerror.txt",'a') as record:
                    record.write(str(e)+"\t\t\t\t"+file+"\n")


print('已经解析' + str(i) + "个文件")
print('解析出得api为：'+'\n'+list)