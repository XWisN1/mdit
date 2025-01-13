from mdit_utils.dir_handler import DirHandler
from mdit_utils.file_handler import FileHandler
from mdit_utils.image_handler import ImageHandler
from mdit_utils.Markdown_image_replacer import MarkdownImageReplacer
from mdit_utils.local_image_mover import LocalImageMover1,LocalImageMover2
from mdit_utils.log_handler import LogHandler
from mdit_utils.network_image_request import NetworkImageRequest


def logic(input_dir, output_dir, image_types, move_method):
    dir_handler = DirHandler(input_dir)
    dirs, files = dir_handler._get_dirs_and_files()
    file_handler = FileHandler(files)
    # md_files = file_handler._extract_md_files()
    # print(f"{file_handler.readme_files}")
    # readme_files = file_handler.readme_files   #后续传入替换操作中去
    image_handler = ImageHandler(file_handler.md_files, image_types)
    # image_info = image_handler._extract_images_md()
    # print(f"{image_info[0]}")

    processed_network_images, processed_local_absolute_images, processed_local_relative_images = image_handler.process_images(file_handler.readme_files)
    # print(f"处理本地绝对路径图片：{processed_local_absolute_images[0:2]},处理本地相对路径图片：{processed_local_relative_images[0:2]}")
    network_image_request = NetworkImageRequest(processed_network_images)
    local_absolute_images = LocalImageMover1(processed_local_absolute_images,move_method)
    local_relative_images = LocalImageMover2(processed_local_relative_images,move_method)
    # print(f"{local_relative_images.mapping[0:2]}")
    if len(local_absolute_images.mapping) > 0:
        print(f"本次绝对路径图片移动成功：{len(local_absolute_images.mapping)}")
    if len(local_relative_images.mapping) > 0:
        print(f"本次相对路径图片移动成功：{len(local_relative_images.mapping)}")
        
    replacer = MarkdownImageReplacer(network_image_request.mapping, local_relative_images.mapping, local_absolute_images.mapping)
    # print(f"替换图片成功：{replacer.processed_data[0:2]}")
    if len(local_absolute_images.missing_images) > 0:
        print(f"本次绝对路径丢失图片：{len(local_absolute_images.missing_images)},请联系相应作者处理,遗失图片路径之一为：{local_absolute_images.missing_images[0]['local_image_path']}")
    if len(local_relative_images.missing_images) > 0:
        print(f"本次相对路径丢失图片：{len(local_relative_images.missing_images)},请联系相应作者处理，遗失图片路径之一为：{local_relative_images.missing_images[0]}")

    
    