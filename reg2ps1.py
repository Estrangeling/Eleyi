import os, re, sys

def reg2ps1(args):
    
    hive = {
        'HKEY_CLASSES_ROOT':   'HKCR:',
        'HKEY_CURRENT_CONFIG': 'HKCC:',
        'HKEY_CURRENT_USER':   'HKCU:',
        'HKEY_LOCAL_MACHINE':  'HKLM:',
        'HKEY_USERS':          'HKU:'
    }
    
    addedpath = []
    args = rf'{args}'
    
    if os.path.exists(args) and os.path.isfile(args) and args.endswith('.reg'):
        commands = []
        f = open(args, 'r', encoding='utf-16')
        content = f.read()
        f.close()
        for r in hive.keys():
            if r in content and hive[r] not in ['HKCU:', 'HKLM:']:
                commands.append("New-PSDrive -Name {0} -PSProvider Registry -Root {1}".format(hive[r].replace(':', ''), r))
        filecontent = []
        for line in content.splitlines():
            if line != '':
                filecontent.append(line.strip())
        
        text = ''
        joinedlines = []
        
        for line in filecontent:
            if line.endswith('\\'):
                text = text + line.replace('\\', '')
            else:
                joinedlines.append(text + line)
                text = ''
        
        for joinedline in joinedlines:
            if re.search('\[HKEY(.*)+\]', joinedline):
                key = re.sub('\[-?|\]', '', joinedline)
                hivename = key.split('\\')[0]
                key = '"' + (key.replace(hivename, hive[hivename])) + '"'
                if joinedline.startswith('[-HKEY'):
                    commands.append(f'Remove-Item -Path {key} -Force -Recurse -ErrorAction SilentlyContinue')
                else:
                    if key not in addedpath:
                        commands.append(f'New-Item -Path {key} -ErrorAction SilentlyContinue | Out-Null')
                        addedpath.append(key)
            elif re.search('"([^"=]+)"=', joinedline):
                delete = False
                name = re.search('("[^"=]+")=', joinedline).groups()[0]
                if '=-' in joinedline:
                    commands.append(f'Remove-ItemProperty -Path {key} -Name {name} -Force')
                    delete = True
                elif '"="' in joinedline:
                    vtype = 'String'
                    value = re.sub('"([^"=]+)"=', '', joinedline)
                elif 'dword' in joinedline:
                    vtype = 'Dword'
                    value = '0x' + re.sub('"([^"=]+)"=dword:', '', joinedline)
                elif 'qword' in joinedline:
                    vtype = 'QWord'
                    value = '0x' + re.sub('"([^"=]+)"=qword:', '', joinedline)
                elif re.search('hex(\([2,7,b]\))?:', joinedline):
                    value = re.sub('"([^"=]+)"=hex(\([2,7,b]\))?:', '', joinedline).split(',')
                    hextype = re.search('(hex(\([2,7,b]\))?)', joinedline).groups()[0]
                    if hextype == 'hex(2)':
                        vtype = 'ExpandString'
                        chars = []
                        for i in range(0, len(value), 2):
                            if value[i] != '00':
                                chars.append(bytes.fromhex(value[i]).decode('utf-8'))
                        value = '"' + ''.join(chars) + '"'
                    elif hextype == 'hex(7)':
                        vtype = 'MultiString'
                        chars = []
                        for i in range(0, len(value), 2):
                            if value[i] != '00':
                                chars.append(bytes.fromhex(value[i]).decode('utf-8'))
                            else:
                                chars.append(',')
                        chars0 = (''.join(chars)).split(',')
                        chars.clear()
                        for i in chars0:
                            chars.append('"' + i + '"')
                        value = '@(' + ','.join(chars).replace(',"",""', '') + ')'
                    elif hextype == 'hex(b)':
                        vtype = 'QWord'
                        value.reverse()
                        value = '0x' + ''.join(value).lstrip('0')
                    elif hextype == 'hex':
                        vtype = 'Binary'
                        value1 = []
                        for i in value:
                            value1.append('0x' + i)
                        value = '([byte[]]$(' + ','.join(value1) + '))'
                if not delete:
                    if '@=' in joinedline:
                        value = joinedline.replace('@=', '')
                        commands.append(f'Set-ItemProperty -Path {key} -Name "(Default)" -Type "String" -Value {value}')
                    else:
                        commands.append('Set-ItemProperty -Path {0} -Name {1} -Type {2} -Value {3} -Force'.format(key, name, vtype, value))
        filename = args.replace('.reg', '_reg.ps1')
        output = open(filename, 'w+')
        print(*commands, sep='\n', file=output)
        output.close()

if __name__ == '__main__':
    reg2ps1(sys.argv[1])
