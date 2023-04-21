



# MS_ActiveDirectory
  
Connect with Microsoft Active Directory, manage every user account within the domain, make queries and more.  

*Read this in other languages: [English](Manual_MS_ActiveDirectory.md), [Português](Manual_MS_ActiveDirectory.pr.md), [Español](Manual_MS_ActiveDirectory.es.md)*
  
![banner](imgs/Banner_MS_ActiveDirectory.jpg)
## How to install this module
  
To install the module in Rocketbot Studio, it can be done in two ways:
1. Manual: __Download__ the .zip file and unzip it in the modules folder. The folder name must be the same as the module and inside it must have the following files and folders: \__init__.py, package.json, docs, example and libs. If you have the application open, refresh your browser to be able to use the new module.
2. Automatic: When entering Rocketbot Studio on the right margin you will find the **Addons** section, select **Install Mods**, search for the desired module and press install.  


## Description of the commands

### Connect
  
Connect to Microsoft Active Directory
|Parameters|Description|example|
| --- | --- | --- |
|Active Directory Domain||ldap://your-domain-controller|
|User group or search base||OU=Groups,OU=UserProvisioning|
|User with read permissions||DOMAIN\username|
|Password||password|
|Indicate the name of the variable where to store the response||Variable|

### Run query
  
Run query in Microsoft Active Directory
|Parameters|Description|example|
| --- | --- | --- |
|Query||(&(objectClass=user)(objectCategory=person)(sAMAccountName={0}))|
|Attributes||cn, givenName, sn, userPrincipalName|
|Indicate the name of the variable where to store the response||Variable|

### Enable/Disable User
  
Enables or disables a user in Microsoft Active Directory
|Parameters|Description|example|
| --- | --- | --- |
|Username (DN or principal name)||cn=user1,o=test or username@domain.tld|
|Action|||

### Unlock User
  
Unlock a suspended or locked user in Microsoft Active Directory
|Parameters|Description|example|
| --- | --- | --- |
|Username (DN or principal name)||cn=user1,o=test or username@domain.tld|

### Change User Password
  
Change the password of a user in Microsoft Active Directory
|Parameters|Description|example|
| --- | --- | --- |
|Username (DN or principal name)||cn=user1,o=test or username@domain.tld|
|New Password||12345678|
|Current Password (Optional)||87654321|

### Change Password at next login
  
Make a user change its password at the next login in Microsoft Active Directory
|Parameters|Description|example|
| --- | --- | --- |
|Username (DN or principal name)||cn=user1,o=test or username@domain.tld|

### Create User
  
Create a user from Microsoft Active Directory
|Parameters|Description|example|
| --- | --- | --- |
|User DN||cn=user1,o=test|
|Classes||['employee', 'person', 'organization', 'user']|
|Attributes||{'givenName': 'Test', 'sn': 'User', 'mail': 'test.user@domain.com', 'sAMAccountName': 'testuser'}|

### Delete User
  
Delete a user from Microsoft Active Directory
|Parameters|Description|example|
| --- | --- | --- |
|Username (DN or principal name)||cn=user1,o=test or username@domain.tld|
