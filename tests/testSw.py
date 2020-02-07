def main():
    from tests.enablelog import ScriptLog, banner
    sl = ScriptLog("switch.log")
    log = sl.log
    from mdslib.switch import Switch

    user = 'admin'
    pw = 'nbv!2345'
    ip_address = '10.126.94.104'
    ip_address1 = '10.126.94.121'

    p = 8443

    sw104 = Switch(
        ip_address=ip_address,
        username=user,
        password=pw,
        connection_type='https',
        port=p,
        timeout=30,
        verify_ssl=False)

    sw121 = Switch(
        ip_address=ip_address1,
        username=user,
        password=pw,
        connection_type='https',
        port=p,
        timeout=30,
        verify_ssl=False)

    sw220 = Switch(
        ip_address="10.126.94.220",
        username=user,
        password=pw,
        connection_type='https',
        port=p,
        timeout=30,
        verify_ssl=False)

    sw = sw220
    banner("ip, version, model, npv")
    print("switch ip addr is   : " + sw.ipaddr)
    print("switch version is   : " + sw.version)
    print("switch model is     : " + sw.model)
    print("switch npv state is : " + str(sw.npv))
    banner("end")


if __name__ == "__main__":
    main()
