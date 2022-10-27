# 开发者： Hei Guang
# 开发时间：2022/10/20 18:19
import os
import shutil
if __name__=="__main__":
    list=[]
    dir='/Volumes/西数S770/2021_malware_feature/'
    for file in os.listdir(dir):
        if file.endswith(".txt"):
            list.append(file.split('_')[0])

    for i in range(1,1218):
        if str(i) in list:
            continue
        else:
            print('缺少的文件号'+str(i))
            shutil.copy('/Volumes/西数S770/2021_malware'+os.sep+str(i)+".apk",
                        '/Volumes/西数S770/2021_malware_incompleted'+os.sep+str(i)+".apk")