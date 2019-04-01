import os
#print("Select game:")
runner = {
	"1":"python3 zork.py",
	"2":"python /usr/local/bin/pywumpus.py",
	"3":"python3 adventureontheweb.py"
}
while True:
	print("1. Zork\n2. Wumpus\n3. Adventure On The Web\n")
	input_text = input("Choose game:")
	os.system("ls && pwd")
	os.system(runner[input_text])
	break
