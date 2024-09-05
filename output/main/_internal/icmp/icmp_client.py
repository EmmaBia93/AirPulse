import icmplib

def is_device_online(ips):
   
#    return True if ping(ip,timeout=1) else False

    results = {}
    for ip in ips:
        try:
            response = icmplib.ping(ip, count=1, timeout=1)
            if response.is_alive:
                results[ip] = True
            else:
                results[ip] = False
        
        except Exception as e:
            results[ip] = False

    return results

