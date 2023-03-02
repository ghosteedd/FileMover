#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import hashlib
import shutil
import sys
import os


def check_access_to_file(path: str):
    if not os.path.exists(path):
        return 'Error! File not found or permission denied!'
    if os.path.isdir(path):
        return 'Error! This path is directory!'
    try:
        file = open(path, 'r')
        file.close()
    except PermissionError:
        return f'Error reading file!'
    return 0


def move_or_copy_file(source_path: str, target_path: str, move_file: bool = True):
    if not os.path.exists(source_path):
        return 'Source file not found or permission denied!'
    if os.path.exists(target_path):
        try:
            os.remove(target_path)
        except PermissionError:
            return 'Permission denied on target file!'
    try:
        if move_file:
            shutil.move(source_path, target_path)
        else:
            shutil.copy(source_path, target_path)
        return 0
    except PermissionError:
        return f'File permission denied! ({sys.exc_info()[1].filename})'
    except Exception as e:
        return 'Error! ' + str(e)


def rotate_files(dir_path, limit: int, file_prefix: str = '', file_postfix: str = '', new_file: str = ''):
    if limit < 2:
        return 'Error rotating files!'
    if limit == 1:
        if os.path.exists(dir_path + new_file):
            try:
                os.remove(dir_path + new_file)
            except PermissionError:
                return f'File permission denied! ({sys.exc_info()[1].filename})'

    if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
        return 'Target path not exist!'
    last_file = limit
    for i in range(limit - 1, 0, -1):
        if os.path.exists(dir_path + file_prefix + str(i) + file_postfix):
            last_file = i
            break
    if last_file == limit - 1:
        try:
            os.remove(dir_path + file_prefix + str(last_file) + file_postfix)
        except PermissionError:
            return f'File permission denied! ({sys.exc_info()[1].filename})'
        except FileNotFoundError:
            return 'File ' + file_prefix + str(last_file) + file_postfix + ' not found!'

    for i in range(limit - 2, 0, -1):
        try:
            if os.path.exists(dir_path + file_prefix + str(i) + file_postfix):
                shutil.move(dir_path + file_prefix + str(i) + file_postfix,
                            dir_path + file_prefix + str(i + 1) + file_postfix)
        except PermissionError:
            return f'Error! File permission denied! ({sys.exc_info()[1].filename})'

    if os.path.exists(dir_path + new_file):
        try:
            shutil.move(dir_path + new_file, dir_path + file_prefix + '1' + file_postfix)
        except PermissionError:
            return f'Error! File permission denied! ({sys.exc_info()[1].filename})'
    return 0


def get_file_hash(file_path: str):
    buffer_size = 65536  # 64Kb
    md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(buffer_size)
                if not data:
                    break
                md5.update(data)
    except PermissionError:
        return -1, f'File permission denied! ({sys.exc_info()[1].filename})'
    except FileNotFoundError:
        return -1, f'File not found! ({sys.exc_info()[1].filename})'
    return 0, md5.hexdigest()


def delete_file(file_path: str):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        return f'File not found! ({sys.exc_info()[1].filename})'
    except PermissionError:
        return f'File permission denied! ({sys.exc_info()[1].filename})'
    return 0


def main():
    parser = argparse.ArgumentParser(description='Copy/move and rotating files v1.0  //  '
                                                 'https://github.com/ghosteedd/FileMover')
    parser.add_argument('-s', '--source', type=str, required=True, help='source file')
    parser.add_argument('-t', '--target', type=str, required=True, help='target path')
    parser.add_argument('-f', '--file-name', type=str, required=True, help='file name in target path')
    parser.add_argument('-l', '--limit', type=int, default=7, help='files limit in target path')
    parser.add_argument('-c', '--copy', action='store_true', help='don\'t delete source file')
    parser.add_argument('-comp', '--comparison', action='store_true',
                        help='enable comparison source file and newest file in target path. '
                             'If files is equal don\'t rotate files'
                        )
    args = parser.parse_args()
    print('Checking source file...')
    check_result = check_access_to_file(args.source)
    if check_result != 0:
        print(check_result)
        sys.exit(1)
    else:
        print('Done!')
    if args.copy:
        print('Coping new file to temporary path...')
    else:
        print('Moving new file to temporary path...')
    file_move_result = move_or_copy_file(args.source, args.target + '/tmp', not args.copy)
    if file_move_result != 0:
        print(file_move_result)
        sys.exit(2)
    else:
        print('Done!')
    if args.comparison:
        print('File comparison...')
        hash_src_result = get_file_hash(args.target + '/tmp')
        hash_target_result = get_file_hash(args.target + '/' + args.file_name)
        if hash_src_result[0] == 0 or hash_target_result[0] == 0:
            if hash_src_result[1] == hash_target_result[1]:
                print(f'new file = {args.file_name}')
                delete_file_result = delete_file(args.target + '/tmp')
                if delete_file_result == 0:
                    print('Exiting')
                    sys.exit(0)
                else:
                    print(delete_file_result)
                    sys.exit(3)
        print('Done!')
    print('Rotate files...')
    rotate_files_result = rotate_files(args.target + '/', args.limit, args.file_name + '.', '', args.file_name)
    if rotate_files_result != 0:
        print(rotate_files_result)
        sys.exit(7)
    else:
        print('Done!')
    print('Moving new file from temporary path...')
    file_move_result = move_or_copy_file(args.target + '/tmp', args.target + '/' + args.file_name, True)
    if file_move_result != 0:
        print(file_move_result)
        sys.exit(4)
    else:
        print('Done!')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
