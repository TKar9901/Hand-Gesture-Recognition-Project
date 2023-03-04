from gcalAPI import gAPI

obj = gAPI(source=0)

print("updating events...")
obj.eventsUpdate()
print("filing data...")
obj.dataProcessing()
print("ready to output...")
obj.dataOutput()




































# # print("making output files...")
# obj.dataOutput()

