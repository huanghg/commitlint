#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

import os

def isRootDir():
	return os.path.exists(".git")

# npm init
def npmInit():
	if not os.path.exists("package.json"):
		print "init npm now"
		os.system("npm init -y")
		print "init npm finished"
		pass
	pass

def installCommitLint():
	if not os.path.exists("node_modules/@commitlint"):
		print "install CommitLint now"
		os.system("npm install -D @commitlint/cli @commitlint/config-conventional")
		print "install CommitLint finished"
		pass
	pass

def exportCommitLint():
	if not os.path.exists("commitlint.config.js"):
		print "export CommitLint now"
		os.system("echo \"module.exports = {extends: ['@commitlint/config-conventional']};\" > commitlint.config.js")
		print "export CommitLint finished"
		pass
	pass

def installHusky():
	if not os.path.exists("node_modules/husky"):
		print "install husky now"
		os.system("npm install --save-dev husky")
		print "export CommitLint finished"

		#配置 husky
		setupHusky()
		pass
	pass

def setupHusky():
	jsonData = {}
	with open("package.json",'rb') as f1:
		params = json.load(f1)
		if params.has_key("devDependencies") == False:
			params["devDependencies"] = { 'husky': "^4.3.0" }
		else:
			devDependencies = params["devDependencies"]
			devDependencies["husky"] = "^4.3.0"		#这里的版本最好动态获取
			pass

		if params.has_key("husky") == False:
			params["husky"] = { 'hooks': {'commit-msg': 'commitlint -E HUSKY_GIT_PARAMS' }}
		else:
			husky = params["husky"]
			if husky.has_key("hooks") == False:
				husky["hook"] = { 'commit-msg': 'commitlint -E HUSKY_GIT_PARAMS' }
			else:
				hooks = husky["hooks"]
				hooks['commit-msg'] = 'commitlint -E HUSKY_GIT_PARAMS'
			pass
		pass
		jsonData = json.dumps(params, separators=(',', ': '))
	f1.close()

	with open("package.json",'w') as f2:
		f2.write(str(jsonData))
	f2.close()

	pass

def setuphook():
	if not os.path.exists(os.environ['HOME']+"/.git_template"):
		print "start clone git_template"
		os.system("git clone http://git.code.oa.com/VBank-APP/git_template ~/.git_template")
		os.system("git config --global init.templatedir '~/.git_template/template'")
		os.system("git init")
		pass
	pass

def modifygitignore():
	if os.path.exists(".gitignore"):
		print "start modify .gitignore"
		ignoreDict = {'commitlint.config.js':False, 'node_modules':False, 'package.json':False, 'package-lock.json':False}
		with open(".gitignore", "r") as f:
			for line in f.readlines():
				for key in ignoreDict.keys():
					if key in line:
						ignoreDict[key] = True
					pass
				pass
		f.close()

		with open(".gitignore", "a") as f:
			for item in ignoreDict.items():
				if item[1] == False:
					f.write(str(item[0]+"\n"))
					pass
		f.close()
	else:
		print "❌没找到gitignore文件"
	pass

def commit():
	os.system("git add .")
	os.system("git commit -m 'feat: install commitlint'")
	pass

def setup():
	if not isRootDir():
		print "❌请去工程主目录"
		return

	#npm initialize
	npmInit()

	#判断需不需要安装commitlint
	installCommitLint()

	#export commitlint
	exportCommitLint()

	#安装 husky
	installHusky()

	setuphook()

	modifygitignore()

	commit() 

	pass

if __name__ == "__main__":
	setup()