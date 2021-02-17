import os

# 检查文件夹内文件数量
def check_file_num(path):
    folders = os.listdir(path)
    for folder in folders:
        true_folder = path + folder
        files = os.listdir(true_folder)
        if len(files) < 5:
            print(folder)


def check_size(path):
    folders = os.listdir(path)
    for folder in folders:
        true_folder = path + folder
        files = os.listdir(true_folder)
        find = False
        for file in files:
            true_file = true_folder + '/' + file
            size = os.path.getsize(true_file)
            if size < 100:
                find = True
        if find:
            print(true_folder)

if __name__ == '__main__':
    folder_path = 'D:/文件/漫画/春哥传/'
    # check_file_num(folder_path)
    check_size(folder_path)