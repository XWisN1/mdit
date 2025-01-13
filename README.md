#### 1.目的：

- 解决markdown文件中网络图片引用问题，将文件中所有的图片都更改为本地指定路径的图片引用。
- 无论原路径是网络的，还是本地的，都移动到指定目录下，并将原路径替换为新路径。
- 本地的相对路径不替换，只替换绝对路径

#### 2.使用方法：

- 将代码移动到指定的目录下

- 在命令行中进入该目录，执行命令：

  ```
  pip install -r requirements.txt
  
  mv contain_http_md_files mdit/
  
  python mdit.py
  ```

#### 3.参数解析：

- -i：指定markdown文件所在目录，默认为当前目录
- -o：指定图片移动后的目录，默认为contain_http_md_files下的README.md文件的路径（可能没用了）
- -t：指定图片类型，默认为png和jpg，可选jpg、jpeg、gif、svg、webp等
- -m：指定移动方式，默认为move，可选copy、link、symlink等
- -h：显示帮助信息

#### 4.注意事项：

- 图片移动后，原文件中的图片引用路径将被替换为新路径。
- 图片移动后，替换信息将会被记录在mdit_images.log文件中。
