import os
#print("Select game:")
runner = {
	"1":"/usr/bin/python3 /opt/app/MLMOS2/zork.py",
	"2":"python /usr/local/bin/pywumpus.py"
}
while True:
	print("1. Zork\n2. Wumpus\n")
	input_text = input("Choose game:")
	os.system(runner[input_text])
	break
