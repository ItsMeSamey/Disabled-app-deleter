import command
import os
all_packages = str(command.run('adb shell pm list packages -s -u -f'.split(' ')).output.decode("utf-8")).splitlines()
installed_packages = str(command.run('adb shell pm list packages -s -f'.split(' ')).output.decode("utf-8")).splitlines()
uninstalled_packages = []
for i in all_packages:
    if installed_packages.count(i) == 0:
        j = i.lstrip('package:').split('.apk=')
        appname = j[0].split('/')[-2]
        k = [j[0].rstrip('/'+appname+'/'),appname,j[1]]
        if k[0].find('/system/') != -1:
            k[0] = '/system_root'+k[0]
        uninstalled_packages.append(k[:])


script = open('remover.sh','w')
script.write('umount -a\n')
script.write('mount -rw -a\n')


for num in range(len(uninstalled_packages)):
    i = uninstalled_packages[num]
    yess = str(input(f'{i[1]} ({i[2]})\nY/N/Q (↩ = Y): '))
    if yess.upper() == 'Q':
        script.close()
        quit()
    elif yess.upper() == 'Y' or yess == '':
        script.write(f'rm -rf {i[0]}\n')

script.close()