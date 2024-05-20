# 教务系统课程表爬虫
该项目用于爬取 [福州职业技术学院](https://www.fvti.cn/) 教务系统学生端的课程表信息，并以截图形式保存至项目根目录。截图命名规则为“学年+学期+周次+专业代码.png”。 
## 快速开始
1. **环境准备**
- 确保安装Python3.8+。
- 安装依赖：运行 `pip install -r requirements.txt` 。
2. **配置Edge WebDriver**
- 下载与Edge浏览器版本匹配的 [Microsoft Edge WebDriver](https://developer.microsoft.com/microsoft-edge/tools/webdriver/) 。
- 将下载的`MicrosoftWebDriver.exe`放置于项目根目录，并重命名为`MicrosoftWebDriver.exe`。

> 查看驱动器版本：
> 1. 方法一：在命令行中输入： `MicrosoftWebDriver.exe -version` 。
> 2. 方法二：直接双击运行`MicrosoftWebDriver.exe`

> 查看浏览器版本：
> 1. 打开Microsoft Edge。
> 2. 选择右上角的“设置及更多”，然后选择“设置”。
> 3. 在“关于此应用”下查找你的版本。
3. **输入信息**
- 临时输入：直接从命令行输入账号密码等信息
- 持久化输入：从 [文件](student.json) 中读取账号密码等信息
- 1. 已提供 `student.json.template` 模板文件

```json
{
  "login": [
    {
      "username": "",
      "password": ""
    }
  ],
  "kcb": [
    {
      "xn": "",
      "xq": "",
      "dqz": "",
      "sybmdmstr": ""
    }
  ]
}
```
- 2. 填入账号密码等信息
- 3. 重命名为 `student.json`
## 功能特性
- **模拟登录**：使用`selenium`实现自动化登录。
- **验证码识别**：集成`ddddocr`库识别登录验证码。
- **截图保存**：自动抓取并保存课程表截图。
## 安装
1. 从 [Releases](https://github.com/Bonger34/CourseTableCrawler-EDU/releases) 下载安装包安装。
2. 从源码安装。

    如果使用 `pyinstaller` 打包成 `.exe` 文件，需要添加一个动态库和一个模型文件：
    
    `onnxruntime_providers_shared.dll`和`common_old.onnx`
    
    可参考以下 `.spec` 文件示例：
    ```
    # -*- mode: python ; coding: utf-8 -*-
    
    
    a = Analysis(
        ['schedule.py'],
        pathex=[],
        binaries=[],
        datas=[('D:/Python/Python38/Lib/site-packages/onnxruntime/capi/onnxruntime_providers_shared.dll','onnxruntime/capi/'), ('D:/Python/Python38/Lib/site-packages/ddddocr/common_old.onnx', 'ddddocr/')],
        hiddenimports=[],
        hookspath=[],
        hooksconfig={},
        runtime_hooks=[],
        excludes=[],
        noarchive=False,
        optimize=0,
    )
    pyz = PYZ(a.pure)
    
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name='schedule',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=True,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )
    
    ```
    需要根据环境调整自己的路径，或者使用 [`--add-data`](https://pyinstaller.org/en/stable/usage.html#cmdoption-add-data)选项打包

如有疑问或遇到问题，欢迎查阅项目文档或联系开发者寻求帮助。