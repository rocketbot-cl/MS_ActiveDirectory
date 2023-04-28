# coding: utf-8
"""
Base para desarrollo de módulos externos.
Para obtener el modulo/Función que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opción seleccionada:
    opcion = GetParams("option")


Para instalar librerías se debe ingresar por terminal a la carpeta "libs"
    
   sudo pip install <package> -t .

"""

import sys
import os
import traceback

base_path = tmp_global_obj["basepath"]
cur_path = base_path + "modules" + os.sep + "MS_ActiveDirectory" + os.sep + "libs" + os.sep
if cur_path not in sys.path:
    sys.path.append(cur_path)

from ldap3 import Server, Connection, ALL, MODIFY_ADD, MODIFY_REPLACE, SUBTREE, extend, Tls
from ldap3.core.exceptions import LDAPEntryAlreadyExistsResult
from ldap3.utils.hashed import hashed
from ldap3.extend.standard.modifyPassword import ModifyPassword
import ssl

global mod_ms_activedirectory 

module = GetParams("module")

if module == "connect":

    domain = GetParams("domain")
    username = GetParams("username")
    password = GetParams("password")
    var_ = GetParams("var_")
    base = GetParams("base")
    try:
        # Define the server and connection details
        tls_config = Tls(validate=ssl.CERT_NONE)
        server = Server(domain, get_info=ALL, use_ssl=True, tls=tls_config)
        conn = Connection(server, user=username, password=password)

        # Bind to the server
        conn.bind()
        
        mod_ms_activedirectory = {"connection": conn, "base": base, "description": conn.result["description"]}
        SetVar(var_, "invalidCredentials" not in conn.result["description"])
    except Exception as e:
        SetVar(var_, False)
        PrintException()
        traceback.print_exc()
        raise e
    
if module == "run_query":
    query = GetParams("query")
    response = GetParams("response")
    var_ = GetParams("var_")

    import re
    import datetime
    from ldap3.core.timezone import OffsetTzInfo
    
    if "success" not in mod_ms_activedirectory.get("description"):
        raise Exception(mod_ms_activedirectory.get("description"))
    if response and response != "":
        response = response.split(',')
    else:
        response ['cn', 'givenName', 'sn', 'userPrincipalName', 'sAMAccountName', 'userAccountControl']
    
    try:
        conn = mod_ms_activedirectory.get("connection")
        base = mod_ms_activedirectory.get("base")
        conn.search(base, query, attributes=response)
        
        entries = [{"dn": entry.entry_dn, **entry.entry_attributes_as_dict} for entry in conn.entries]
        
        data_str = str(entries)
        
        regex = r"datetime\.datetime\(\d{4},\s\d{1,2},\s\d{1,2},\s\d{1,2},\s?\d{0,2},\s?\d{0,2},?\s?\d{0,6},?\stzinfo=OffsetTzInfo\(offset=\d+,\sname='[A-Za-z0-9]+'\)\)"
        
        matches = re.finditer(regex, str(entries), re.MULTILINE)
        
        for match in matches:
            data_str = data_str.replace(match.group(), '"{}"'.format(eval(match.group()).strftime("%d/%m/%Y")))
        
        SetVar(var_, data_str)
    except Exception as e:
        SerVar(var_, False)
        PrintException()
        traceback.print_exc()
        raise e

if module == "enable_disable_user":

    user = GetParams("username")
    action = GetParams("action")
    
    try:
        conn = mod_ms_activedirectory.get("connection")
        base = mod_ms_activedirectory.get("base")
        
        if '@' in user:
            query = f'(UserPrincipalName={user})'
            conn.search(base, query, attributes=['distinguishedName'])
            dn = conn.entries[0].distinguishedName
        else:
            dn = user
        
        if action == "":
            raise Exception("Must select an action...")
        else:
            conn.modify(dn, {'userAccountControl': [(MODIFY_REPLACE, [eval(action)])]})
        
        #conn.modify(user, {'ibm-pwdAccountLocked': [(MODIFY_REPLACE, [True])]})

    except Exception as e:
        traceback.print_exc()
        PrintException()
        raise e


if module == "unlock_user":

    user = GetParams("username")

    try:
        conn = mod_ms_activedirectory.get("connection")
        base = mod_ms_activedirectory.get("base")
        
        if '@' in user:
            query = f'(UserPrincipalName={user})'
            conn.search(base, query, attributes=['distinguishedName'])
            dn = conn.entries[0].distinguishedName
        else:
            dn = user
        
        conn.extend.microsoft.unlock_account(dn)

    except Exception as e:
        traceback.print_exc()
        PrintException()
        raise e

if module == "change_password":
    username = GetParams("username")
    password = GetParams("password")
    server = GetParams("server")
    user = GetParams("user")
    new_password = GetParams("new_password")
    
    import subprocess
    
    try:
        conn = mod_ms_activedirectory.get("connection")
        base = mod_ms_activedirectory.get("base")
        
        if '@' in user:
            query = f'(UserPrincipalName={user})'
            conn.search(base, query, attributes=['cn', 'givenName', 'userPrincipalName'])
            
            for entry in conn.response:
                if entry.get("dn") and entry.get("attributes"):
                    if entry.get("attributes").get("userPrincipalName"):
                        if entry.get("attributes").get("userPrincipalName") == user:
                            dn=entry.get("dn")
        else:
            dn = user
        
        if username and password and server:
            command =f"""$User = "{username}"
            $PWord = ConvertTo-SecureString -String "{password}" -AsPlainText -Force
            $Credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $User, $PWord
            Set-ADAccountPassword -Server "{server}" -Credential $Credential -Identity '{dn}' -Reset -NewPassword (ConvertTo-SecureString -AsPlainText \"{new_password}\" -Force)"""
        else:
            command = f"Set-ADAccountPassword -Identity '{dn}' -Reset -NewPassword (ConvertTo-SecureString -AsPlainText \"{new_password}\" -Force)"
        
        
        print(command)
        print('powershell -command '+"'"+command+"'")
        with open("ac.ps1", "w") as power:
            power.write(command)
        
        #os.startfile("ac.ps1")
        ps_file = os.path.join(base_path, "ac.ps1")
        #powershell.exe -ExecutionPolicy RemoteSigned -file
        process=subprocess.Popen(["powershell.exe", "-ExecutionPolicy", "RemoteSigned", "-file", ps_file], stderr=subprocess.PIPE,stdout=subprocess.PIPE, shell=False)
        output, error = process.communicate()
        #print("output: ", output.decode("latin-1"))
        error = error.decode("latin-1")
        os.remove("ac.ps1")

        if error:
            raise Exception(error)
        
        # conn.extend.microsoft.modify_password(dn, None, new_password)
        
        # new_password = hashed('SHA', password)
        # modify = ModifyPassword(conn, user, new_password=new_password)
        # resp = modify.send()
        # conn.modify(user, {'unicodePwd': [(MODIFY_REPLACE, [password.encode('utf-16-le')])]})

    except Exception as e:
        traceback.print_exc()
        PrintException()
        raise e

if module == "next_login_change_password":

    user = GetParams("username")

    try:
        conn = mod_ms_activedirectory.get("connection")
        base = mod_ms_activedirectory.get("base")
        
        if '@' in user:
            query = f'(UserPrincipalName={user})'
            conn.search(base, query, attributes=['distinguishedName'])
            dn = conn.entries[0].distinguishedName
        else:
            dn = user
        
        mod_attrs = {"pwdLastSet": [(MODIFY_REPLACE, [0])]}
        conn.modify(dn, mod_attrs)
    
    except Exception as e:
        traceback.print_exc()
        PrintException()
        raise e

if module == "create_user":

    user_dn = GetParams("user_dn")
    object_class = GetParams("classes")
    attributes = GetParams("attributes") 
    
    try:
        conn = mod_ms_activedirectory.get("connection")
        base = mod_ms_activedirectory.get("base")
        
        if object_class.startswith("["):
            object_class = eval(object_class)
        else:
            raise Exception("object_class must be a list")
        if attributes.startswith("{"):
            attributes = eval(attributes)
        else:
            raise Exception("attributes must be a dictionary")
        
        conn.add(user_dn, object_class, attributes)

    except Exception as e:
        traceback.print_exc()
        PrintException()
        raise e

if module == "delete_user":

    user = GetParams("username")

    try:
        conn = mod_ms_activedirectory.get("connection")
        base = mod_ms_activedirectory.get("base")
        
        if '@' in user:
            query = f'(UserPrincipalName={user})'
            conn.search(base, query, attributes=['distinguishedName'])
            dn = conn.entries[0].distinguishedName
        else:
            dn = user
        
        conn.delete(dn)
    
    except Exception as e:
        traceback.print_exc()
        PrintException()
        raise e    
    
    
#     # Define the attributes for the new user
#     dn = 'CN=John Doe,OU=Users,DC=your-domain,DC=com'
#     attributes = {
#         'objectClass': ['user'],
#         'cn': 'John Doe',
#         'givenName': 'John',
#         'sn': 'Doe',
#         'userPrincipalName': 'johndoe@your-domain.com',
#         'sAMAccountName': 'johndoe',
#         'unicodePwd': '"Password123!"'.encode('utf-16-le')
#     }

#     # Create the new user
#     try:
#         conn.add(dn, attributes)
#         print('User created successfully')
#     except LDAPEntryAlreadyExistsResult:
#         print('User already exists')

#     # Update the user's attributes
#     changes = {
#         'givenName': [(MODIFY_REPLACE, ['Jonathan'])],
#         'sn': [(MODIFY_REPLACE, ['Doe-Smith'])]
#     }
#     conn.modify(dn, changes)
#     print('User updated successfully')

#     # Delete the user
#     conn.delete(dn)
#     print('User deleted successfully')

#     # Unbind from the server
#     conn.unbind()
