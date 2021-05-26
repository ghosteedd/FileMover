# FileMover

![](https://img.shields.io/appveyor/ci/gruntjs/grunt.svg)![](https://img.shields.io/badge/platform-*nix%20%7C%20windows-lightgrey)![](https://img.shields.io/badge/python-3.6%2B-blue)![](https://img.shields.io/badge/license-MIT-orange.svg)

FileMover это небольшой скрипт, позволяющий переносить файлы между локальными и примонтированными хранилищами и осуществлять их ротацию. 

##  Аргументы запуска

* -s - исходный файл, который будет скопирован/перемещён

* -t - целевая директория, в которой будет помещён файл и выполнена ротация

* -f - имя файла в целевой директории (при ротации будет добавлен постфикс вида `.N`)

* -l - кол-во последних копий файла (по умолчанию: 7)

* -c - выполнить копирование исходного файла, а не его перенос

* -comp - при совпадении нового файла с последней копией не добавлять этот файл в коллекцию

## Пример использования

### Windows

Перемещение файла `backup.bak` из smb шары `\\192.168.0.1\Backups` в директорию `E:\Backups` c максимальным количеством копий: 3:

```
net use \\192.168.0.1\Backups password /user:username
file-mover.exe -s "\\192.168.0.1\Backups\backup.bak" -t "E:\Backups" -f "backup.bak" -l 3
net use \\192.168.0.1\Backups /delete /y
```

**ВНИМАНИЕ!** При указывании пути не используйте комбинацию `\"` или `\'` в конце.

### Linux

Перемещение файла `file.data` из примонтированной директории `/data` в директорию `/var/backups/` с сохранением исходного файла:

```
python3 file-mover.py -s "/data/file.data" -t "/var/backups" -f "file.data.bak"
```