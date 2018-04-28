# README #

### Timeline Component ###

##### version 0.1.0 #####
##### Created by Richard Burns | richardburns@gmail.com #####

### Functions ###

#### Playback ####
`Play ()` |  `op.timeline.Play()`  
`Pause ()` | `op.timeline.Pause()`  
`Stop ()` | `op.timeline.Stop()`  
`Gotosection ( [string] section name )` | `op.timeline.Gotosection("cue001")`  
`Gotosectionid ( [string] section id )` | `op.timeline.Gotosection("44b80849_8e09_43e8_a7a8_a16ba0500c2e")`  
`Gotosectionandwait ( [string] section name )` | `op.timeline.Gotosectionandwait("cue001")`  
`Gotonextsection ()` | `op.timeline.Gotonextsection()`  
`Gotoprevioussection ()` | `op.timeline.Gotoprevioussection()`  

#### Getters ####
`Getlength ()` |  `l = op.timeline.Getlength()`  
`Getrate ()` |  `r = op.timeline.Getrate()`  
`Gettimecode ()` |  `tc = op.timeline.Gettimecode()`  

#### Setters ####
`Setlength ( [int] frame length )` | `op.timeline.Setlength(1000)`  
`Setlooping ( [bool] looping )` | `op.timeline.Setlooping(True)`  
`Setrate ( [int] rate )` | `op.timeline.Setrate(60)`  
`Setframe ( [int] frame )` | `op.timeline.Setrate(1000)`  
`Settimecode ( [string] timecode )` | `op.timeline.Settimecode("01:01:10.20")`  
`Addsection ( [string] name )` | `op.timeline.Addsection("cue001")`  

#### Utilities ####

`Framestotimecode ( [int] frames , [int] rate )` | `tc = op.timeline.Framestotimecode(600,60)`  
`Timecodetoframes ( [string] timecode , [int] rate )` | `fc = op.timeline.Timecodetoframes("00:01:02.03",60)`  
`Rerangesections ( [int] old rate , [int] new rate )` | `op.timeline.Rerangesections(25,50)`  
`Createid ()` | `id = op.timeline.Createid()	`  
`Updatesectionmenus ()` | `op.timeline.Updatesectionmenus()`
`Deletesectionsbyrow ( [int] row id )` | `op.timeline.Deletesectionsbyrow(1)`  