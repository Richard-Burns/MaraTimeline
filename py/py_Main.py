import uuid

class Main:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.o = ownerComp
		self.t = ownerComp.op('local/time')
		self.sections = op(ownerComp.par.Sectionsdat)
	
	# Timeline control functions
	
	def Play(self):
		self.t.play = 1
		self.o.par.Playing = 1
		return
		
	def Pause(self):
		self.t.play = 0
		self.o.par.Playing = 0
		return
	
	def Stop(self):
		self.t.play = 0
		self.t.frame = 1
		self.o.par.Playing = 0
		return
		
	def Gotosection(self,name):
		timecode = self.sections[name,"Timecode"]
		self.o.Settimecode(timecode)
	
	def Gotosectionid(self,id):
		timecode = self.sections[id,"Timecode"]
		self.o.Settimecode(timecode)
		
	def Gotosectionandwait(self,name):
		timecode = self.sections[name,"Timecode"]
		self.o.Settimecode(timecode)
		self.o.Pause()
		
	def Gotonextsection(self):
		curtimecode = self.o.Gettimecode()
		rate = self.o.Getrate()
		curframe = self.o.Timecodetoframes(curtimecode,rate)
		sortop = op('sort1')
		
		for r in range(1,sortop.numRows):
			tc = sortop[r,'Timecode'].val
			tf = self.o.Timecodetoframes(tc,rate)
			
			if tf > curframe:
				self.o.Gotosectionid(sortop[r,'Id'])
				break
			else:
				self.o.Setframe(self.t.end)
		return
		
	def Gotoprevioussection(self):
		curtimecode = self.o.Gettimecode()
		sp = op('speed1')
		sc = sp['chan1']

		rate = self.o.Getrate()
		curframe = self.o.Timecodetoframes(curtimecode,rate)
		sortop = op('sort1')
		maxval = sortop.numRows
		reval = maxval-1
		for r in range(1,maxval):
			if reval == 1:
				self.o.Setframe(1)
			tc = sortop[reval,'Timecode'].val
			tf = self.o.Timecodetoframes(tc,rate)
			if tf < curframe:
				if sc >= 1.0:
					sp.par.reset.pulse()
					self.o.Gotosectionid(sortop[reval,'Id'])
				else:
					if op('null_info')['play'] == 1:
						self.o.Gotosectionid(sortop[reval-1,'Id'])
					else:
						self.o.Gotosectionid(sortop[reval,'Id'])
				break
			
			reval = reval-1

		return
		
	# Getters
	
	def Getlength(self):
		return self.t.end
	
	def Getrate(self):
		return self.t.rate
		
	def Gettimecode(self):
		return self.t.timecode
		
	# Setters
		
	def Setlength(self, length):
		self.t.start = 1
		self.t.end = length
		self.t.rangeStart = 1
		self.t.rangeEnd = length
		return
	
	def Setlooping(self, looping):
		if looping:
			self.t.loop = 1
		else:
			self.t.loop = 0
		return
			
	def Setrate(self, rate):
		oldrate = self.t.rate
		self.t.rate = rate
		self.o.par.Rate = self.t.rate
		self.o.Rerangesections(oldrate,rate)
		return
	
	def Setframe(self, frame):
		self.t.frame = frame
		return
		
	def Settimecode(self, timecode):
		self.t.timecode = timecode
		return
		
	def Addsection(self,name, extend):
		if not self.sections:
			c = self.o.create(tableDAT,"sections")
			self.o.par.Sections = './'+c.name
			c.nodeX = 400
			c.nodeY = -150
			c.clear()
			c.appendRow(['Name','Timecode'])
		t = self.o.Gettimecode()
		id = self.Createid()
		d = self.sections.appendRow([id, name,t,extend])
		self.Updatesectionmenus()
		return
		
	def Endsectionid(self, id):
		ec = self.sections[id, "End Condition"]
		tc = self.sections[id, "Timecode"]
		ns = self.sections[id, "Goto"]
		if ec == "Hold":
			self.Pause()
		elif ec == "Loop":
			self.Settimecode(tc)
		elif ec == "Goto":
			if ns:
				self.Gotosectionid(ns)

		return

	# Utilities
	
	def Framestotimecode(self, frame, rate):
		frame = frame-1
		h = frame / (3600*rate)
		m = frame / (60*rate) % 60
		s = frame / rate % 60
		f = frame % rate
		timecode =  "%02d:%02d:%02d.%02d" % (h, m, s, f)

		return timecode
		
	def Timecodetoframes(self,timecode,rate):
		timecode = timecode.replace('.', ':')
		timesplit = timecode.split(":")
		hours = (int(timesplit[0])*3600)*rate
		minutes = (int(timesplit[1])*60)*rate
		seconds = (int(timesplit[2]))*rate
		frames = int(timesplit[3])
		totalframes = frames+seconds+minutes+hours+1
		return totalframes
	
	def Rerangesections(self, oldrate, newrate):
		for r in range(1, self.sections.numRows):
			tc = self.sections[r,'Timecode'].val
			oldf = self.o.Timecodetoframes(tc,oldrate)
			newtc = self.o.Framestotimecode(oldf, newrate)
			self.sections[r,'Timecode'] = newtc
		return
			
			
	def Createid(self):
		uid = str(uuid.uuid4())
		uid = uid.replace("-", "_")
		return uid
	
	def Updatesectionmenus(self):
		labels = []
		names = []
		c = self.sections.col('Name')
		for r in c:
			if r.row > 0:
				labels.append(r.val)
				names.append("section_"+str(r.row))

		self.o.par.Sections.menuLabels = labels
		self.o.par.Sections.menuNames = names

		if len(labels) == 0:
			self.o.par.Sections.enable = False
			self.o.par.Deletesection.enable = False
			self.o.par.Timecode2.enable = False
			self.o.par.Extendmode.enable = False
		else:
			self.o.par.Sections.enable = True
			self.o.par.Deletesection.enable = True
			self.o.par.Timecode2.enable = True
			self.o.par.Extendmode.enable = True

		return

	def Deletesectionbyrow(self, row):
		self.sections.deleteRow(row)
		self.Updatesectionmenus()
		self.o.par.Sections.val = 0
		return