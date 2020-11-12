# CommitLint

## 背景

多人协作，为了减少合作成本，需对代码风格，commit message等形成统一规范。本文将统一介绍如何用git hook在commit的时候对message的检测。



## CommitLint

现在业内比较推荐的是用CommitLint，详情见[官网](https://commitlint.js.org/)。

### Install

主要是安装node相关module，有全局和局部两种方式

```js
npm install -g @commitlint/cli @commitlint/config-conventional	//全局，路径在/usr/local/lib/node_modules/
npm install -D @commitlint/cli @commitlint/config-conventional  //局部，路径在当前目录
```

### Configure

安装完以后，接下来配置

```js
echo "module.exports = {extends: ['@commitlint/config-conventional']}" > commitlint.config.js
```

在当前目录创建配置文件**commitlint.config.js**

至此，CommitLint就安装配置好了，下面测试一下

```js
echo "test" | commitlint
⧗   input: test
✖   subject may not be empty [subject-empty]
✖   type may not be empty [type-empty]

✖   found 2 problems, 0 warnings
ⓘ   Get help: https://github.com/conventional-changelog/commitlint/#what-is-commitlint
```

如上，如果message不符合规范，下面就会提示报错。

```js
echo "feat: test" | commitlint
```

如果符合规范，则不会有任何提示

commitlint默认的配置在**node_module->@commitlint->config-conventional->index.js**，具体规则如下方

```js
module.exports = {
	parserPreset: 'conventional-changelog-conventionalcommits',
	rules: {
		'body-leading-blank': [1, 'always'],
		'body-max-line-length': [2, 'always', 100],
		'footer-leading-blank': [1, 'always'],
		'footer-max-line-length': [2, 'always', 100],
		'header-max-length': [2, 'always', 100],
		'scope-case': [2, 'always', 'lower-case'],
		'subject-case': [
			2,
			'never',
			['sentence-case', 'start-case', 'pascal-case', 'upper-case'],
		],
		'subject-empty': [2, 'never'],
		'subject-full-stop': [2, 'never', '.'],
		'type-case': [2, 'always', 'lower-case'],
		'type-empty': [2, 'never'],
		'type-enum': [
			2,
			'always',
			[
				'build',
				'chore',
				'ci',
				'docs',
				'feat',
				'fix',
				'perf',
				'refactor',
				'revert',
				'style',
				'test',
			],
		],
	},
};
```

如果需要修改规则，可以在**commitlint.config.js** 添加自己的规则，如下：

```js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Place your rules here
    'type-enum': [2, 'always', ['build', 'chore']], // error if type is given but not in provided list
  }
};
```

修改完规则后，再测试一下

```js
echo "feat: test" | commitlint
⧗   input: feat: test
✖   type must be one of [build, chore] [type-enum]

✖   found 1 problems, 0 warnings
ⓘ   Get help: https://github.com/conventional-changelog/commitlint/#what-is-commitlint
```

这时候就会报错，因为`feat`不在规则列表内，由此可见修改`commitlint.config.js`是覆盖了默认规则。

现在检查规则已经OK了，但是具体要怎么跟git hook结合起来呢？我们可以编辑`.git->hooks`, 但是不利于团队内推广，接下来就需要介绍git hook利器[husky](https://github.com/typicode/husky)



## Husky

husky是一个npm包，安装后，可以很方便的在`package.json`配置`git hook` 脚本 

安装`Husky`之前，需要初始化npm环境，其实就是创建`package.json`文件

```js
npm init -y
{
  "name": "commitlintdemo",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```



### Install

```js
npm install --save-dev husky
```

安装完`husky`，会发现package.json里面的`devDependencies`就会包含`husky`

```js
{
  ...
  "devDependencies": {
    "husky": "^4.3.0"
  },
  ...
}
```

另外可以查看一下`.git->hooks`，多了很多钩子文件，但调用的都是`husky.sh`

```shell
applypatch-msg            post-applypatch           pre-applypatch            pre-push                  push-to-checkout
applypatch-msg.sample     post-checkout             pre-applypatch.sample     pre-push.sample           sendemail-validate
commit-msg                post-commit               pre-auto-gc               pre-rebase                update.sample
commit-msg.sample         post-merge                pre-commit                pre-rebase.sample
fsmonitor-watchman.sample post-rewrite              pre-commit.sample         pre-receive.sample
husky.local.sh            post-update               pre-merge-commit          prepare-commit-msg
husky.sh                  post-update.sample        pre-merge-commit.sample   prepare-commit-msg.sample
```

到这里还没完，如果需要`husky`和`commitlint`联动起来，还需要在`package.json`里面添加

```js
{
	...
	"husky": {
    "hooks": {
      "commit-msg": "commitlint -E HUSKY_GIT_PARAMS"
    }
  }
}
```

至此，如果在提交commit 信息不规范的时候，就会报错啦。

```js
git commit -m "feat: a"
⧗   input: a
✖   subject may not be empty [subject-empty]
✖   type may not be empty [type-empty]

✖   found 2 problems, 0 warnings
ⓘ   Get help: https://github.com/conventional-changelog/commitlint/#what-is-commitlint

husky > commit-msg hook failed (add --no-verify to bypass)
```

要输入符合规范的message才能提交成功

```js
git commit -m "feat: update"
```

