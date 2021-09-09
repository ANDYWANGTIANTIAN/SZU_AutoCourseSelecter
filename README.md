# SZU_AutoCourseSelecter
## 关于本软件
本软件由 [Matt-Dong123](https://github.com/Matt-Dong123) 和 [ANDYWANGTIANTIAN](github.com/ANDYWANGTIANTIAN) 开发制作，可以在深圳大学本科选课系统实现自动选课功能
为方便国内网络环境访问，设立了[镜像站](https://gitee.com/a2309724277/SZU_AutoCourseSelecter) ，如无法访问github，可通过镜像站下载

## 如何使用
### Windows免安装版
免安装版压缩包在项目主页右侧的 [Releases](https://github.com/ANDYWANGTIANTIAN/SZU_AutoCourseSelecter/releases) 栏

解压安装包后，点击main.exe即可运行

### 下载源代码自行打包运行（适用于Windows环境）
1.本地打包运行依赖 PyInstaller 库，安装方法：在控制台输入
```
pip install pyinstaller
```
2.显示以下文字即可（其中的 x.x.x 代表 PyInstaller 的版本）
```
Successfully installed pyinstaller-x.x.x
```
3.使用以下命令生成spec文件(项目中已带有开发者在自己电脑上生成的spec文件(main.spec)，若想直接使用开发者的spec文件，此步可忽略)
```
 pyi-makespec -w main.py
```
4.使用spec执行打包命令
```
pyinstaller -D main.spec
```
5.在dist文件夹内找到main.exe即可运行

## 进一步了解本软件的使用方式
请查看仓库内的 [使用说明.pdf](https://github.com/ANDYWANGTIANTIAN/SZU_AutoCourseSelecter/blob/master/%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E.pdf)
