import os

DEFAULT_EXTENSION = 'rst'

def expand_tree(path, input_extension=DEFAULT_EXTENSION):
    file_list = []
    for root, subFolders, files in os.walk(path):
        for file in files:
            f = os.path.join(root,file)

            if f.rsplit('.', 1)[1] == input_extension:
                file_list.append(f)

    return file_list

if __name__ == '__main__':
    pass
