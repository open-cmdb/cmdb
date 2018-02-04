import ldap
ldapServer = 'ldap://192.168.1.203:389'
domain = 'hbgd.com'
userName = 'Manage'
domainUserName = domain + '\\' + userName
password = 'tmm3239448'
try:
    conn = ldap.initialize(ldapServer)
    conn.simple_bind_s("cn=lisi,ou=sales,dc=hbgd,dc=com", password)
    # 认证通过
except:
    print("auth error")