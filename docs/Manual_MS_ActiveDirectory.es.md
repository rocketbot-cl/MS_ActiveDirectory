



# MS_ActiveDirectory
  
Conéctese con Microsoft Active Directory, administre todas los usuarios dentro del dominio, realice consultas y más.  

*Read this in other languages: [English](Manual_MS_ActiveDirectory.md), [Português](Manual_MS_ActiveDirectory.pr.md), [Español](Manual_MS_ActiveDirectory.es.md)*
  
![banner](imgs/Banner_MS_ActiveDirectory.jpg)
## Como instalar este módulo
  
Para instalar el módulo en Rocketbot Studio, se puede hacer de dos formas:
1. Manual: __Descargar__ el archivo .zip y descomprimirlo en la carpeta modules. El nombre de la carpeta debe ser el mismo al del módulo y dentro debe tener los siguientes archivos y carpetas: \__init__.py, package.json, docs, example y libs. Si tiene abierta la aplicación, refresca el navegador para poder utilizar el nuevo modulo.
2. Automática: Al ingresar a Rocketbot Studio sobre el margen derecho encontrara la sección de **Addons**, seleccionar **Install Mods**, buscar el modulo deseado y presionar install.  


## Descripción de los comandos

### Conectar
  
Conectar con Microsoft Active Directory
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Dominio del active directory||ldap://your-domain-controller|
|Grupo de usuarios o base de búsqueda||OU=Groups,OU=UserProvisioning|
|Usuario con permisos de lectura||DOMAIN\username|
|Contraseña||password|
|Indique nombre de la variable donde almacenar respuesta||Variable|

### Ejecutar consulta
  
Ejecutar consulta en Microsoft Active Directory
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Consulta||(&(objectClass=user)(objectCategory=person)(sAMAccountName={0}))|
|Atributos||cn, givenName, sn, userPrincipalName|
|Indique nombre de la variable donde almacenar respuesta||Variable|

### Habilitar/Deshabilitar Usuario
  
Habilita o deshabilita un usuario en Microsoft Active Directory
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Usuario (DN o nombre principal)||cn=user1,o=test ó username@domain.tld|
|Acción|||

### Desbloquear Usuario
  
Desbloquear un usuario suspendido o bloqueado en Microsoft Active Directory
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Usuario (DN o nombre principal)||cn=user1,o=test ó username@domain.tld|

### Cambiar Contraseña de Usuario
  
Cambia la contraseña de un usuario en Microsoft Active Directory
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Usuario con permisos de administración||DOMAIN\username|
|Contraseña||password|
|Server||server|
|Usuario (DN o nombre principal)||cn=user1,o=test ó username@domain.tld|
|Nueva Contraseña||12345678|

### Cambiar Contraseña en el proximo inicio de sesión
  
Hacer que un usuario cambie su contraseña en el próximo inicio de sesión en Microsoft Active Directory
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Usuario (DN o nombre principal)||cn=user1,o=test ó username@domain.tld|

### Crear Usuario
  
Crear un usuario en Microsoft Active Directory
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Usuario DN||cn=user1,o=test|
|Clases||['employee', 'person', 'organization', 'user']|
|Atributos||{'givenName': 'Test', 'sn': 'User', 'mail': 'test.user@domain.com', 'sAMAccountName': 'testuser'}|

### Borrar Usuario
  
Borrar un usuario en Microsoft Active Directory
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Usuario (DN o nombre principal)||cn=user1,o=test ó username@domain.tld|
