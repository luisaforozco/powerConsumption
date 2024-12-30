"""
 Notes from Luisa Orozco:
 - We have two networks LuisaHerman and Luisa&Herman. The devices on the second floor are in LuisaHerman network. So this script should be run on a machine connected to the right network (LuisaHerman).
"""
import os
import time
from matplotlib import pyplot as plt
import demjson3 as demjson
import tuyapower


# Terminal Color Formatting
bold="\033[0m\033[97m\033[1m"
subbold="\033[0m\033[32m"
normal="\033[97m\033[0m"
dim="\033[0m\033[97m\033[2m"
alert="\033[0m\033[91m\033[1m"
alertdim="\033[0m\033[91m\033[2m"

PLOT_REAL_TIME = False

# Load Device Keys from Tuya JSON file
print("Loading Tuya Keys...")
f = open('../devices.json',"r")
data = demjson.decode(f.read())
f.close()
print("    %s%s device keys loaded%s"%(subbold, len(data), normal))

print("Polling devices...")
for i in data:
    name = i['name'] 
    if name != 'washing machine': continue # only consider device with name 'washing machine'
    if (i['ip'] == 0):
        print ('%s[%s]%s - %sError - No IP found%s'%(bold, name, dim, alert, normal))
    else:
        if PLOT_REAL_TIME:
            fig1 = plt.figure()
            plt.xlabel('Time (s)')
            plt.ylabel('Power (kWh)')
            plt.title('Power vs Time')
        os.makedirs('../measurements/', exist_ok=True)
        output_file = open('../measurements/' 
                           + time.strftime("%Y-%m-%d_%H-%M", time.localtime())
                           + '.txt', 'w')
        output_file.write("%s\t%s\t%s\t%s\t%s\n"%("#Time", "W", "mA", "V","kWh"))
        times, watts, power_consumption = [], [], []
        kwh = 0
        time_start = time.time()
        time_iteration = time_start
        total_measure_time = 60 * 5.5 # minutes
        while (time.time() - time_start < total_measure_time*60):
            (on, w, mA, V, err) = tuyapower.deviceInfo(i['id'], i['ip'], i['key'], i['version'])
            times.append(time.time() - time_start)
            kwh += (w/1000) * (time.time() - time_iteration)/3600
            time_iteration = time.time()
            power_consumption.append(kwh)
            watts.append(w)
            state = alertdim + "Off" + normal
            if isinstance(on, dict):
                state = dim + "%d Switches: " % len(on)
                for e in on:
                    if(on[e] == True):
                        state = state + normal + e + ":" + subbold + "On " + normal
                    else:
                        state = state + normal + e + ":" + alertdim + "Off " + normal
            elif(on):
                state = subbold + "On" + normal
            if(err == "OK"):
                print("%s[%s]%s - %s - Power: %sW, %smA, %sV %skWh"%(bold, name, normal, state, w, mA, V, kwh))
                output_file.write("%s\t%s\t%s\t%s\t%s\n"%(time.time() - time_start, w, mA, V, kwh))
            else:
                print("%s[%s]%s - %s"%(bold, name, normal, state))
            if PLOT_REAL_TIME:
                #plotting the read values
                plt.plot(times, power_consumption, 'k')
                #plt.show()
                plt.draw()
                plt.pause(0.001)
            time.sleep(5) # wait X seconds before polling again
        output_file.close()
print("END")