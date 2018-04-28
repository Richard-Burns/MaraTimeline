# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
# 
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.

def onValueChange(par, val, prev):
	sections = op(me.parent().par.Sectionsdat)
	s = me.parent().par.Sections.val
	s = s.split("_")
	r = int(s[1])

	if par.name == "Rate":
		me.parent().Setrate(val)

	if par.name == "Sections":
		me.parent().par.Timecode2 = sections[r,"Timecode"]
		me.parent().par.Extendmode = sections[r,"End Condition"]

	if par.name == "Timecode2":

		sections[r,'Timecode'] = val
	
	if par.name == "Extendmode":
		sections[r,'End Condition'] = val


	return

def onPulse(par):
	if par.name == "Play":
		me.parent().Play()
		
	if par.name == "Pause":
		me.parent().Pause()
		
	if par.name == "Stop":
		me.parent().Stop()
		
	if par.name == "Addsection":
		name = me.parent().par.Name
		if name != "":
			me.parent().Addsection(name,me.parent().par.Extendcondition)
			me.parent().par.Name = ""
			
	if par.name == "Gotonextsection":
		me.parent().Gotonextsection()
		
	if par.name == "Gotoprevsection":
		me.parent().Gotoprevioussection()

	if par.name == "Deletesection":
		s = me.parent().par.Sections.val
		s = s.split("_")
		me.parent().Deletesectionbyrow(int(s[1]))

	return

def onExpressionChange(par, val, prev):
	return

def onExportChange(par, val, prev):
	return

def onEnableChange(par, val, prev):
	return

def onModeChange(par, val, prev):
	return
	