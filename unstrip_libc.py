import os,pwn,sys,random
from Libc import *
from fetch_deb import *
from check_requirement import *
required_tools=["7z","patchelf","eu-unstrip","wget"]
def unstrip(libc: LIBC):
	pwn.log.info("Unstripping libc")
	id_=random.randint(1,50)
	working_dir=f"/tmp/{id_}"
	file_deb=f"libc6-dbg_{libc.name}_{libc.arch}.deb"
	pwn.log.info(f"Download {pkd_url}{file_deb}")
	fetch_deb(libc,working_dir,file_deb)
	cmd=os.system(f"""
	eu-unstrip -o {libc.path} {libc.path} {working_dir}/usr/lib/debug/lib/x86_64-linux-gnu/libc-{libc.version}.so 
	rm -rf {working_dir}
	""")
	if cmd:
		raise Exception("Error when unstripping libc")
def main():
	global libc
	check_requirement()
	if len(sys.argv)!=2:
		print(f"Usage: {sys.argv[0]} <libc_file>")
		exit(1)
	libc=LIBC(sys.argv[1])
	unstrip(libc)
if __name__=='__main__':
	main()
