
import sys
import os
import ntpath
import Tkinter
import tkFileDialog
import struct
import traceback
import tkMessageBox


class Init:
	
	def __init__(self, root):
		
		Tkinter.Grid.rowconfigure(root, 0, weight=1)
		Tkinter.Grid.columnconfigure(root, 0, weight=1)
		
		frame = Tkinter.Frame(root)
		frame.grid(row = 0, column = 0, sticky = Tkinter.N + Tkinter.S + Tkinter.E + Tkinter.W)
		
		Tkinter.Button(frame, text = "Input Dir", command = self.get_in_dir).grid(row = 0, column = 0, sticky = Tkinter.W)
		self.input_entry = Tkinter.Entry(frame, width = 70)
		self.input_entry.grid(row = 0, column = 1, sticky = Tkinter.W)
		
		
		Tkinter.Button(frame, text = "Output Dir", command = self.get_out_dir).grid(row = 1, column = 0, sticky = Tkinter.W)
		self.output_entry = Tkinter.Entry(frame, width = 70)
		self.output_entry.grid(row = 1, column = 1, sticky = Tkinter.W)
		
		
		self.type_to_options = [
			"1  (Byte: 8-bit unsigned)",
			"2  (Integer: 16-bit signed)",
			"3  (Integer: 32-bit signed)",
			"4  (Floating-point: 32-bit single precision)",
			"5  (Floating-point: 64-bit double precision)",
			"12 (Integer: 16-bit unsigned)",
			"13 (Integer: 32-bit unsigned)",
			"14 (Integer: 64-bit signed)",
			"15 (Integer: 64-bit unsigned)"
		]
		
		Tkinter.Label(frame, text = "Convert To:").grid(row = 2, column = 0, sticky = Tkinter.W)
		
		self.type_to_var = Tkinter.StringVar(frame)
		self.type_to_var.set(self.type_to_options[5])
		
		type_to_option = Tkinter.OptionMenu(frame, self.type_to_var, *self.type_to_options)
		type_to_option.grid(row = 2, column = 1, sticky = Tkinter.W)
		
		Tkinter.Button(frame, text = "Start!", command = self.outer).grid(row = 3, column = 1, sticky = Tkinter.W)
		
	def get_in_dir(self):
		infile = tkFileDialog.askdirectory()
		if infile != "":
			self.input_entry.delete(0, Tkinter.END)
			self.input_entry.insert(0, infile)
			
	def get_out_dir(self):
		outdir = tkFileDialog.askdirectory()
		if outdir != "":
			self.output_entry.delete(0, Tkinter.END)
			self.output_entry.insert(0, outdir)
			
	def show_alert(self, msg):
		top = Tkinter.Toplevel()
		txt = Tkinter.Text(top, width = 120, height = 40)
		txt.insert(Tkinter.END, msg)
		txt.update()
		txt.pack()
		
	def get_out_type(self):
		return self.type_to_var.get().split()[0].strip()
		
		
	"""
	1 = Byte: 8-bit unsigned integer
	2 = Integer: 16-bit signed integer
	3 = Long: 32-bit signed integer
	4 = Floating-point: 32-bit single-precision
	5 = Double-precision: 64-bit double-precision floating-point
	6 = Complex: Real-imaginary pair of single-precision floating-point
	9 = Double-precision complex: Real-imaginary pair of double precision floating-point
	12 = Unsigned integer: 16-bit
	13 = Unsigned long integer: 32-bit
	14 = 64-bit long integer (signed)
	15 = 64-bit unsigned long integer (unsigned)
	"""
	def get_mult_and_code(self, dtype):
		
		if dtype == "1":
			return 1, "b"
		
		if dtype == "2":
			return 2, "h"
		
		if dtype == "3":
			return 4, "i"
		
		if dtype == "4":
			return 4, "f"
		
		if dtype == "5":
			return 8, "d"
		
		if dtype == "12":
			return 2, "H"
		
		if dtype == "13":
			return 4, "I"
		
		if dtype == "14":
			return 1, "q"
		
		if dtype == "15":
			return 1, "Q"
		
		return 0, ""
		
	def out_type_is_integral(self, dtype):
		if dtype == "1" or dtype == "2" or dtype == "3" or dtype == "12" or dtype == "13" or dtype == "14" or dtype == "15":
			return True
		else:
			return False
			
	def outer(self):
		
		try:
			indir  = self.input_entry.get()
			outdir = self.output_entry.get()
			
			if indir == outdir:
				tkMessageBox.showerror("Error", "input and output directories must be different.")
				return
			
			for f in os.listdir(indir):
				if not(f.endswith(".hdr")) and not(os.path.isdir(os.path.join(indir, f))):
					self.go(os.path.join(indir, f), outdir)
		except:
			exc_type, exc_value, exc_trace = sys.exc_info()
			lines = traceback.format_exception(exc_type, exc_value, exc_trace)
			tkMessageBox.showerror("Error", "".join(line for line in lines))
			
		
	def go(self, in_dat_path, out_dir):
		
		print("go...")
		in_hdr_path = ""
		
		if in_dat_path.rfind(".") == -1:
			in_hdr_path = in_dat_path + ".hdr"
		else:
			base = in_dat_path[:in_dat_path.rfind(".")]
			in_hdr_path = base + ".hdr"
		
		if not(os.path.exists(in_hdr_path)):
			tkMessageBox.showerror("Error", in_hdr_path + " does not exist.")
			return
			
		if not(os.path.exists(in_dat_path)):
			tkMessageBox.showerror("Error", in_dat_path + " does not exist.")
			return
		
		if not(os.path.exists(out_dir)):
			tkMessageBox.showerror("Error", out_dir + " does not exist.")
			return
			
		out_dat_path = os.path.join(out_dir, ntpath.basename(in_dat_path))
		out_hdr_path = os.path.join(out_dir, ntpath.basename(in_hdr_path))
		
		print("in hdr:  " + in_hdr_path)
		print("in dat:  " + in_dat_path)
		print("out hdr: " + out_hdr_path)
		print("out dat: " + out_dat_path)
		
		in_type  = ""
		out_type = self.get_out_type()
		
		print("out type: " + out_type)
		
		in_code  = ""
		in_mult  = 0
		out_code = ""
		out_mult = 0
		
		# copy the headers
		with open(in_hdr_path, "r") as fin, open(out_hdr_path, "w") as fout:
			for line in fin:
				if line.startswith("data type"):
					temp = line.split("=")
					in_type = temp[1].strip()
					line = temp[0].strip() + " = " + out_type + "\n"
					fout.write(line)
				else:
					fout.write(line)
			fout.write("generating software = convert_types.py: converted from " + in_dat_path + "\n")
		
		in_mult, in_code  = self.get_mult_and_code(in_type)
		
		print("in mult: " + str(in_mult))
		print("in code: " + in_code)
		
		if in_mult == 0:
			tkMessageBox.showerror("Error", "unsupported data type: " + in_type)
			return
			
		out_mult, out_code = self.get_mult_and_code(out_type)
		
		print("out mult: " + str(out_mult))
		print("out code: " + out_code)
		
		if out_mult == 0:
			tkMessageBox.showerror("Error", "unsupported data type: " + out_type)
			return
		
		chunk = 2**23
		
		with open(in_dat_path, "rb") as fin, open(out_dat_path, "wb") as fout:
			while True:
				s = fin.read(chunk)
				if s == "":
					break
				t = struct.unpack(in_code * (len(s) / in_mult), s)
				#if self.out_type_is_integral(out_type):
				#	t = tuple(int(x) for x in t)
				s = struct.pack(out_code * len(t), *t)
				fout.write(s)
		
		print("Done!")
		
		
master = Tkinter.Tk()
init = Init(master)
master.mainloop()
