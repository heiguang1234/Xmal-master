# -*- coding: utf-8 -*-
import sys
import os
import shutil
from multiprocessing import Process,Manager,Lock
import random

# sys.path.append("."+os.sep+'log')
# from log import Log
from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis
from androguard.core.bytecodes.apk import APK
import re
import logging

def Log(self):
	"""log"""
	logPath = "log.txt"
	logger = logging.getLogger("RESULT")
	logger.setLevel(logging.INFO)
	if not logger.handlers:
		formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
		file_handler = logging.FileHandler(logPath)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)
	return logger


class GetAPI:
	def __init__(self):
		"""
		init
		:param file:
		:return:
		"""
		self.logger = Log(self)

	def getAPICalls(self, Path, fileName, dataPath):
		"""
		get the API Calls
		:param Path: the APK folder path
		:param fileNmae: the APK Nmae
		:param dataPath: the folder path where the api files save
		:return: api files
		"""
		filePath = Path + os.sep + fileName
		self.logger.info("Extract" + fileName + "API calls")
		print("Extract" + fileName + "API calls")
		app = APK(filePath)
		app_dex = dvm.DalvikVMFormat(app.get_dex())
		app_x = analysis.Analysis(app_dex)
		APIs = list()

		classes = [cc.get_name() for cc in app_dex.get_classes()]
		for method in app_dex.get_methods():
			methodBlock = app_x.get_method(method)
			if method.get_code() == None:
				continue
			for i in methodBlock.get_basic_blocks().get():
				for ins in i.get_instructions():
					output = ins.get_output()
					match = re.search(r'(L[^;]*;)->([^\(]*)', output)
					if match and match.group(1) not in classes:
						# print "API: "+match.group()+"	 "+match.group(1)
						if match.group(2) == "<init>":
							continue
						api = match.group()
						if api in APIs:
							continue
						else:
							APIs.append(api)

		name = fileName.replace(".apk", "")
		with open(dataPath + os.sep + name + "_API.txt", 'w') as f:
			print("Saving " + fileName + " APIs")
			self.logger.info("Saving " + fileName + " APIs")
			for i in range(APIs.__len__()):
				f.write(APIs[i] + "\n")

class GetPermission:
	def __init__(self):
		"""init params"""
		self.logger = Log(self)

	def getPermissions(self, Path, fileName, dataPath):
		"""
		get the API Calls
		:param Path: the APK folder path
		:param fileNmae: the APK Nmae
		:param dataPath: the folder path where the permission files save
		:return: permission files
		"""
		filePath = Path + os.sep + fileName
		self.logger.info("Extract" + fileName + " Permissions")
		print("Extract" + fileName + "Permissions")
		app = APK(filePath)
		permissions = app.get_permissions()
		name = fileName.replace(".apk", "")
		with open(dataPath + os.sep + name + "_Permission.txt", 'w') as f:
			self.logger.info("Saving" + fileName + " Permissions")
			print("Saving" + fileName + "Permissions")
			for i in range(permissions.__len__()):
				f.write(permissions[i] + "\n")


class FeatureExtraction:
	def __init__(self):
		"""init params"""
		self.logger=Log(self)
		self.apk=".."+os.sep+"apk"

	# 	文件夹中的文件（遍历文件）
	def filesInFolder(self, folderPath, suffix):
		"""
		get the files in folderPath
		:param folderPath: the folder path
		:param suffix: the file extension
		:return: files list
		"""
		self.logger.info("Traversing " + folderPath + " folder")
		# 检测文件路径是否存在
		if not os.path.exists(folderPath):
			self.logger.error(folderPath + "does not exist")
			return
		# 将文件夹中的文件加进列表
		files = os.listdir(folderPath)
		suit = list()
		for file in files:
			if file.endswith(suffix):
				suit.append(file)
		return suit		

	# 获得文件地址Apkpath，根据文件名进行处理并放进Datapath
	def getFeature(self,Apkpath,apk,Datapath):
		"""
		get features from apk
		:param Apkpath: APK file folder path
		:param apk: apk name
		:param Datapath: the folder where the feature files save
		:return:
		"""
		GetAPIClass = GetAPI()
		GetPermissionClass = GetPermission()
		'''
		获得两个接口
		'''
		try:
			'''
			开始提取api和permission
			'''
			GetAPIClass.getAPICalls(Apkpath,apk,Datapath)
			GetPermissionClass.getPermissions(Apkpath,apk,Datapath)
		except Exception as e:
			# 将后缀.apk替换成''（去掉.apk）
			name = apk.replace(".apk", "")
			permissionName = Datapath+os.sep+name+"_Permission.txt"
			if os.path.exists(permissionName):
				os.remove(permissionName)
			apiName=Datapath+os.sep+name+"_API.txt"
			if os.path.exists(apiName):
				os.remove(apiName)
			self.logger.info(apk+"Features Extraction errors.")
			print(apk+"Features Extraction errors.")

		
	def getFeatures(self,Apkpath,apks,Datapath,fileLock,getfile):
		"""
		get features from apks
		:param Apkpath: APK file folder path
		:param apk: apk name
		:param Datapath: the folder where the feature files save
		:param fileLock: multiple process lock  多进程锁
		:param getfile: the list of the apk files that have been extracted  已经提取过的apk
		:return:
		"""
		random.shuffle(apks)
		
		for apk in apks:
			fileLock.acquire()
			if apk not in getfile:
				getfile.append(apk)
				fileLock.release()
				self.getFeature(Apkpath,apk,Datapath)
			else:
				fileLock.release()
			
		
	def productFeature(self,benApkpath,malApkPath,benDatapath,malDatapath):
		"""
		get features from apks by multi-process
		:param benApkpath: benign APK file folder path
		:param malApkPath: malicious APK file folder path
		:param benDatapath: the folder where the feature files of benign APKs save
		:param malDatapath: the folder where the feature files of malicious APKs save
		:return:
		"""
		BenFileLock = Lock()
		MalFileLock = Lock()

		m = Manager()
		getBenFile = m.list()
		getMalFile = m.list()


		""" from APK folder to product the feature
		检索两个路径下的良性和恶意样本（以后缀.apk进行鉴别）
		"""
		benApks = self.filesInFolder(benApkpath, ".apk")
		malApks = self.filesInFolder(malApkPath, ".apk")

		'''
		启动恶意检测线程和良性检测线程
		'''
		bthreads = []
		mthreads = []
		
		for i in range(0):
			bthread= Process(target=self.getFeatures, args=(benApkpath,benApks,benDatapath,BenFileLock,getBenFile) )
			bthreads.append(bthread)
		
		for i in range(6):
			mthread= Process(target=self.getFeatures, args=(malApkPath,malApks,malDatapath,MalFileLock,getMalFile) )
			mthreads.append(mthread)
			
		for bthread in bthreads:
			bthread.start()
		for mthread in mthreads:
			mthread.start()
		
		for bthread in bthreads:
			bthread.join()
		for mthread in mthreads:
			mthread.join()
		print("exists multi-process")




if __name__=='__main__':
	adapter = FeatureExtraction()
	adapter.productFeature('/Volumes/西数S770/2021_benign','/Volumes/西数S770/2022_malware_incompeleted','/Volumes/西数S770/2021_benign_feature','/Volumes/西数S770/2022_malware_feature')
				
