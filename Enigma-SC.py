'''
BSD 3-Clause License

Copyright (c) 2023, art2mri

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

import os
import subprocess
import tkfilebrowser
import csv
import math
import shutil
import getpass
import webbrowser
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import simpledialog
from datetime import datetime
from tkinter import ttk


#############################

def get_exit(command_a, command_b):
		exit2 = subprocess.run(command_a, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
		if exit2 != 0:
			subprocess.run(command_b, shell=True, check=True)
		else:
			subprocess.run(command_a, shell=True, check=True)
			
#############################
def browse_folder_niigz():
	root = tk.Tk()
	root.withdraw()	
	
	print('\033[94m\033[1mPLEASE SELECT THE\033[0m \033[92m\033[1mOUTPUT\033[0m \033[94m\033[1mFOLDER\033[0m')
	output = tkfilebrowser.askopendirnames()
	if not output:
		print('\033[91m\033[1mNo folder selected.\033[0m')
		return
	print ('\033[92m\033[1mSelected Folder:\033[0m')
	print(str(output[0]))	
	print('\033[94m\033[1mNOW SELECT THE WANTED\033[0m \033[92m\033[1m.nii.gz FILES\033[0m \033[94m\033[1mIN THE INPUT FOLDER:\033[0m')
	file_paths = filedialog.askopenfilenames(
		title="Select Files",
		filetypes=[("All Files","*.*")]
	)
	if not file_paths:
		print('\033[91m\033[1mNo dataset selected.\033[0m')
		return		
	print ('\033[92m\033[1mSelected Files:\033[0m')
	for i in file_paths:
		print(str(i))
		
	before = str(file_paths[0])	
	before = os.path.dirname(before)
	output = str(output[0])
	
	for i in file_paths:
		if '.nii.gz' not in i:
			os.system(os.path.basename(str(i))+'\033[91m\033[1m is not a .nii.gz file\033[0m')
		if '.nii.gz' in i:
			os.system('cd '+output+' && mkdir '+os.path.basename(str(i).replace(".nii.gz","")))
			os.system('cp '+before+'/'+os.path.basename(str(i))+' '+output+'/'+os.path.basename(str(i).replace(".nii.gz",""))+'/'+os.path.basename(str(i)))	
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')	
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				subfolder_path = os.path.join(directory, subfolder)
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('.nii.gz' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')						
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mEMPTY FOLDER\033[0m")
						output_file.write(f"{subfolder}.nii.gz EMPTY FOLDER" + '\n')						
					else:
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[91m\033[1mFAILED (MISSING SEGMENTATION FILE)\033[0m")
						output_file.write(f"{subfolder}.nii.gz FAILED (MISSING SEGMENTATION FILE)" + '\n')
                			
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mFOLDERS PREPARED!\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mFOLDERS PREPARED - CHECK THE WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mPREPARING FOLDERS FAILED\033[0m")
	else:	      			
		check_subfolders(str(output), str(output)+'/PrepareFoldersResults.txt')	   							
					
	
	
#############################

def browse_folder_BIDS():
	root = tk.Tk()
	root.withdraw()	
	
	print('\033[94m\033[1mPLEASE SELECT THE\033[0m \033[92m\033[1mOUTPUT\033[0m \033[94m\033[1mFOLDER\033[0m')
	output = tkfilebrowser.askopendirnames()
	if not output:
		print('\033[91m\033[1mNo folder selected.\033[0m')
		return
	print ('\033[92m\033[1mSelected Folder:\033[0m')
	print(str(output[0]))	
	print('\033[94m\033[1mNOW SELECT THE BIDS\033[0m \033[92m\033[1mDATASET\033[0m \033[94m\033[1mFOLDER:\033[0m')
	file_paths = tkfilebrowser.askopendirnames()
	if not file_paths:
		print('\033[91m\033[1mNo dataset selected.\033[0m')
		return		
	print ('\033[92m\033[1mSelected Dataset:\033[0m')
	print(str(file_paths[0]))	
	before = str(file_paths[0])
	output = str(output[0])

	def process_folder(before, output):
		for root, dirs, files in os.walk(before): 
			if 'anat' in dirs:
				anat_folder = os.path.join(root, 'anat')
				for file in os.listdir(anat_folder): 				          			       
					if file.endswith('T1w.nii.gz'):
						file_name = file.replace('.nii.gz', '')
						subfolder_path = os.path.join(output, file_name)
						os.makedirs(subfolder_path, exist_ok=True)
						file_path = os.path.join(anat_folder, file)
						os.system('cp '+file_path+' '+os.path.join(subfolder_path, file))
						
  				
	process_folder(before, output)                    						
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')	
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				subfolder_path = os.path.join(directory, subfolder)
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('.nii.gz' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')						
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mEMPTY FOLDER\033[0m")
						output_file.write(f"{subfolder}.nii.gz EMPTY FOLDER" + '\n')						
					else:
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[91m\033[1mFAILED (MISSING SEGMENTATION FILE)\033[0m")
						output_file.write(f"{subfolder}.nii.gz FAILED (MISSING SEGMENTATION FILE)" + '\n')
                			
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mFOLDERS PREPARED!\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mFOLDERS PREPARED - CHECK THE WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mPREPARING FOLDERS FAILED\033[0m")
	else:	      			
		check_subfolders(str(output), str(output)+'/PrepareFoldersResults.txt')	   			
  
                          
#############################   

def modal_docker():
	
	print('\033[94m\033[1mPLEASE SELECT THE DESIRED\033[0m \033[92m\033[1mSUBFOLDERS\033[0m \033[94m\033[1mFROM THE PREPARED FOLDER:\033[0m')		 			 	       	
	file_paths = tkfilebrowser.askopendirnames()
	if not file_paths:
		print('\033[91m\033[1mNo folders selected.\033[0m')
		return
		
	print ('\033[92m\033[1mSelected subfolders:\033[0m')
	for file_path in file_paths:
		print(file_path)
		
	before = str(file_paths[0])
	before = os.path.dirname(before)
           	            	 			
	progress_window = tk.Toplevel()
	progress_window.title("Segmentation Progress")

	progress_label = tk.Label(progress_window, text="Segmenting...")
	progress_label.pack()

	progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate")
	progress_bar.pack()

	progress_text = tk.Label(progress_window, text="")
	progress_text.pack()
	
	progress_bar["value"] = 0
	progress_text["text"] = "0% done"
	progress_window.update()
	
	def update_progress_bar(current, total):
		progress_percent = int((current / total) * 99)
		progress_bar["value"] = progress_percent
		progress_text["text"] = f"{progress_percent}% done"
		progress_window.update()
		
	exit_code = os.system("docker --version")
	if exit_code != 0:
    		print('\033[91m\033[1mDOCKER NOT INSTALLED. Please install Docker before running this script.\033[0m')
    		raise SystemExit(1)
    			
	password = None
	
	comando1='docker stop vertebral_labeling'
	comando2='docker rm vertebral_labeling'

	exit_code1 = subprocess.run('docker ps', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
	if exit_code1 != 0:
		result = subprocess.check_output("docker ps", shell=True, text=True)
		if 'vertebral_labeling' in result:
			subprocess.run(comando1, shell=True, check=True)
			subprocess.run(comando2, shell=True, check=True)
	else:
		result = subprocess.check_output("docker ps", shell=True, text=True)
		result = str(result)
		if 'vertebral_labeling' in result:
			os.system('docker stop vertebral_labeling')
			os.system('docker rm vertebral_labeling')
		
	exit_code2 = subprocess.run('docker ps -a', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
	if exit_code2 != 0:
		result = subprocess.check_output("docker ps -a", shell=True, text=True)
		if 'vertebral_labeling' in result:
			subprocess.run(comando2, shell=True, check=True)
	else:
		result = subprocess.check_output("docker ps", shell=True, text=True)
		result = str(result)
		if 'vertebral_labeling' in result:
			os.system('docker rm vertebral_labeling')
						
	loww1='docker run -itd --ipc=host --name vertebral_labeling art2mri/vertebral_labeling:3.0'
	loww2='docker run -itd --ipc=host --name vertebral_labeling art2mri/vertebral_labeling:3.0'
	
	try:
		subprocess.run(loww1, shell=True, check=True, stderr=subprocess.DEVNULL)
	except subprocess.CalledProcessError as e:
			subprocess.run(loww2, shell=True, check=True)		

	for idx, i in enumerate(file_paths): 
		try:
			subprocess.run('docker start vertebral_labeling', shell=True, check=True, stderr=subprocess.DEVNULL)
		except subprocess.CalledProcessError as e:
			subprocess.run('docker start vertebral_labeling', shell=True, check=True)
			
		os.environ['OMP_NUM_THREADS'] = '1'
		os.environ['MKL_NUM_THREADS'] = '1'
		os.environ['OPENBLAS_NUM_THREADS'] = '1'		

		command1 = 'cd '+before+'/'+os.path.basename(str(i).replace(".nii.gz",""))+' && '+'docker cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz vertebral_labeling:/home/SCT/'+os.path.basename(str(i))+'.nii.gz'+' && '+'docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling python3 spine.py 2> /dev/null'
		command2 = 'cd '+before+'/'+os.path.basename(str(i).replace(".nii.gz",""))+' && '+'sudo docker cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz vertebral_labeling:/home/SCT/'+os.path.basename(str(i))+'.nii.gz'+' && '+'sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling python3 spine.py'
		os.system(command1)
											
		command3='docker exec -it vertebral_labeling chmod -R 777 /home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz'
		command4='sudo docker exec -it vertebral_labeling chmod -R 777 /home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz'
		os.system(command3)
						
		command5='docker exec -it vertebral_labeling chmod -R 777 /home/SCT/qc_'+os.path.basename(str(i).replace(".nii.gz","")).replace(".nii","")
		command6='sudo docker exec -it vertebral_labeling chmod -R 777 /home/SCT/qc_'+os.path.basename(str(i).replace(".nii.gz","")).replace(".nii","")
		exit3 = subprocess.run(command5, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
		os.system(command5)
		
		command7='docker cp vertebral_labeling:/home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz'+' '+str(i)+'/'+os.path.basename(str(i))+'_seg.nii.gz'
		command8='sudo docker cp vertebral_labeling:/home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz'+' '+str(i)+'/'+os.path.basename(str(i))+'_seg.nii.gz'
		os.system(command7)
		
		command9='docker cp vertebral_labeling:/home/SCT/qc_'+os.path.basename(str(i))+' '+str(i)+'/qc_'+os.path.basename(str(i))
		command10='sudo docker cp vertebral_labeling:/home/SCT/qc_'+os.path.basename(str(i))+' '+str(i)+'/qc_'+os.path.basename(str(i))
		exit5 = subprocess.run(command9, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
		os.system(command9)
		
		command11='docker exec -it vertebral_labeling rm -f /home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz'
		command12='sudo docker exec -it vertebral_labeling rm -f /home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz'
		os.system(command11)
		
		command13='docker exec -it vertebral_labeling rm -f /home/SCT/'+os.path.basename(str(i))+'.nii.gz'
		command14='sudo docker exec -it vertebral_labeling rm -f /home/SCT/'+os.path.basename(str(i))+'.nii.gz'
		os.system(command13)
		
		command15='docker exec -it vertebral_labeling rm -r /home/SCT/qc_'+os.path.basename(str(i))
		command16='sudo docker exec -it vertebral_labeling rm -r /home/SCT/qc_'+os.path.basename(str(i))
		os.system(command15)
		update_progress_bar(idx + 1, len(file_paths))
					
	command17='docker stop vertebral_labeling'
	command18='docker stop vertebral_labeling'
	exit9 = subprocess.run(command17, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
	if exit9 != 0:
		subprocess.run(command18, shell=True, check=True)
	else:
		os.system(command17)
	command19='docker rm vertebral_labeling'
	os.system(command19)
				
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')	
	progress_label.config(text="SEGMENTATION FINISHED!")
	progress_window.update()
	progress_window.after(4000, progress_window.destroy)
	
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				subfolder_path = os.path.join(directory, subfolder)
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('_seg.nii.gz' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')						
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mEMPTY FOLDER\033[0m")
						output_file.write(f"{subfolder} EMPTY FOLDER" + '\n')						
					else:
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[91m\033[1mFAILED (MISSING SEGMENTATION FILE)\033[0m")
						output_file.write(f"{subfolder}.nii.gz FAILED (MISSING SEGMENTATION FILE)" + '\n')
                			
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mSEGMENTATION FINISHED\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mSEGMENTATION FINISHED WITH WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mSEGMENTATION FAILED\033[0m")
	else:	      			
		check_subfolders(str(before), str(before)+'/SegmentationResults.txt')		
	
#############################

def modal_singularity():			 			 	       	
	print('\033[94m\033[1mPLEASE SELECT THE\033[0m \033[92m\033[1mEnigma-SC\033[0m \033[94m\033[1mFOLDER\033[0m')
	enigma_folder = tkfilebrowser.askopendirname()
	if not enigma_folder:
		print('\033[91m\033[1mNo folder selected.\033[0m')
		return
	print('The \033[92m\033[1mEnigma-SC\033[0m folder selected is located at: '+enigma_folder)
	
	print('\033[94m\033[1mNOW SELECT THE DESIRED\033[0m \033[92m\033[1mSUBFOLDERS\033[0m \033[94m\033[1mFROM THE PREPARED FOLDER:\033[0m')		 			 	       	
	file_paths = tkfilebrowser.askopendirnames()
	if not file_paths:
		print('\033[91m\033[1mNo folders selected.\033[0m')
		return
		
	print ('\033[92m\033[1mSelected subfolders:\033[0m')
	for file_path in file_paths:
		print(file_path)
		
	before = str(file_paths[0])
	before = os.path.dirname(before)
           	            	 		
	progress_window = tk.Toplevel()
	progress_window.title("Segmentation Progress")

	progress_label = tk.Label(progress_window, text="Segmenting...")
	progress_label.pack()

	progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate")
	progress_bar.pack()

	progress_text = tk.Label(progress_window, text="")
	progress_text.pack()
	
	progress_bar["value"] = 0
	progress_text["text"] = "0% done"
	progress_window.update()
	
	def update_progress_bar(current, total):
		progress_percent = int((current / total) * 99)
		progress_bar["value"] = progress_percent
		progress_text["text"] = f"{progress_percent}% done"
		progress_window.update()
		
	exit_code = os.system("singularity --version")
	exity_code = os.system("apptainer --version")
	if exit_code and exity_code != 0:
    		print('\033[91m\033[1mSINGULARITY AND APPTAINER NOT INSTALLED. Please install one of them before running this script.\033[0m')
    		raise SystemExit(1)		
		
	k = os.listdir(enigma_folder+'/vertebral_labeling.simg/home/SCT/')
	for i in k:
		if os.path.isdir(enigma_folder+'/vertebral_labeling.simg/home/SCT/'+str(i)):
			shutil.rmtree(enigma_folder+'/vertebral_labeling.simg/home/SCT/'+str(i))
		else:
			os.remove(enigma_folder+'/vertebral_labeling.simg/home/SCT/'+str(i))		
	path = enigma_folder+'/vertebral_labeling.simg/home'
	dir_list = os.listdir(path)		
	for i in dir_list:
		if 'SCT' not in i:
			if 'datav2' not in i:
				if 'scripts' not in i:
					command21='rm -rf '+path+'/'+str(i)
					command22='sudo rm -rf '+path+'/'+str(i)
					os.system(command21)		
    	 
	for idx, i in enumerate(file_paths): 
		if any(arq.endswith('.nii.gz') for arq in os.listdir('vertebral_labeling.simg/home/SCT/')):
			command23='rm vertebral_labeling.simg/home/SCT/*nii.gz'
			command24='sudo rm vertebral_labeling.simg/home/SCT/*nii.gz'
			os.system(command23)
		if any(arq.endswith('.cache') for arq in os.listdir('vertebral_labeling.simg/home/SCT/')):
			command25='rm vertebral_labeling.simg/home/SCT/*nii.gz'
			command26='sudo rm vertebral_labeling.simg/home/SCT/*nii.gz'
			os.system(command25)			
		
		
		os.environ['OMP_NUM_THREADS'] = '1'
		os.environ['MKL_NUM_THREADS'] = '1'
		os.environ['OPENBLAS_NUM_THREADS'] = '1'
				
		os.system ('cd '+before+'/'+os.path.basename(str(i).replace(".nii.gz","")))
		command27='cd '+before+'/'+os.path.basename(str(i).replace(".nii.gz",""))+' && '+'cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'.nii.gz'
		command28='cd '+before+'/'+os.path.basename(str(i).replace(".nii.gz",""))+' && '+'sudo cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'.nii.gz'
		os.system(command27)
		command29='chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'.nii.gz'
		command30='sudo chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'.nii.gz'
		os.system(command29)				
		try:
			command31='singularity exec --writable --bind '+before+':/home/SCT '+enigma_folder+'/vertebral_labeling.simg/ python3 /spine.py'
			command32 = 'singularity exec --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ python3 /spine.py 2> /dev/null'						
			subprocess.run(command32, shell=True, check=True)
		except subprocess.CalledProcessError:
			command33='apptainer exec --writable vertebral_labeling.simg/ python3 /spine.py'
			command34='apptainer exec --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ python3 /spine.py 2> /dev/null'
			subprocess.run(command34, shell=True, check=True)
		command35='chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz'
		command36='sudo chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz'
		os.system(command35)				
		try:
			command37='singularity exec --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ chmod -R 777 /home/SCT/qc_'+os.path.basename(str(i).replace(".nii.gz","")).replace(".nii","")
			command38='sudo singularity exec --writable vertebral_labeling.simg/ chmod -R 777 /home/SCT/qc_'+os.path.basename(str(i).replace(".nii.gz","")).replace(".nii","")
			subprocess.run(command37, shell=True, check=True)
		except subprocess.CalledProcessError:
			command39='apptainer exec --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ chmod -R 777 /home/SCT/qc_'+os.path.basename(str(i).replace(".nii.gz","")).replace(".nii","")
			command40='sudo apptainer exec --writable vertebral_labeling.simg/ chmod -R 777 /home/SCT/qc_'+os.path.basename(str(i).replace(".nii.gz","")).replace(".nii","")
			subprocess.run(command39, shell=True, check=True)	
		command41='mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz '+str(i)
		subprocess.run(command41, shell=True, check=True)
		command47='mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/qc_'+os.path.basename(str(i))+' '+str(i)+'/qc_'+os.path.basename(str(i))
		subprocess.run(command47, shell=True, check=True)
		try:
			command49='singularity exec --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ rm -f /home/SCT/'+os.path.basename(str(i))+'.nii.gz'
			command50='sudo singularity exec --writable --nv vertebral_labeling.simg/ rm -f /home/SCT/'+os.path.basename(str(i))+'.nii.gz'
			subprocess.run(command49, shell=True, check=True)
		except subprocess.CalledProcessError:
			command51='apptainer exec --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ rm -f /home/SCT/'+os.path.basename(str(i))+'.nii.gz'
			command52='sudo apptainer exec --writable --nv vertebral_labeling.simg/ rm -f /home/SCT/'+os.path.basename(str(i))+'.nii.gz'	
			subprocess.run(command51, shell=True, check=True)
		update_progress_bar(idx + 1, len(file_paths))		
	progress_label.config(text="SEGMENTATION FINISHED!")
	progress_window.update()
	progress_window.after(4000, progress_window.destroy)
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')	
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				subfolder_path = os.path.join(directory, subfolder)
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('_seg.nii.gz' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')						
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mEMPTY FOLDER\033[0m")
						output_file.write(f"{subfolder} EMPTY FOLDER" + '\n')						
					else:
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[91m\033[1mFAILED (MISSING SEGMENTATION FILE)\033[0m")
						output_file.write(f"{subfolder}.nii.gz FAILED (MISSING SEGMENTATION FILE)" + '\n')
                			
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mSEGMENTATION FINISHED\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mSEGMENTATION FINISHED WITH WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mSEGMENTATION FAILED\033[0m")
	else:	      			
		check_subfolders(str(before), str(before)+'/SegmentationResults.txt')	   

#############################  

def docker():

	print('\033[94m\033[1mPLEASE SELECT THE DESIRED\033[0m \033[92m\033[1mSUBFOLDERS\033[0m \033[94m\033[1mFROM THE PREPARED FOLDER:\033[0m')
	file_paths = tkfilebrowser.askopendirnames()
	if not file_paths:
		print('\033[91m\033[1mNo folders selected.\033[0m')
		return
		
	print ('\033[92m\033[1mSelected folders:\033[0m')
	for file_path in file_paths:
		print(file_path)
		
	before = str(file_paths[0])
	before = os.path.dirname(before)	
		
	progress_window = tk.Toplevel()
	progress_window.title("Automated Labeling Progress")

	progress_label = tk.Label(progress_window, text="Labeling...")
	progress_label.pack()

	progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate")
	progress_bar.pack()

	progress_text = tk.Label(progress_window, text="")
	progress_text.pack()
	
	progress_bar["value"] = 0
	progress_text["text"] = "0% done"
	progress_window.update()
	
	def update_progress_bar(current, total):
		progress_percent = int((current / total) * 99)
		progress_bar["value"] = progress_percent
		progress_text["text"] = f"{progress_percent}% done"
		progress_window.update()
		
	exit_code = os.system("docker --version")
	if exit_code != 0:
    		print('\033[91m\033[1mDOCKER NOT INSTALLED. Please install Docker before running this script.\033[0m')
    		raise SystemExit(1)
    		
	password = None		
		
	comando1='docker stop vertebral_labeling'
	comando2='docker rm vertebral_labeling'

	exit_code1 = subprocess.run('docker ps', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
	if exit_code1 != 0:	
		result = subprocess.check_output("docker ps", shell=True, text=True)
		if 'vertebral_labeling' in result:
			subprocess.run(comando1, shell=True, check=True)
			subprocess.run(comando2, shell=True, check=True)
	else:
		result = subprocess.check_output("docker ps", shell=True, text=True)
		result = str(result)
		if 'vertebral_labeling' in result:
			os.system('docker stop vertebral_labeling')
			os.system('docker rm vertebral_labeling')
		
	exit_code2 = subprocess.run('docker ps -a', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
	if exit_code2 != 0:
		result = subprocess.check_output("docker ps -a", shell=True, text=True)
		if 'vertebral_labeling' in result:
			subprocess.run(comando2, shell=True, check=True)
	else:
		result = subprocess.check_output("docker ps", shell=True, text=True)
		result = str(result)
		if 'vertebral_labeling' in result:
			os.system('docker rm vertebral_labeling')																	
	try:
    		subprocess.run('nvidia-smi', check=True)
    		docker_command = 'docker run -itd --gpus all --ipc=host --name vertebral_labeling art2mri/vertebral_labeling:3.0'
	except FileNotFoundError as gpu_error:
    		docker_command = 'docker run -itd --ipc=host --name vertebral_labeling art2mri/vertebral_labeling:3.0'
	except subprocess.CalledProcessError as gpu_error:
    		docker_command = 'docker run -itd --ipc=host --name vertebral_labeling art2mri/vertebral_labeling:3.0'	
	try:
    		subprocess.run(docker_command, check=True)
	except FileNotFoundError as e:
		os.system(docker_command)


	for idx,i in enumerate(file_paths):
		
		command53='docker cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz vertebral_labeling:/home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/'+os.path.basename(str(i))+'_0000.nii.gz'
		command54='sudo -S docker cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz vertebral_labeling:/home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/'+os.path.basename(str(i))+'_0000.nii.gz'
		os.system(command53)
		command55='docker start vertebral_labeling'
		command56='docker start vertebral_labeling'
		try:
			subprocess.run(command55, shell=True, check=True, stderr=subprocess.DEVNULL)
		except subprocess.CalledProcessError as e:
			subprocess.run(command56, shell=True, check=True)					
		comando_11 = 'docker exec -it vertebral_labeling python3 /home/scripts/cuda.py'
		comando_12 = 'docker exec -it vertebral_labeling python3 /home/scripts/cuda.py'
		comando_2 = 'docker exec -it vertebral_labeling python3 /home/scripts/cpu.py'
		command_1 = 'docker exec -it vertebral_labeling python3 /home/scripts/cuda.py'
		file_to_check = '/home/datav2/inference/761_SCT/preds/'+os.path.basename(str(i))+'.nii.gz'
		command_21 = 'docker exec -it vertebral_labeling python3 /home/scripts/cpu.py'
		command_22 = 'docker exec -it vertebral_labeling python3 /home/scripts/cpu.py'
		exit16 = subprocess.run(comando_11, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
		if exit16 != 0:
			os.system('docker exec -it vertebral_labeling python3 /home/scripts/cuda.py')
		else:
			os.system('docker exec -it vertebral_labeling python3 /home/scripts/cuda.py')	
				
		check_file_command1 = f'docker exec -it vertebral_labeling test -f {file_to_check} && echo "found" || echo "not found"'	      				
		check_file_command2 = f'docker exec -it vertebral_labeling test -f {file_to_check} && echo "found" || echo "not found"'
		exit15 = subprocess.run(check_file_command1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
		if exit15 != 0:
			check_file_command = check_file_command2
		else:
			check_file_command = check_file_command1
			
		check_result = subprocess.run(check_file_command, shell=True, stdout=subprocess.PIPE, text=True)
		if "not found" in check_result.stdout:
			print("\033[93mTried to predict on GPU, but your GPU is not able to work on this task. Please check your CUDA settings\033[0m")
			print('\033[95m\033[1mNow trying to perform on CPU, this may take much more time to finish\033[0m')
			exit16 = subprocess.run(command_21, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
			if exit16 != 0:
				os.system('docker exec -it vertebral_labeling python3 /home/scripts/cpu.py')
			else:
				os.system('docker exec -it vertebral_labeling python3 /home/scripts/cpu.py')
		command555='docker exec -it vertebral_labeling chmod -R 777 /home/datav2/inference/761_SCT/preds/'+os.path.basename(str(i))+'.nii.gz'
		command666='docker exec -it vertebral_labeling chmod -R 777 /home/datav2/inference/761_SCT/preds/'+os.path.basename(str(i))+'.nii.gz'
		os.system(command555)
		command515='docker cp vertebral_labeling:/home/datav2/inference/761_SCT/preds/'+os.path.basename(str(i))+'.nii.gz'+' '+str(i)+'/'+os.path.basename(str(i))+'_seg_labeled.nii.gz'
		command616='sudo docker cp vertebral_labeling:/home/datav2/inference/761_SCT/preds/'+os.path.basename(str(i))+'.nii.gz'+' '+str(i)+'/'+os.path.basename(str(i))+'_seg_labeled.nii.gz'
		os.system(command515)
		command575='docker exec -it vertebral_labeling rm -f /home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/'+os.path.basename(str(i))+'_0000.nii.gz'
		command676='sudo docker exec -it vertebral_labeling rm -f /home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/'+os.path.basename(str(i))+'_0000.nii.gz'
		os.system(command575)
		
					
		os.system('docker cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz vertebral_labeling:/'+os.path.basename(str(i))+'.nii.gz')
		os.system('docker cp '+str(i)+'/'+os.path.basename(str(i))+'_seg_labeled.nii.gz vertebral_labeling:/'+os.path.basename(str(i))+'_seg_labeled.nii.gz')
		os.system('docker exec -it vertebral_labeling chmod -R 777 /'+os.path.basename(str(i))+'.nii.gz')
		os.system('docker exec -it vertebral_labeling chmod -R 777 /'+os.path.basename(str(i))+'_seg_labeled.nii.gz')
		os.system('docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling sct_qc -i /'+os.path.basename(str(i))+'.nii.gz -s /'+os.path.basename(str(i))+'_seg_labeled.nii.gz'+' -p sct_label_vertebrae')
		os.system('docker exec -it vertebral_labeling chmod -R 777 qc')
		os.system('docker cp vertebral_labeling:/qc'+' '+str(i)+'/'+'qc_labeled_'+os.path.basename(str(i)))
		os.system('docker exec -it vertebral_labeling rm -rf qc')
		os.system('docker exec -it vertebral_labeling rm -f /*.nii.gz')
		update_progress_bar(idx + 1, len(file_paths))		
		
		
					
		#os.system('cd '+str(i)+' && sct_qc -i '+os.path.basename(str(i))+'.nii.gz -s '+os.path.basename(str(i))+'_seg_labeled.nii.gz'+' -p sct_label_vertebrae')
		#os.system('mv -v '+str(i)+'/qc '+str(i)+'/qc_labeled_'+os.path.basename(str(i)))
		
		
			
	command63='docker stop vertebral_labeling'
	command64='docker stop vertebral_labeling'
	exit19 = subprocess.run(command63, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
	if exit19 != 0:
		subprocess.run(command64, shell=True, check=True)
	else:
		os.system(command63)
	command65='docker rm vertebral_labeling'
	command66='docker rm vertebral_labeling'
	os.system(command65)
	progress_label.config(text="AUTOMATED LABELING FINISHED!")
	progress_window.update()
	progress_window.after(4000, progress_window.destroy)
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				subfolder_path = os.path.join(directory, subfolder)
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('_seg_labeled.nii.gz' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')						
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mEMPTY FOLDER\033[0m")
						output_file.write(f"{subfolder} EMPTY FOLDER" + '\n')						
					else:
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[91m\033[1mFAILED (MISSING LABELED FILE)\033[0m")
						output_file.write(f"{subfolder}.nii.gz FAILED (MISSING LABELED FILE)" + '\n')
                			
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mAUTOMATED LABELING FINISHED\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mAUTOMATED LABELING FINISHED WITH WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mSEGMENTATION FAILED\033[0m")
	else:	      			
		check_subfolders(str(before), str(before)+'/AutomatedLabelingResults.txt')
	#pass
	
#############################		

def singularity():
	print('\033[94m\033[1mPLEASE SELECT THE\033[0m \033[92m\033[1mEnigma-SC\033[0m \033[94m\033[1mFOLDER\033[0m')
	enigma_folder = tkfilebrowser.askopendirname()
	print('The \033[92m\033[1mEnigma-SC\033[0m folder selected is located at: '+enigma_folder)
	
	print('\033[94m\033[1mPLEASE SELECT THE DESIRED\033[0m \033[92m\033[1mSUBFOLDERS\033[0m \033[94m\033[1mFROM THE PREPARED FOLDER:\033[0m')
	file_paths = tkfilebrowser.askopendirnames()
	if not file_paths:
		print('\033[91m\033[1mNo folders selected.\033[0m')
		return
		
	print ('\033[92m\033[1mSelected folders:\033[0m')
	for file_path in file_paths:
		print(file_path)
		
	before = str(file_paths[0])
	before = os.path.dirname(before)
		
	progress_window = tk.Toplevel()
	progress_window.title("Automated Labeling Progress")

	progress_label = tk.Label(progress_window, text="Labeling...")
	progress_label.pack()

	progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate")
	progress_bar.pack()

	progress_text = tk.Label(progress_window, text="")
	progress_text.pack()
	
	################################
	progress_bar["value"] = 0
	progress_text["text"] = "0% done"
	progress_window.update()
    	################################
	
	def update_progress_bar(current, total):
		progress_percent = int((current / total) * 99)
		progress_bar["value"] = progress_percent
		progress_text["text"] = f"{progress_percent}% done"
		progress_window.update()

	exit_code = os.system("singularity --version")
	exity_code = os.system("apptainer --version")
	if exit_code and exity_code != 0:
    		print('\033[91m\033[1mSINGULARITY AND APPTAINER NOT INSTALLED. Please install one of them before running this script.\033[0m')
    		raise SystemExit(1)		
	password = None
	
	k = os.listdir(enigma_folder+'/vertebral_labeling.simg/home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/')
	for i in k:
		if os.path.isdir(enigma_folder+'/vertebral_labeling.simg/home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/'+str(i)):
			shutil.rmtree(enigma_folder+'/vertebral_labeling.simg/home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/'+str(i))
		else:
			os.remove(enigma_folder+'/vertebral_labeling.simg/home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/'+str(i))	
	path = enigma_folder+'/vertebral_labeling.simg/home'
	dir_list = os.listdir(path)		
	for i in dir_list:
		if 'SCT' not in i:
			if 'datav2' not in i:
				if 'scripts' not in i:
					command21='rm -rf '+path+'/'+str(i)
					command22='sudo -S rm -rf '+path+'/'+str(i)
					exit2 = subprocess.run(command21, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
					os.system(command21)
					
	for idx,i in enumerate(file_paths):
		if any(arq.endswith('.nii.gz') for arq in os.listdir('vertebral_labeling.simg/home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/')):
			command219='rm vertebral_labeling.simg/home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/*nii.gz'
			command222='sudo -S rm vertebral_labeling.simg/home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/*nii.gz'
			exit238 = subprocess.run(command219, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
			os.system(command219)	
		#update_progress_bar(idx + 1, len(file_paths))
		command67='cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz '+enigma_folder
		command68='sudo cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz '+enigma_folder
		os.system(command67)
		command69='chmod -R 777 '+enigma_folder+'/'+os.path.basename(str(i))+'.nii.gz'
		command70='sudo chmod -R 777 '+enigma_folder+'/'+os.path.basename(str(i))+'.nii.gz'
		os.system(command69)
		os.system('mv '+os.path.basename(str(i))+'.nii.gz '+'vertebral_labeling.simg/home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/'+os.path.basename(str(i))+'_0000.nii.gz')	
		command73='chmod -R 777 vertebral_labeling.simg/home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/'+os.path.basename(str(i))+'_0000.nii.gz'
		command74='sudo chmod -R 777 vertebral_labeling.simg/home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/'+os.path.basename(str(i))+'_0000.nii.gz'
		os.system(command73)
		try:
			subprocess.run(["singularity --version"], check=True, shell=True)
			command_1 = 'singularity exec --writable --nv --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ python3 /home/scripts/cuda.py 2>/dev/null'
			command_12 = 'apptainer exec --writable --nv --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ python3 /home/scripts/cuda.py 2>/dev/null'
			command_2 = 'singularity exec --writable --nv --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ python3 /home/scripts/cpu.py 2>/dev/null'
			command_22= 'apptainer exec --writable --nv --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ python3 /home/scripts/cpu.py 2>/dev/null'
			try:
        			subprocess.run(command_1, shell=True)	
			except subprocess.CalledProcessError:
				try:
					subprocess.run(command_12, shell=True)  
				except subprocess.CalledProcessError:
					pass
			dire = 'vertebral_labeling.simg/home/datav2/inference/761_SCT/preds/'
			file1 = os.path.basename(str(i))+'.nii.gz'
			way = os.path.join(dire, file1)	     				
			if os.path.exists(way):
				print('OK')
			else:	
				print("\033[93mTried to predict on GPU, but your GPU is not able to work on this task. Please check your CUDA settings\033[0m")
				print('\033[95m\033[1mNow trying to perform on CPU, this may take much more time to finish\033[0m')
				try:
					subprocess.run(command_2, shell=True)
				except subprocess.CalledProcessError:		
					subprocess.run(command_22, shell=True)
					
		except subprocess.CalledProcessError:
			print('AUTOMATED LABELING FAILED')			

		command75='chmod -R 777 vertebral_labeling.simg/home/datav2/inference/761_SCT/preds/'+os.path.basename(str(i))+'.nii.gz'
		command76='sudo chmod -R 777 vertebral_labeling.simg/home/datav2/inference/761_SCT/preds/'+os.path.basename(str(i))+'.nii.gz'			
		os.system(command75)
		os.system('mv -v '+enigma_folder+'/vertebral_labeling.simg/home/datav2/inference/761_SCT/preds/'+os.path.basename(str(i))+'.nii.gz '+enigma_folder+'/vertebral_labeling.simg/home/datav2/inference/761_SCT/preds/'+os.path.basename(str(i))+'_seg_labeled.nii.gz')
		os.system('rm vertebral_labeling.simg/home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/*nii.gz')
				
		os.system('mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/datav2/inference/761_SCT/preds/'+os.path.basename(str(i))+'_seg_labeled.nii.gz '+enigma_folder)			
		os.system('mv '+enigma_folder+'/'+os.path.basename(str(i))+'_seg_labeled.nii.gz '+str(i))
		
		os.system('cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz '+enigma_folder+'/vertebral_labeling.simg/'+os.path.basename(str(i))+'.nii.gz')
		os.system('cp '+str(i)+'/'+os.path.basename(str(i))+'_seg_labeled.nii.gz '+enigma_folder+'/vertebral_labeling.simg/'+os.path.basename(str(i))+'_seg_labeled.nii.gz')
		os.system('chmod -R 777 vertebral_labeling.simg/'+os.path.basename(str(i))+'.nii.gz')
		os.system('chmod -R 777 vertebral_labeling.simg/'+os.path.basename(str(i))+'_seg_labeled.nii.gz')
		command_1 = 'singularity exec -e --env SCT_DIR=/spinalcordtoolbox --env PATH=/spinalcordtoolbox/bin:$PATH --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ sct_qc -i /'+os.path.basename(str(i))+'.nii.gz -s /'+os.path.basename(str(i))+'_seg_labeled.nii.gz'+' -p sct_label_vertebrae'
		command_2 = 'apptainer exec -e --env SCT_DIR=/spinalcordtoolbox --env PATH=/spinalcordtoolbox/bin:$PATH --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ sct_qc -i /'+os.path.basename(str(i))+'.nii.gz -s /'+os.path.basename(str(i))+'_seg_labeled.nii.gz'+' -p sct_label_vertebrae'
		try:
			subprocess.run(command_1, shell=True, check=True)
		except subprocess.CalledProcessError:
			subprocess.run(command_2, shell=True, check=True)
			
		os.system('mv -v '+enigma_folder+'/vertebral_labeling.simg/home/'+os.getenv('USER')+'/qc '+str(i)+'/qc_labeled_'+os.path.basename(str(i)))
		os.system('rm '+enigma_folder+'/vertebral_labeling.simg/*nii.gz')
		update_progress_bar(idx + 1, len(file_paths))
		
		
	progress_label.config(text="AUTOMATED LABELING FINISHED!")
	progress_window.update()
	progress_window.after(4000, progress_window.destroy)
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				subfolder_path = os.path.join(directory, subfolder)
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('_seg_labeled.nii.gz' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')						
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mEMPTY FOLDER\033[0m")
						output_file.write(f"{subfolder} EMPTY FOLDER" + '\n')						
					else:
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[91m\033[1mFAILED (MISSING LABELED FILE)\033[0m")
						output_file.write(f"{subfolder}.nii.gz FAILED (MISSING LABELED FILE)" + '\n')
                			
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mAUTOMATED LABELING FINISHED\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mAUTOMATED LABELING FINISHED WITH WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mSEGMENTATION FAILED\033[0m")
	else:	      			
		check_subfolders(str(before), str(before)+'/AutomatedLabelingResults.txt')
		
															
#############################  

def manual():	 
	
	print('\033[94m\033[1mPLEASE SELECT FROM THE PREPARED FOLDER ALL THE\033[0m \033[92m\033[1mSUBFOLDERS WHICH AUTOMATED LABELING\033[0m \033[94m\033[1mHAVE FAILED:\033[0m')
	file_paths = tkfilebrowser.askopendirnames()
	if not file_paths:
		print('\033[91m\033[1mNo folders selected.\033[0m')
		return
		
	print ('\033[92m\033[1mSelected folders:\033[0m')
	for file_path in file_paths:
		print(file_path)
		
	before = str(file_paths[0])
	before = os.path.dirname(before)	
		
	progress_window = tk.Toplevel()
	progress_window.title("Manual Labeling Progress")

	progress_label = tk.Label(progress_window, text="Labeling...")
	progress_label.pack()

	progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate")
	progress_bar.pack()

	progress_text = tk.Label(progress_window, text="")
	progress_text.pack()
	
	progress_bar["value"] = 0
	progress_text["text"] = "0% done"
	progress_window.update()
	
	def update_progress_bar(current, total):
		progress_percent = int((current / total) * 99)
		progress_bar["value"] = progress_percent
		progress_text["text"] = f"{progress_percent}% done"
		progress_window.update()	
		
	for idx, i in enumerate(file_paths):
		
		os.system('cd '+str(i)+' && sct_label_utils -i '+os.path.basename(str(i))+'.nii.gz'+' -create-viewer 2,3 -o '+os.path.basename(str(i))+'_labels_disc.nii.gz')
		update_progress_bar(idx + 1, len(file_paths))
	progress_label.config(text="Labeling Done!")
	progress_window.update()
	progress_window.after(4000, progress_window.destroy)
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				subfolder_path = os.path.join(directory, subfolder)
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('_labels_disc.nii.gz' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')						
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mEMPTY FOLDER\033[0m")
						output_file.write(f"{subfolder} EMPTY FOLDER" + '\n')						
					else:
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[93m\033[1mNOT SELECTED\033[0m")
						output_file.write(f"{subfolder}.nii.gz NOT SELECTED" + '\n')
	
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mMANUAL LABELING FINISHED\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mMANUAL LABELING FINISHED WITH WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mMANUAL LABELING FAILED\033[0m")
	else:	      			
		check_subfolders(str(before), str(before)+'/ManualLabelingResults.txt')	

#############################

def reg_aut_docker():
	
	print('\033[94m\033[1mPLEASE SELECT THE DESIRED\033[0m \033[92m\033[1mSUBFOLDERS\033[0m \033[94m\033[1mFROM THE PREPARED FOLDER:\033[0m')
	file_paths = tkfilebrowser.askopendirnames()
	if not file_paths:
		print('\033[91m\033[1mNo folders selected.\033[0m')
		return
		
	print ('\033[92m\033[1mSelected folders:\033[0m')
	for file_path in file_paths:
		print(file_path)
		
	before = str(file_paths[0])
	before = os.path.dirname(before)	
		
	progress_window = tk.Toplevel()
	progress_window.title("Automated Registration Progress")

	progress_label = tk.Label(progress_window, text="Registering...")
	progress_label.pack()

	progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate")
	progress_bar.pack()

	progress_text = tk.Label(progress_window, text="")
	progress_text.pack()
	
	progress_bar["value"] = 0
	progress_text["text"] = "0% done"
	progress_window.update()
	
	
	def update_progress_bar(current, total):
		progress_percent = int((current / total) * 99)
		progress_bar["value"] = progress_percent
		progress_text["text"] = f"{progress_percent}% done"
		progress_window.update()
		
	exit_code = os.system("docker --version")
	if exit_code != 0:
    		print('\033[91m\033[1mDOCKER NOT INSTALLED. Please install Docker before running this script.\033[0m')
    		raise SystemExit(1)
    		
	password = None	
    				
	comando1='docker stop vertebral_labeling'
	comando2='docker rm vertebral_labeling'

	exit_code1 = subprocess.run('docker ps', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
	if exit_code1 != 0:
		result = subprocess.check_output("docker ps", shell=True, text=True)
		if 'vertebral_labeling' in result:
			subprocess.run(comando1, shell=True, check=True)
			subprocess.run(comando2, shell=True, check=True)
	else:
		result = subprocess.check_output("docker ps", shell=True, text=True)
		result = str(result)
		if 'vertebral_labeling' in result:
			os.system('docker stop vertebral_labeling')
			os.system('docker rm vertebral_labeling')
		
	exit_code2 = subprocess.run('docker ps -a', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
	if exit_code2 != 0:
		result = subprocess.check_output("docker ps -a", shell=True, text=True)
		if 'vertebral_labeling' in result:
			subprocess.run(comando2, shell=True, check=True)
	else:
		result = subprocess.check_output("docker ps", shell=True, text=True)
		result = str(result)
		if 'vertebral_labeling' in result:
			os.system('docker rm vertebral_labeling')																	
	try:
    		subprocess.run('nvidia-smi', check=True)
    		docker_command = 'docker run -itd --gpus all --ipc=host --name vertebral_labeling art2mri/vertebral_labeling:3.0'
	except FileNotFoundError as gpu_error:
    		docker_command = 'docker run -itd --ipc=host --name vertebral_labeling art2mri/vertebral_labeling:3.0'
	except subprocess.CalledProcessError as gpu_error:
    		docker_command = 'docker run -itd --ipc=host --name vertebral_labeling art2mri/vertebral_labeling:3.0'	
	try:
    		subprocess.run(docker_command, check=True)
	except FileNotFoundError as e:
		os.system(docker_command)				
		
	for idx, i in enumerate(file_paths):
		#update_progress_bar(idx + 1, len(file_paths))
		
		try:
			subprocess.run('docker start vertebral_labeling', shell=True, check=True, stderr=subprocess.DEVNULL)
		except subprocess.CalledProcessError as e:
			subprocess.run('docker start vertebral_labeling', shell=True, check=True)
		command77='cd '+before+'/'+os.path.basename(str(i).replace(".nii.gz",""))+' && '+'docker cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz vertebral_labeling:/home/SCT/'
		command78='cd '+before+'/'+os.path.basename(str(i).replace(".nii.gz",""))+' && '+'sudo docker cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz vertebral_labeling:/home/SCT/'	
		os.system(command77)
		command79='cd '+before+'/'+os.path.basename(str(i).replace(".nii.gz",""))+' && '+'docker cp '+str(i)+'/'+os.path.basename(str(i))+'_seg.nii.gz vertebral_labeling:/home/SCT/'
		command80='cd '+before+'/'+os.path.basename(str(i).replace(".nii.gz",""))+' && '+'sudo docker cp '+str(i)+'/'+os.path.basename(str(i))+'_seg.nii.gz vertebral_labeling:/home/SCT/'
		os.system(command79)
		command81='cd '+before+'/'+os.path.basename(str(i).replace(".nii.gz",""))+' && '+'docker cp '+str(i)+'/'+os.path.basename(str(i))+'_seg_labeled.nii.gz vertebral_labeling:/home/SCT/'
		command82='cd '+before+'/'+os.path.basename(str(i).replace(".nii.gz",""))+' && '+'sudo docker cp '+str(i)+'/'+os.path.basename(str(i))+'_seg_labeled.nii.gz vertebral_labeling:/home/SCT/'
		os.system(command81)
		command83='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling python3 spine1.py'
		command84='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling python3 spine1.py'
		os.system(command83)
		command85='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/'+os.path.basename(str(i))+'_labels_vert.nii.gz'
		command86='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/'+os.path.basename(str(i))+'_labels_vert.nii.gz'
		os.system(command85)
		command87='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling python3 spine2.py'
		command88='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling python3 spine2.py'
		os.system(command87)
		command89='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/anat2template.nii.gz'
		command90='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/anat2template.nii.gz'
		os.system(command89)
		command91='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/straight_ref.nii.gz'
		command92='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/straight_ref.nii.gz'
		os.system(command91)
		command93='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/template2anat.nii.gz'
		command94='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/template2anat.nii.gz'
		os.system(command93)
		command95='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/warp_anat2template.nii.gz'
		command96='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/warp_anat2template.nii.gz'
		os.system(command95)
		command97='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/warp_curve2straight.nii.gz'
		command98='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/warp_curve2straight.nii.gz'
		os.system(command97)
		command99='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/warp_straight2curve.nii.gz'
		command100='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/warp_straight2curve.nii.gz'
		os.system(command99)
		command101='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/warp_template2anat.nii.gz'
		command102='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/warp_template2anat.nii.gz'
		os.system(command101)
		command103='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling python3 spine3.py'
		command104='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling python3 spine3.py'
		os.system(command103)
		command105='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/label'
		command106='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/label'
		os.system(command105)
		command107='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/straightening.cache'
		command108='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/straightening.cache'
		os.system(command107)
		command109='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/qc_template_'+os.path.basename(str(i))
		command110='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/qc_template_'+os.path.basename(str(i))
		os.system(command109)
		command111='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/qc_warp_'+os.path.basename(str(i))
		command112='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling chmod -R 777 /home/SCT/qc_warp_'+os.path.basename(str(i))
		os.system(command111)
		command113='docker cp vertebral_labeling:/home/SCT/anat2template.nii.gz '+before+'/'+os.path.basename(str(i))+'/anat2template.nii.gz'
		command114='sudo docker cp vertebral_labeling:/home/SCT/anat2template.nii.gz '+before+'/'+os.path.basename(str(i))+'/anat2template.nii.gz'		
		os.system(command113)
		command115='docker cp vertebral_labeling:/home/SCT/'+os.path.basename(str(i))+'_labels_vert.nii.gz'+' '+before+'/'+os.path.basename(str(i))+'/'+os.path.basename(str(i))+'_labels_vert.nii.gz'
		command116='sudo docker cp vertebral_labeling:/home/SCT/'+os.path.basename(str(i))+'_labels_vert.nii.gz'+' '+before+'/'+os.path.basename(str(i))+'/'+os.path.basename(str(i))+'_labels_vert.nii.gz'		
		os.system(command115)
		if 'label' in os.listdir(before+'/'+os.path.basename(str(i))):
			shutil.rmtree(before+'/'+os.path.basename(str(i))+'/label')
		command117='docker cp vertebral_labeling:/home/SCT/label '+before+'/'+os.path.basename(str(i))+'/label'
		command118='sudo docker cp vertebral_labeling:/home/SCT/label '+before+'/'+os.path.basename(str(i))+'/label'			
		os.system(command117)
		if 'qc_template_'+os.path.basename(str(i)) in os.listdir(before+'/'+os.path.basename(str(i))):
			shutil.rmtree(before+'/'+os.path.basename(str(i))+'/qc_template_'+os.path.basename(str(i)))
		command119='docker cp vertebral_labeling:/home/SCT/qc_template_'+os.path.basename(str(i))+' '+before+'/'+os.path.basename(str(i))+'/qc_template_'+os.path.basename(str(i))
		command120='sudo docker cp vertebral_labeling:/home/SCT/qc_template_'+os.path.basename(str(i))+' '+before+'/'+os.path.basename(str(i))+'/qc_template_'+os.path.basename(str(i))					
		os.system(command119)
		if 'qc_warp_'+os.path.basename(str(i)) in os.listdir(before+'/'+os.path.basename(str(i))):
			shutil.rmtree(before+'/'+os.path.basename(str(i))+'/qc_warp_'+os.path.basename(str(i)))
		command121='docker cp vertebral_labeling:/home/SCT/qc_warp_'+os.path.basename(str(i))+' '+before+'/'+os.path.basename(str(i))+'/qc_warp_'+os.path.basename(str(i))
		command122='sudo docker cp vertebral_labeling:/home/SCT/qc_warp_'+os.path.basename(str(i))+' '+before+'/'+os.path.basename(str(i))+'/qc_warp_'+os.path.basename(str(i))	
		os.system(command121)
		command123='docker cp vertebral_labeling:/home/SCT/straight_ref.nii.gz '+before+'/'+os.path.basename(str(i))+'/straight_ref.nii.gz'
		command124='sudo docker cp vertebral_labeling:/home/SCT/straight_ref.nii.gz '+before+'/'+os.path.basename(str(i))+'/straight_ref.nii.gz'		
		os.system(command123)
		command125='docker cp vertebral_labeling:/home/SCT/straightening.cache '+before+'/'+os.path.basename(str(i))+'/straightening.cache'
		command126='sudo docker cp vertebral_labeling:/home/SCT/straightening.cache '+before+'/'+os.path.basename(str(i))+'/straightening.cache'		
		os.system(command125)
		command127='docker cp vertebral_labeling:/home/SCT/template2anat.nii.gz '+before+'/'+os.path.basename(str(i))+'/template2anat.nii.gz'
		command128='sudo docker cp vertebral_labeling:/home/SCT/template2anat.nii.gz '+before+'/'+os.path.basename(str(i))+'/template2anat.nii.gz'	
		os.system(command127)
		command129='docker cp vertebral_labeling:/home/SCT/warp_anat2template.nii.gz '+before+'/'+os.path.basename(str(i))+'/warp_anat2template.nii.gz'
		command130='sudo docker cp vertebral_labeling:/home/SCT/warp_anat2template.nii.gz '+before+'/'+os.path.basename(str(i))+'/warp_anat2template.nii.gz'
		os.system(command129)
		command131='docker cp vertebral_labeling:/home/SCT/warp_curve2straight.nii.gz '+before+'/'+os.path.basename(str(i))+'/warp_curve2straight.nii.gz'
		command132='sudo docker cp vertebral_labeling:/home/SCT/warp_curve2straight.nii.gz '+before+'/'+os.path.basename(str(i))+'/warp_curve2straight.nii.gz'
		os.system(command131)
		command133='docker cp vertebral_labeling:/home/SCT/warp_straight2curve.nii.gz '+before+'/'+os.path.basename(str(i))+'/warp_straight2curve.nii.gz'
		command134='sudo docker cp vertebral_labeling:/home/SCT/warp_straight2curve.nii.gz '+before+'/'+os.path.basename(str(i))+'/warp_straight2curve.nii.gz'
		os.system(command133)
		command135='docker cp vertebral_labeling:/home/SCT/warp_template2anat.nii.gz '+before+'/'+os.path.basename(str(i))+'/warp_template2anat.nii.gz'
		command136='sudo docker cp vertebral_labeling:/home/SCT/warp_template2anat.nii.gz '+before+'/'+os.path.basename(str(i))+'/warp_template2anat.nii.gz'
		os.system(command135)
		command137='docker exec -it vertebral_labeling rm -rf /home/SCT/qc_template_'+os.path.basename(str(i))
		command138='sudo docker exec -it vertebral_labeling rm -rf /home/SCT/qc_template_'+os.path.basename(str(i))
		os.system(command137)
		command141='docker exec -it vertebral_labeling rm -rf /home/SCT/qc_warp_'+os.path.basename(str(i))
		command142='sudo docker exec -it vertebral_labeling rm -rf /home/SCT/qc_warp_'+os.path.basename(str(i))
		os.system(command141)
		command143='docker exec -it vertebral_labeling rm -rf /home/SCT/label'
		command144='sudo docker exec -it vertebral_labeling rm -rf /home/SCT/label'
		os.system(command143)
		command145='docker exec -it vertebral_labeling rm -f /home/SCT/anat2template.nii.gz'
		command146='sudo docker exec -it vertebral_labeling rm -f /home/SCT/anat2template.nii.gz'
		os.system(command145)
		command147='docker exec -it vertebral_labeling rm -f /home/SCT/straight_ref.nii.gz'
		command148='sudo docker exec -it vertebral_labeling rm -f /home/SCT/straight_ref.nii.gz'
		os.system(command147)
		command149='docker exec -it vertebral_labeling rm -f /home/SCT/straightening.cache'
		command150='sudo docker exec -it vertebral_labeling rm -f /home/SCT/straightening.cache'
		os.system(command149)
		command151='docker exec -it vertebral_labeling rm -f /home/SCT/template2anat.nii.gz'
		command152='sudo docker exec -it vertebral_labeling rm -f /home/SCT/template2anat.nii.gz'
		os.system(command151)
		command153='docker exec -it vertebral_labeling rm -f /home/SCT/warp_anat2template.nii.gz'
		command154='sudo docker exec -it vertebral_labeling rm -f /home/SCT/warp_anat2template.nii.gz'
		os.system(command153)
		command155='docker exec -it vertebral_labeling rm -f /home/SCT/warp_curve2straight.nii.gz'
		command156='sudo docker exec -it vertebral_labeling rm -f /home/SCT/warp_curve2straight.nii.gz'
		os.system(command155)
		command157='docker exec -it vertebral_labeling rm -f /home/SCT/warp_straight2curve.nii.gz'
		command158='sudo docker exec -it vertebral_labeling rm -f /home/SCT/warp_straight2curve.nii.gz'
		os.system(command157)
		command159='docker exec -it vertebral_labeling rm -f /home/SCT/warp_template2anat.nii.gz'
		command160='sudo docker exec -it vertebral_labeling rm -f /home/SCT/warp_template2anat.nii.gz'
		os.system(command159)
		command161='docker exec -it vertebral_labeling rm -f /home/SCT/'+os.path.basename(str(i))+'.nii.gz'
		command162='sudo docker exec -it vertebral_labeling rm -f /home/SCT/'+os.path.basename(str(i))+'.nii.gz'
		os.system(command161)
		command163='docker exec -it vertebral_labeling rm -f /home/SCT/'+os.path.basename(str(i))+'_labels_vert.nii.gz'
		command164='sudo docker exec -it vertebral_labeling rm -f /home/SCT/'+os.path.basename(str(i))+'_labels_vert.nii.gz'
		os.system(command163)
		command165='docker exec -it vertebral_labeling rm -f /home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz'
		command166='sudo docker exec -it vertebral_labeling rm -f /home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz'
		os.system(command165)
		command167='docker exec -it vertebral_labeling rm -f /home/SCT/'+os.path.basename(str(i))+'_seg_labeled.nii.gz'
		command168='sudo docker exec -it vertebral_labeling rm -f /home/SCT/'+os.path.basename(str(i))+'_seg_labeled.nii.gz'
		os.system(command167)
		update_progress_bar(idx + 1, len(file_paths))		
	command169='docker stop vertebral_labeling'
	command170='docker stop vertebral_labeling'
	os.system(command169)
	command171='docker rm vertebral_labeling'
	command172='docker rm vertebral_labeling'
	os.system(command171)				
	progress_label.config(text="AUTOMATED REGISTRATION FINISHED!")
	progress_window.update()
	progress_window.after(4000, progress_window.destroy)
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				if os.path.isdir(os.path.join(directory, subfolder)):
					if os.path.exists(os.path.join(directory, subfolder)+'/label/template/'):
						pass
					else:
						all_responses_are_one = False	
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mMISSING FOLDERS\033[0m")
						output_file.write(f"{subfolder} MISSING FOLDERS" + '\n')		
				subfolder_path = os.path.join(directory, subfolder)+'/label/template/'
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('PAM50_levels.nii.gz' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mMISSING FOLDERS\033[0m")
						output_file.write(f"{subfolder} MISSING FOLDERS" + '\n')												
					else:
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[91m\033[1mFAILED (MISSING REGISTRATION FILE)\033[0m")
						output_file.write(f"{subfolder}.nii.gz FAILED (MISSING REGISTRATION FILE)" + '\n')
                			
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mAUTOMATED REGISTRATION FINISHED\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mAUTOMATED REGISTRATION FINISHED WITH WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mREGISTRATION FAILED FAILED\033[0m")
	else:	      			
		check_subfolders(str(before), str(before)+'/AutomatedRegistrationResults.txt')	

#############################

def reg_aut_singularity():

	print('\033[94m\033[1mPLEASE SELECT THE\033[0m \033[92m\033[1mEnigma-SC\033[0m \033[94m\033[1mFOLDER\033[0m')
	enigma_folder = tkfilebrowser.askopendirname()
	print('The \033[92m\033[1mEnigma-SC\033[0m folder selected is located at: '+enigma_folder)

	print('\033[94m\033[1mPLEASE SELECT THE DESIRED\033[0m \033[92m\033[1mSUBFOLDERS\033[0m \033[94m\033[1mFROM THE PREPARED FOLDER:\033[0m')
	file_paths = tkfilebrowser.askopendirnames()
	if not file_paths:
		print('\033[91m\033[1mNo folders selected.\033[0m')
		return
		
	print ('\033[92m\033[1mSelected folders:\033[0m')
	for file_path in file_paths:
		print(file_path)
		
	before = str(file_paths[0])
	before = os.path.dirname(before)	
		
	progress_window = tk.Toplevel()
	progress_window.title("Automated Registration Progress")

	progress_label = tk.Label(progress_window, text="Registering...")
	progress_label.pack()

	progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate")
	progress_bar.pack()

	progress_text = tk.Label(progress_window, text="")
	progress_text.pack()
	
	progress_bar["value"] = 0
	progress_text["text"] = "0% done"
	progress_window.update()
	
	def update_progress_bar(current, total):
		progress_percent = int((current / total) * 99)
		progress_bar["value"] = progress_percent
		progress_text["text"] = f"{progress_percent}% done"
		progress_window.update()
		
	exit_code = os.system("singularity --version")
	exity_code = os.system("apptainer --version")
	if exit_code and exity_code != 0:
    		print('\033[91m\033[1mSINGULARITY AND APPTAINER NOT INSTALLED. Please install one of them before running this script.\033[0m')
    		raise SystemExit(1)		
	
	k = os.listdir(enigma_folder+'/vertebral_labeling.simg/home/SCT/')
	for i in k:
		if os.path.isdir(enigma_folder+'/vertebral_labeling.simg/home/SCT/'+str(i)):
			shutil.rmtree(enigma_folder+'/vertebral_labeling.simg/home/SCT/'+str(i))
		else:
			os.remove(enigma_folder+'/vertebral_labeling.simg/home/SCT/'+str(i))		
	path = enigma_folder+'/vertebral_labeling.simg/home'
	dir_list = os.listdir(path)	
	for i in dir_list:
		if 'SCT' not in i:
			if 'datav2' not in i:
				if 'scripts' not in i:
					command21='rm -rf '+path+'/'+str(i)
					command22='sudo -S rm -rf '+path+'/'+str(i)
					os.system(command21)
				
	for idx, i in enumerate(file_paths):
		if any(arq.endswith('.nii.gz') for arq in os.listdir('vertebral_labeling.simg/home/SCT/')):	
			command219='rm vertebral_labeling.simg/home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/*nii.gz'
			command222='sudo -S rm vertebral_labeling.simg/home/datav2/nnUNet_raw/Dataset761_SCT/imagesTs/*nii.gz'
			os.system(command219)
		if any(arq.endswith('.cache') for arq in os.listdir('vertebral_labeling.simg/home/SCT/')):			
			command219='rm vertebral_labeling.simg/home/SCT/straightening.cache'
			command222='sudo -S rm vertebral_labeling.simg/home/SCT/straightening.cache'
			os.system(command219)
		
		command171='cd '+before+'/'+os.path.basename(str(i))+' && '+'cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'.nii.gz'
		command172='cd '+before+'/'+os.path.basename(str(i))+' && '+'sudo cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'.nii.gz'
		os.system(command171)
		command173='chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'.nii.gz'
		command174='sudo chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'.nii.gz'
		os.system(command173)				
		command175='cd '+before+'/'+os.path.basename(str(i))+' && '+'cp '+str(i)+'/'+os.path.basename(str(i))+'_seg.nii.gz '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz'
		command176='cd '+before+'/'+os.path.basename(str(i))+' && '+'sudo cp '+str(i)+'/'+os.path.basename(str(i))+'_seg.nii.gz '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz'
		os.system(command175)
		command177='chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz'
		command178='sudo chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz'
		os.system(command177)	
		command179='cd '+before+'/'+os.path.basename(str(i))+' && '+'cp '+str(i)+'/'+os.path.basename(str(i))+'_seg_labeled.nii.gz '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'_seg_labeled.nii.gz'
		command180='cd '+before+'/'+os.path.basename(str(i))+' && '+'sudo cp '+str(i)+'/'+os.path.basename(str(i))+'_seg_labeled.nii.gz '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'_seg_labeled.nii.gz'
		os.system(command179)
		command181='chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'_seg_labeled.nii.gz'
		command182='sudo chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'_seg_labeled.nii.gz'
		os.system(command181)			
		cmd_1='singularity exec --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ python3 /spine1.py'
		cmd_2='apptainer exec --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ python3 /spine1.py'
		try:	
			subprocess.run(cmd_1, shell=True, check=True)
		except subprocess.CalledProcessError:
			subprocess.run(cmd_2, shell=True, check=True)
		os.system('chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'_labels_vert.nii.gz')
			
		cmd_11='singularity exec --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ python3 /spine2.py'
		cmd_22='apptainer exec --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ python3 /spine2.py'
		try:		
			subprocess.run(cmd_11, shell=True, check=True)
		except subprocess.CalledProcessError:	
			subprocess.run(cmd_22, shell=True, check=True)

		os.system('chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/anat2template.nii.gz')
		os.system('chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/straight_ref.nii.gz')
		os.system('chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/template2anat.nii.gz')
		os.system('chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/warp_anat2template.nii.gz')
		os.system('chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/warp_curve2straight.nii.gz')
		os.system('chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/warp_straight2curve.nii.gz')
		os.system('chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/warp_template2anat.nii.gz')
		cmd_111='singularity exec --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ python3 /spine3.py'
		cmd_222='apptainer exec --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ python3 /spine3.py'
		try:		
			subprocess.run(cmd_111, shell=True, check=True)
		except subprocess.CalledProcessError:	
			subprocess.run(cmd_222, shell=True, check=True)
				
		os.system('chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/label')	
		os.system('chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/straightening.cache')		
		os.system('chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/qc_template_'+os.path.basename(str(i)))	
		os.system('chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/SCT/qc_warp_'+os.path.basename(str(i)))
		os.system('mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/anat2template.nii.gz '+before+'/'+os.path.basename(str(i))+'/anat2template.nii.gz')	
		os.system('mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'_labels_vert.nii.gz'+' '+before+'/'+os.path.basename(str(i))+'/'+os.path.basename(str(i))+'_labels_vert.nii.gz')	
		if 'label' in os.listdir(before+'/'+os.path.basename(str(i))):
			shutil.rmtree(before+'/'+os.path.basename(str(i))+'/label')
		os.system('mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/label'+' '+str(i)+'/label')	
		if 'qc_template_'+os.path.basename(str(i)) in os.listdir(before+'/'+os.path.basename(str(i))):
			shutil.rmtree(before+'/'+os.path.basename(str(i))+'/qc_template_'+os.path.basename(str(i)))
		os.system('mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/qc_template_'+os.path.basename(str(i))+' '+str(i)+'/qc_template_'+os.path.basename(str(i)))	
		if 'qc_warp_'+os.path.basename(str(i)) in os.listdir(before+'/'+os.path.basename(str(i))):
			shutil.rmtree(before+'/'+os.path.basename(str(i))+'/qc_warp_'+os.path.basename(str(i)))
		os.system('mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/qc_warp_'+os.path.basename(str(i))+' '+str(i)+'/qc_warp_'+os.path.basename(str(i)))
		os.system('mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/straight_ref.nii.gz '+before+'/'+os.path.basename(str(i))+'/straight_ref.nii.gz')
		os.system('mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/straightening.cache '+before+'/'+os.path.basename(str(i))+'/straightening.cache')
		os.system('mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/template2anat.nii.gz '+before+'/'+os.path.basename(str(i))+'/template2anat.nii.gz')
		os.system('mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/warp_anat2template.nii.gz '+before+'/'+os.path.basename(str(i))+'/warp_anat2template.nii.gz')
		os.system('mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/warp_curve2straight.nii.gz '+before+'/'+os.path.basename(str(i))+'/warp_curve2straight.nii.gz')
		os.system('mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/warp_straight2curve.nii.gz '+before+'/'+os.path.basename(str(i))+'/warp_straight2curve.nii.gz')
		os.system('mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/warp_template2anat.nii.gz '+before+'/'+os.path.basename(str(i))+'/warp_template2anat.nii.gz')
		os.system('rm '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'.nii.gz')
		os.system('rm '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'_seg.nii.gz')
		os.system('rm '+enigma_folder+'/'+'vertebral_labeling.simg/home/SCT/'+os.path.basename(str(i))+'_seg_labeled.nii.gz')
		update_progress_bar(idx + 1, len(file_paths))								
	progress_label.config(text="AUTOMATED REGISTRATION FINISHED!")
	progress_window.update()
	progress_window.after(4000, progress_window.destroy)
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				if os.path.isdir(os.path.join(directory, subfolder)):
					if os.path.exists(os.path.join(directory, subfolder)+'/label/template/'):
						pass
					else:
						all_responses_are_one = False	
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mMISSING FOLDERS\033[0m")
						output_file.write(f"{subfolder} MISSING FOLDERS" + '\n')		
				subfolder_path = os.path.join(directory, subfolder)+'/label/template/'
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('PAM50_levels.nii.gz' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mMISSING FOLDERS\033[0m")
						output_file.write(f"{subfolder} MISSING FOLDERS" + '\n')												
					else:
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[91m\033[1mFAILED (MISSING REGISTRATION FILE)\033[0m")
						output_file.write(f"{subfolder}.nii.gz FAILED (MISSING REGISTRATION FILE)" + '\n')
                			
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mAUTOMATED REGISTRATION FINISHED\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mAUTOMATED REGISTRATION FINISHED WITH WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mREGISTRATION FAILED FAILED\033[0m")
	else:	      			
		check_subfolders(str(before), str(before)+'/AutomatedRegistrationResults.txt')
		
#############################

def reg_man():
	
	print('\033[94m\033[1mPLEASE SELECT THE SUBFOLDERS THAT WERE\033[0m \033[92m\033[1mMANUAL LABELED\033[0m \033[94m\033[1mON THE PREVIOUS STEP:\033[0m')
	file_paths = tkfilebrowser.askopendirnames()
	if not file_paths:
		print('\033[91m\033[1mNo folders selected.\033[0m')
		return
		
	print ('\033[92m\033[1mSelected folders:\033[0m')
	for file_path in file_paths:
		print(file_path)
		
	before = str(file_paths[0])
	before = os.path.dirname(before)	
		
	progress_window = tk.Toplevel()
	progress_window.title("Manual Registration Progress")

	progress_label = tk.Label(progress_window, text="Registering...")
	progress_label.pack()

	progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate")
	progress_bar.pack()

	progress_text = tk.Label(progress_window, text="")
	progress_text.pack()
	
	progress_bar["value"] = 0
	progress_text["text"] = "0% done"
	progress_window.update()
	
	def update_progress_bar(current, total):
		progress_percent = int((current / total) * 99)
		progress_bar["value"] = progress_percent
		progress_text["text"] = f"{progress_percent}% done"
		progress_window.update()	
		
	for idx, i in enumerate(file_paths):
		
		if 'qc_template_manual_'+os.path.basename(str(i)) in os.listdir(before+'/'+os.path.basename(str(i))):
			shutil.rmtree(before+'/'+os.path.basename(str(i))+'/qc_template_manual_'+os.path.basename(str(i)))
		os.system('cd '+str(i)+' && sct_register_to_template -i '+os.path.basename(str(i))+'.nii.gz'+' -s '+os.path.basename(str(i))+'_seg.nii.gz -ldisc '+os.path.basename(str(i))+'_labels_disc.nii.gz -c t1 -qc qc_template_manual_'+os.path.basename(str(i)))
		update_progress_bar(idx + 1, len(file_paths))
		
	progress_label.config(text="MANUAL REGISTRATION FINISHED!")
	progress_window.update()
	progress_window.after(4000, progress_window.destroy)
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				subfolder_path = os.path.join(directory, subfolder)
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('qc_template_manual_' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')						
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mEMPTY FOLDER\033[0m")
						output_file.write(f"{subfolder} EMPTY FOLDER" + '\n')						
					else:
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[93m\033[1mNOT SELECTED\033[0m")
						output_file.write(f"{subfolder}.nii.gz NOT SELECTED" + '\n')
	
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mMANUAL REGISTRATION FINISHED\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mMANUAL REGISTRATION FINISHED WITH WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mMANUAL REGISTRATION FAILED\033[0m")
	else:	      			
		check_subfolders(str(before), str(before)+'/ManualRegistrationResults.txt')
	
		
#############################

def ext_docker():
	
	print('\033[94m\033[1mPLEASE SELECT THE DESIRED\033[0m \033[92m\033[1mSUBFOLDERS\033[0m \033[94m\033[1mFROM THE PREPARED FOLDER:\033[0m')
	file_paths = tkfilebrowser.askopendirnames()
	if not file_paths:
		print('\033[91m\033[1mNo folders selected.\033[0m')
		return
		
	print ('\033[92m\033[1mSelected folders:\033[0m')
	for file_path in file_paths:
		print(file_path)
		
	before = str(file_paths[0])
	before = os.path.dirname(before)
	
	data = ["subject", "CSA C1", "CSA C2", "CSA C3"]
	data2 = ["subject", "Mean(eccentricity) C1", "Mean(eccentricity) C2", "Mean(eccentricity) C3"]
	now = datetime.now()
	hour = str(now.strftime("%m-%d-%Y_%H-%M-%S"))
	before = str(file_paths[0])
	before = os.path.dirname(before)
	csvf = before +'/csa_final_table_'+hour+'.csv'
	eccf = before +'/eccentricity_table'+hour+'.csv'
	
	with open(csvf, mode='w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(data)
	print('CSA final table saved on '+str(csvf))
	
	with open(eccf, mode='w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(data2)
	print('eccentricity final table saved on '+str(eccf))	
	
	if not file_paths:
		print('\033[91m\033[1mNo folders selected.\033[0m')
		return
		
	print ('\033[92m\033[1mSelected folders:\033[0m')
	for file_path in file_paths:
		print(file_path)
		
	progress_window = tk.Toplevel()
	progress_window.title("Data Extraction Progress")

	progress_label = tk.Label(progress_window, text="Extracting...")
	progress_label.pack()

	progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate")
	progress_bar.pack()

	progress_text = tk.Label(progress_window, text="")
	progress_text.pack()
	
	progress_bar["value"] = 0
	progress_text["text"] = "0% done"
	progress_window.update()

	exit_code = os.system("docker --version")
	if exit_code != 0:
    		print('\033[91m\033[1mDOCKER NOT INSTALLED. Please install Docker before running this script.\033[0m')
    		raise SystemExit(1)	
    	
	password = None	
	
	def update_progress_bar(current, total):
		progress_percent = int((current / total) * 99)
		progress_bar["value"] = progress_percent
		progress_text["text"] = f"{progress_percent}% done"
		progress_window.update()
		
	comando1='docker stop vertebral_labeling'
	comando2='docker rm vertebral_labeling'

	exit_code1 = subprocess.run('docker ps', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
	if exit_code1 != 0:
		result = subprocess.check_output("docker ps", shell=True, text=True)
		if 'vertebral_labeling' in result:
			subprocess.run(comando1, shell=True, check=True)
			subprocess.run(comando2, shell=True, check=True)
	else:
		result = subprocess.check_output("docker ps", shell=True, text=True)
		result = str(result)
		if 'vertebral_labeling' in result:
			os.system('docker stop vertebral_labeling')
			os.system('docker rm vertebral_labeling')
		
	exit_code2 = subprocess.run('docker ps -a', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
	if exit_code2 != 0:
		result = subprocess.check_output("docker ps -a", shell=True, text=True)
		if 'vertebral_labeling' in result:
			subprocess.run(comando2, shell=True, check=True)
	else:
		result = subprocess.check_output("docker ps", shell=True, text=True)
		result = str(result)
		if 'vertebral_labeling' in result:
			os.system('docker rm vertebral_labeling')																	
	try:
    		subprocess.run('nvidia-smi', check=True)
    		docker_command = 'docker run -itd --gpus all --ipc=host --name vertebral_labeling art2mri/vertebral_labeling:3.0'
	except FileNotFoundError as gpu_error:
    		docker_command = 'docker run -itd --ipc=host --name vertebral_labeling art2mri/vertebral_labeling:3.0'
	except subprocess.CalledProcessError as gpu_error:
    		docker_command = 'docker run -itd --ipc=host --name vertebral_labeling art2mri/vertebral_labeling:3.0'	
	try:
    		subprocess.run(docker_command, check=True)
	except FileNotFoundError as e:
		os.system(docker_command)
			
	
	for idx,i in enumerate(file_paths):
		v = []
		k = []
		b1 = []
		
		try:
			subprocess.run('docker start vertebral_labeling', shell=True, check=True, stderr=subprocess.DEVNULL)
		except subprocess.CalledProcessError as e:
			subprocess.run('sudo -S docker start vertebral_labeling', shell=True, check=True)
			
		command183='docker cp '+str(i)+' vertebral_labeling:/home/'+os.path.basename(str(i))
		command184='sudo docker cp '+str(i)+' vertebral_labeling:/home/'+os.path.basename(str(i))			
		os.system(command183)
		command185='docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling python3 spine4.py'
		command186='sudo docker exec -e SCT_DIR=''/spinalcordtoolbox'' -e PATH=''/spinalcordtoolbox/bin:$PATH'' -it vertebral_labeling python3 spine4.py'
		os.system(command185)
		command187='docker exec -it vertebral_labeling chmod -R 777 /home/'+os.path.basename(str(i))+'/'+os.path.basename(str(i))+'_csa.csv'
		command188='sudo docker exec -it vertebral_labeling chmod -R 777 /home/'+os.path.basename(str(i))+'/'+os.path.basename(str(i))+'_csa.csv'
		os.system(command187)
		command189='docker cp vertebral_labeling:/home/'+os.path.basename(str(i))+'/'+os.path.basename(str(i))+'_csa.csv'+' '+str(i)+'/'+os.path.basename(str(i))+'_csa.csv'
		command190='sudo docker cp vertebral_labeling:/home/'+os.path.basename(str(i))+'/'+os.path.basename(str(i))+'_csa.csv'+' '+str(i)+'/'+os.path.basename(str(i))+'_csa.csv'
		os.system(command189)
		command191='docker exec -it vertebral_labeling rm -r /home/'+os.path.basename(str(i))
		command192='sudo docker exec -it vertebral_labeling rm -r /home/'+os.path.basename(str(i))
		os.system(command191)
		with open(str(i)+'/'+os.path.basename(str(i))+'_csa.csv', 'r', encoding='utf-8') as file:
			sp = csv.reader(file)
			for row in sp:
				v.append(row)		
		k.append(os.path.basename(str(i)))
		b1.append(os.path.basename(str(i)))		
		for j in range(len(v)):
			if v[j][4] == '1':
				f = j
				w = ((float(v[f][6])*math.cos((math.radians(float(v[f][8]))))+((float(v[f][6]))*math.cos(math.radians(float(v[f][10]))))))/(2)
				k.append(str(w))
				b1.append(str(v[f][16]))
		for j in range(len(v)):		
			if v[j][4] == '2':
				f = j
				w = ((float(v[f][6])*math.cos((math.radians(float(v[f][8]))))+((float(v[f][6]))*math.cos(math.radians(float(v[f][10]))))))/(2)
				k.append(str(w))
				b1.append(str(v[f][16]))
		for j in range(len(v)):
			if v[j][4] == '3':
				f = j
				w = ((float(v[f][6])*math.cos((math.radians(float(v[f][8]))))+((float(v[f][6]))*math.cos(math.radians(float(v[f][10]))))))/(2)
				k.append(str(w))
				b1.append(str(v[f][16]))
		with open(csvf, 'a', newline='') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(k)
		with open(eccf, 'a', newline='') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(b1)
		update_progress_bar(idx + 1, len(file_paths))	
			
	command169='docker stop vertebral_labeling'
	command170='docker stop vertebral_labeling'
	os.system(command169)
	command171='docker rm vertebral_labeling'
	command172='docker rm vertebral_labeling'
	os.system(command171)				
										
	progress_label.config(text="Extraction Done!")
	progress_window.update()
	progress_window.after(4000, progress_window.destroy)
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				subfolder_path = os.path.join(directory, subfolder)
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('_csa.csv' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')						
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mEMPTY FOLDER\033[0m")
						output_file.write(f"{subfolder} EMPTY FOLDER" + '\n')						
					else:
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[91m\033[1mFAILED (MISSING EXTRACTION FILE .csv)\033[0m")
						output_file.write(f"{subfolder}.nii.gz FAILED (MISSING EXTRACTION FILE .csv)" + '\n')
                			
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mDATA EXTRACTION FINISHED\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mDATA EXTRACTION FINISHED WITH WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mDATA EXTRACTION FAILED\033[0m")
	else:	      			
		check_subfolders(str(before), str(before)+'/DataExtractionResults.txt')	

#############################	

def ext_singularity():
	print('\033[94m\033[1mPLEASE SELECT THE\033[0m \033[92m\033[1mEnigma-SC\033[0m \033[94m\033[1mFOLDER\033[0m')
	enigma_folder = tkfilebrowser.askopendirname()
	if not enigma_folder:
		print('\033[91m\033[1mNo folder selected.\033[0m')
		return
	print('The \033[92m\033[1mEnigma-SC\033[0m folder selected is located at: '+enigma_folder)
	
	print('\033[94m\033[1mNOW SELECT THE DESIRED\033[0m \033[92m\033[1mSUBFOLDERS\033[0m \033[94m\033[1mFROM THE PREPARED FOLDER:\033[0m')		 			 	       	
	file_paths = tkfilebrowser.askopendirnames()
	if not file_paths:
		print('\033[91m\033[1mNo folders selected.\033[0m')
		return
		
	print ('\033[92m\033[1mSelected subfolders:\033[0m')
	for file_path in file_paths:
		print(file_path)
		
	before = str(file_paths[0])
	before = os.path.dirname(before)
	
	data = ["subject", "CSA C1", "CSA C2", "CSA C3"]
	data2 = ["subject", "Mean(eccentricity) C1", "Mean(eccentricity) C2", "Mean(eccentricity) C3"]
	now = datetime.now()
	hour = str(now.strftime("%m-%d-%Y_%H-%M-%S"))
	before = str(file_paths[0])
	before = os.path.dirname(before)
	csvf = before +'/csa_final_table_'+hour+'.csv'
	eccf = before +'/eccentricity_table'+hour+'.csv'
	
	with open(csvf, mode='w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(data)
	print('CSA final table saved on '+str(csvf))
	
	with open(eccf, mode='w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(data2)
	print('eccentricity final table saved on '+str(eccf))	
	
	if not file_paths:
		print('\033[91m\033[1mNo folders selected.\033[0m')
		return
		
	print ('\033[92m\033[1mSelected folders:\033[0m')
	for file_path in file_paths:
		print(file_path)
		
	progress_window = tk.Toplevel()
	progress_window.title("Data Extraction Progress")

	progress_label = tk.Label(progress_window, text="Extracting...")
	progress_label.pack()

	progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate")
	progress_bar.pack()

	progress_text = tk.Label(progress_window, text="")
	progress_text.pack()
	
	progress_bar["value"] = 0
	progress_text["text"] = "0% done"
	progress_window.update()
	
	path = enigma_folder+'/vertebral_labeling.simg/home'
	dir_list = os.listdir(path)
	for i in dir_list:
		if 'SCT' not in i:
			if 'datav2' not in i:
				if 'scripts' not in i:
					command21='rm -rf '+path+'/'+str(i)
					command22='sudo rm -rf '+path+'/'+str(i)
					os.system(command21)
					
	def update_progress_bar(current, total):
		progress_percent = int((current / total) * 99)
		progress_bar["value"] = progress_percent
		progress_text["text"] = f"{progress_percent}% done"
		progress_window.update()
		
	exit_code = os.system("singularity --version")
	exity_code = os.system("apptainer --version")
	if exit_code and exity_code != 0:
    		print('\033[91m\033[1mSINGULARITY AND APPTAINER NOT INSTALLED. Please install on of them before running this script.\033[0m')
    		raise SystemExit(1)		
				
	for idx,i in enumerate(file_paths):
		v = []
		k = []
		b1 = []
		
		
		subprocess.run('cd '+before+'/'+os.path.basename(str(i))+' && '+'cp -r '+str(i)+' '+enigma_folder+'/vertebral_labeling.simg/home/'+os.path.basename(str(i)), shell=True)		
		#cmd_1='singularity exec --writable --env HOST_USER=$(whoami) --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ python3 /spine4.py'
		#cmd_2='apptainer exec --writable --env HOST_USER=$(whoami) --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ python3 /spine4.py'
		cmd_1 = 'singularity exec --writable --no-home --containall --env HOST_USER=$(whoami) '+enigma_folder+'/vertebral_labeling.simg python3 /spine4.py'
		cmd_2 = 'apptainer exec --writable --no-home --containall --env HOST_USER=$(whoami) '+enigma_folder+'/vertebral_labeling.simg python3 /spine4.py'		
		try:		
			subprocess.run(cmd_1, shell=True, check=True)
		except subprocess.CalledProcessError:	
			subprocess.run(cmd_2, shell=True, check=True)				
		os.system('chmod -R 777 '+enigma_folder+'/vertebral_labeling.simg/home/'+os.path.basename(str(i))+'/'+os.path.basename(str(i))+'_csa.csv')	
		os.system('mv '+enigma_folder+'/'+'vertebral_labeling.simg/home/'+os.path.basename(str(i))+'/'+os.path.basename(str(i))+'_csa.csv'+' '+str(i)+'/'+os.path.basename(str(i))+'_csa.csv')
		cmdd_1='singularity exec --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ rm -rf /home/'+os.path.basename(str(i))
		cmdd_2='apptainer exec --writable --no-home --containall --bind $HOST_TMPDIR:/tmp --bind /dev/null:/etc/resolv.conf ' + enigma_folder + '/vertebral_labeling.simg/ rm -rf /home/'+os.path.basename(str(i))
		try:		
			subprocess.run(cmdd_1, shell=True, check=True)
		except subprocess.CalledProcessError:
			subprocess.run(cmdd_2, shell=True, check=True)					
		with open(str(i)+'/'+os.path.basename(str(i))+'_csa.csv', 'r', encoding='utf-8') as file:
			sp = csv.reader(file)
			for row in sp:
				v.append(row)		
		k.append(os.path.basename(str(i)))
		b1.append(os.path.basename(str(i)))		
		for j in range(len(v)):
			if v[j][4] == '1':
				f = j
				w = ((float(v[f][6])*math.cos((math.radians(float(v[f][8]))))+((float(v[f][6]))*math.cos(math.radians(float(v[f][10]))))))/(2)
				k.append(str(w))
				b1.append(str(v[f][16]))
		for j in range(len(v)):		
			if v[j][4] == '2':
				f = j
				w = ((float(v[f][6])*math.cos((math.radians(float(v[f][8]))))+((float(v[f][6]))*math.cos(math.radians(float(v[f][10]))))))/(2)
				k.append(str(w))
				b1.append(str(v[f][16]))
		for j in range(len(v)):
			if v[j][4] == '3':
				f = j
				w = ((float(v[f][6])*math.cos((math.radians(float(v[f][8]))))+((float(v[f][6]))*math.cos(math.radians(float(v[f][10]))))))/(2)
				k.append(str(w))
				b1.append(str(v[f][16]))
		with open(csvf, 'a', newline='') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(k)
		with open(eccf, 'a', newline='') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(b1)
		update_progress_bar(idx + 1, len(file_paths))					
										
	progress_label.config(text="Extraction Done!")
	progress_window.update()
	progress_window.after(4000, progress_window.destroy)
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				subfolder_path = os.path.join(directory, subfolder)
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('_csa.csv' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')						
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mEMPTY FOLDER\033[0m")
						output_file.write(f"{subfolder} EMPTY FOLDER" + '\n')						
					else:
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[91m\033[1mFAILED (MISSING EXTRACTION FILE .csv)\033[0m")
						output_file.write(f"{subfolder}.nii.gz FAILED (MISSING EXTRACTION FILE .csv)" + '\n')
                			
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mDATA EXTRACTION FINISHED\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mDATA EXTRACTION FINISHED WITH WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mDATA EXTRACTION FAILED\033[0m")
	else:	      			
		check_subfolders(str(before), str(before)+'/DataExtractionResults.txt')	
		
#############################	

def pack():
	print('\033[94m\033[1mPLEASE SELECT THE DESIRED\033[0m \033[92m\033[1mSUBFOLDERS\033[0m \033[94m\033[1mFROM THE PREPARED FOLDER:\033[0m')
	file_paths = tkfilebrowser.askopendirnames()
	if not file_paths:
		print('\033[91m\033[1mNo folders selected.\033[0m')
		return
		
	print ('\033[92m\033[1mSelected folders:\033[0m')
	for file_path in file_paths:
		print(file_path)
		
	before = str(file_paths[0])
	before = os.path.dirname(before)
	
	progress_window = tk.Toplevel()
	progress_window.title("Packing Progress")

	progress_label = tk.Label(progress_window, text="Packing...")
	progress_label.pack()

	progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate")
	progress_bar.pack()

	progress_text = tk.Label(progress_window, text="")
	progress_text.pack()
	
	progress_bar["value"] = 0
	progress_text["text"] = "0% done"
	progress_window.update()
	
	def update_progress_bar(current, total):
		progress_percent = int((current / total) * 99)
		progress_bar["value"] = progress_percent
		progress_text["text"] = f"{progress_percent}% done"
		progress_window.update()	
	
	for idx, i in enumerate(file_paths):
		
		os.system('cd '+str(before)+' && zip -r '+os.path.basename(str(i))+'.zip'+' '+os.path.basename(str(i))+' -x '+os.path.basename(str(i))+'/'+os.path.basename(str(i))+'.nii.gz')
		update_progress_bar(idx + 1, len(file_paths))
	progress_label.config(text="Packing Done!")
	progress_window.update()
	progress_window.after(4000, progress_window.destroy)	
	print ('\033[92m\033[1mDATA PACKED AND READY TO GO!\033[0m')
	print ('\033[94m\033[1mZIP files located at: '+str(before)+'\033[0m')		
			
#############################

def open_checkbox_window():
    checkbox_window = tk.Toplevel(root)
    checkbox_window.title("Choose Platform")

    def on_checkbox_click():
        choice = "Docker" if container_choice.get() == "Docker" else "Singularity/Apptainer"
        checkbox_window.destroy()
        automated(choice)

    container_choice = tk.StringVar()

    checkbox_frame = tk.Frame(checkbox_window)
    checkbox_frame.pack(side="top", pady=(10, 0))

    docker_button = tk.Radiobutton(checkbox_frame, text="Docker", variable=container_choice, value="Docker")
    docker_button.pack(side="left", padx=(0, 10))

    singularity_button = tk.Radiobutton(checkbox_frame, text="Singularity/Apptainer", variable=container_choice, value="Singularity/Apptainer")
    singularity_button.pack(side="left")

    ok_button = tk.Button(checkbox_window, text="OK", command=on_checkbox_click)
    ok_button.pack(side="top", pady=(10, 0))

    button_x, button_y, _, _ = ok_button.bbox("insert")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = root.winfo_x() + button_x
    y_position = root.winfo_y() + button_y

    checkbox_window.geometry(f"300x85+{x_position}+{y_position}")

def automated(choice):
    if choice:
        if choice == "Docker":
            docker()
        elif choice == "Singularity/Apptainer":
            singularity()
            
#############################

def open_SCT():
    checkbox_window = tk.Toplevel(root)
    checkbox_window.title("Choose Platform")

    def on_checkbox_click():
        choice = "Docker" if container_choice.get() == "Docker" else "Singularity/Apptainer"
        checkbox_window.destroy()
        automated_SCT(choice)

    container_choice = tk.StringVar()

    checkbox_frame = tk.Frame(checkbox_window)
    checkbox_frame.pack(side="top", pady=(10, 0))

    docker_button = tk.Radiobutton(checkbox_frame, text="Docker", variable=container_choice, value="Docker")
    docker_button.pack(side="left", padx=(0, 10))

    singularity_button = tk.Radiobutton(checkbox_frame, text="Singularity/Apptainer", variable=container_choice, value="Singularity/Apptainer")
    singularity_button.pack(side="left")

    ok_button = tk.Button(checkbox_window, text="OK", command=on_checkbox_click)
    ok_button.pack(side="top", pady=(10, 0))

    button_x, button_y, _, _ = ok_button.bbox("insert")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = root.winfo_x() + button_x
    y_position = root.winfo_y() + button_y

    checkbox_window.geometry(f"300x85+{x_position}+{y_position}")

def automated_SCT(choice):
    if choice:
        if choice == "Docker":
            modal_docker()
        elif choice == "Singularity/Apptainer":
            modal_singularity() 
            
#############################

def open_browse():
    checkbox_window = tk.Toplevel(root)
    checkbox_window.title("Select File Format")

    def on_checkbox_click():
        choice = ".nii.gz" if container_choice.get() == ".nii.gz" else "BIDS"
        checkbox_window.destroy()
        automated_browse(choice)

    container_choice = tk.StringVar()

    checkbox_frame = tk.Frame(checkbox_window)
    checkbox_frame.pack(side="top", pady=(10, 0))

    docker_button = tk.Radiobutton(checkbox_frame, text=".nii.gz", variable=container_choice, value=".nii.gz")
    docker_button.pack(side="left", padx=(0, 10))

    singularity_button = tk.Radiobutton(checkbox_frame, text="BIDS", variable=container_choice, value="BIDS")
    singularity_button.pack(side="left")

    ok_button = tk.Button(checkbox_window, text="OK", command=on_checkbox_click)
    ok_button.pack(side="top", pady=(10, 0))

    button_x, button_y, _, _ = ok_button.bbox("insert")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = root.winfo_x() + button_x
    y_position = root.winfo_y() + button_y

    checkbox_window.geometry(f"300x85+{x_position}+{y_position}")

def automated_browse(choice):
    if choice:
        if choice == ".nii.gz":
            browse_folder_niigz()
        elif choice == "BIDS":
            browse_folder_BIDS() 
            
#############################

def open_reg():
    checkbox_window = tk.Toplevel(root)
    checkbox_window.title("Select Platform")

    def on_checkbox_click():
        choice = "Docker" if container_choice.get() == "Docker" else "Singularity/Apptainer"
        checkbox_window.destroy()
        automated_reg(choice)

    container_choice = tk.StringVar()

    checkbox_frame = tk.Frame(checkbox_window)
    checkbox_frame.pack(side="top", pady=(10, 0))

    docker_button = tk.Radiobutton(checkbox_frame, text="Docker", variable=container_choice, value="Docker")
    docker_button.pack(side="left", padx=(0, 10))

    singularity_button = tk.Radiobutton(checkbox_frame, text="Singularity/Apptainer", variable=container_choice, value="Singularity/Apptainer")
    singularity_button.pack(side="left")

    ok_button = tk.Button(checkbox_window, text="OK", command=on_checkbox_click)
    ok_button.pack(side="top", pady=(10, 0))

    button_x, button_y, _, _ = ok_button.bbox("insert")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = root.winfo_x() + button_x
    y_position = root.winfo_y() + button_y

    checkbox_window.geometry(f"300x85+{x_position}+{y_position}")

def automated_reg(choice):
    if choice:
        if choice == "Docker":
            reg_aut_docker()
        elif choice == "Singularity/Apptainer":
            reg_aut_singularity() 
            
#############################

def open_ext():
    checkbox_window = tk.Toplevel(root)
    checkbox_window.title("Select Platform")

    def on_checkbox_click():
        choice = "Docker" if container_choice.get() == "Docker" else "Singularity/Apptainer"
        checkbox_window.destroy()
        container_ext(choice)

    container_choice = tk.StringVar()

    checkbox_frame = tk.Frame(checkbox_window)
    checkbox_frame.pack(side="top", pady=(10, 0))

    docker_button = tk.Radiobutton(checkbox_frame, text="Docker", variable=container_choice, value="Docker")
    docker_button.pack(side="left", padx=(0, 10))

    singularity_button = tk.Radiobutton(checkbox_frame, text="Singularity/Apptainer", variable=container_choice, value="Singularity/Apptainer")
    singularity_button.pack(side="left")

    ok_button = tk.Button(checkbox_window, text="OK", command=on_checkbox_click)
    ok_button.pack(side="top", pady=(10, 0))

    button_x, button_y, _, _ = ok_button.bbox("insert")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = root.winfo_x() + button_x
    y_position = root.winfo_y() + button_y

    checkbox_window.geometry(f"300x85+{x_position}+{y_position}")

def container_ext(choice):
    if choice:
        if choice == "Docker":
            ext_docker()
        elif choice == "Singularity/Apptainer":
            ext_singularity()                                               
            
#############################

def open_tutorial():
    url = "https://github.com/art2mri/Enigma-SC" 
    webbrowser.open_new(url)
    
#############################	

root = tk.Tk()
root.title("Enigma-SC")

window_width = 520
window_height = 860
root.geometry(f"{window_width}x{window_height}")
root.configure(bg='gray')

image_path = "files/gustavojarola.png"  
img = Image.open(image_path)

img = img.resize((250, 250))

img = ImageTk.PhotoImage(img)

title_label = tk.Label(root, text="Spinal Cord Segmentation", bg='gray', font=("Helvetica", 20, "bold"))
title_label.pack(pady=10)

subtitle_label = tk.Label(root, text="Spinal Cord Toolbox", bg='gray', font=("Helvetica", 16))
subtitle_label.pack(pady=5)

image_label = tk.Label(root, image=img, bg='gray')
image_label.pack()

images_path_button = tk.Button(root, text="Prepare Folders", height=2, width=20, command=open_browse, highlightbackground="black", highlightthickness=2)
spinal_cord_segmentation_button = tk.Button(root, text="Spinal Cord Segmentation", height=2, width=20, command=open_SCT, highlightbackground="black", highlightthickness=2)
label_text = tk.Label(root, text="Spinal Cord Vertebral Labeling", bg='gray', font=("Helvetica", 15, "bold"))

images_path_button.pack(pady=10)
spinal_cord_segmentation_button.pack(pady=10)
label_text.pack(pady=10)

button_frame = tk.Frame(root, bg='gray')
button_frame.pack(pady=10)

automated_frame = tk.Frame(button_frame, bg='darkgray', padx=4, pady=4, highlightbackground="black", highlightthickness=2)
automated_frame.grid(row=0, column=0, padx=(10, 22), pady=(10,10))

container_choice = tk.StringVar()
container_choice.set("")

automated_button = tk.Button(automated_frame, text="Automated", height=2, width=17, command=open_checkbox_window, highlightbackground="black", highlightthickness=2)
automated_button.pack(fill='both', expand=True, pady=(0, 5))

manual_frame = tk.Frame(button_frame, bg='darkgray', padx=4, pady=4, highlightbackground="black", highlightthickness=2)
manual_frame.grid(row=0, column=1, padx=(22, 10), pady=(10,10))

manual_button = tk.Button(manual_frame, text="Manual", height=2, width=17,command=manual, highlightbackground="black", highlightthickness=2)
manual_button.pack(fill='both', expand=True, pady=(0, 5))

spinal_cord_registration_automated = tk.Button(automated_frame, text="Spinal Cord Registration", height=2, width=17, command=open_reg, highlightbackground="black", highlightthickness=2)
spinal_cord_registration_automated.pack(fill='both', expand=True)

spinal_cord_registration_manual = tk.Button(manual_frame, text="Spinal Cord Registration", height=2, width=17, command=reg_man, highlightbackground="black", highlightthickness=2)
spinal_cord_registration_manual.pack(fill='both', expand=True)

additional_button_frame = tk.Frame(root, bg='gray')
additional_button_frame.pack(pady=10)

data_extraction = tk.Button(additional_button_frame, text="Data Extraction", height=2, width=20, command=open_ext, highlightbackground="black", highlightthickness=2)
send_button = tk.Button(additional_button_frame, text="Pack and Send", height=2, width=20, command=pack, highlightbackground="black", highlightthickness=2)

data_extraction.pack(pady=(10, 10))
send_button.pack(pady=(10, 10))

version_label = tk.Label(root, text="Version 2.0", bg='gray', font=("Helvetica", 11, "bold"))
version_label.place(relx=1.0, rely=1.0, anchor='se', bordermode='outside', x=-10, y=-10)

tutorial_button = tk.Button(root, text="Tutorial", height=1, width=5, highlightbackground="black", highlightthickness=2, command=open_tutorial)
tutorial_button.place(relx=0.0, rely=1.0, anchor='sw', bordermode='outside', x=10, y=-10)

button_frame.grid_columnconfigure(0, weight=1)
additional_button_frame.grid_columnconfigure(0, weight=1)

root.mainloop()
