def main():
        t1='Team 1'
        t2='Team 2'
        data=[]
        j=0
        outfile=open('output.html','w')
        f=open('move.txt','r')
        for lines in f:
                move=lines.strip('\n')
                data.append(move.split(" "))
                j=j+1
        end=data.pop()
        if int(end[0])==1:
                winner=t1.split('.')[0]
        else:
                winner=t2.split('.')[0]
        tor=data[-1][-1]
        if int(tor)>0:
                angle='10'
        else:
                angle='-10'
        
                
        outfile.write( """
<html>
<head>
<style>
body {background-color:#D2B48C;}
#bench {position:absolute;top:400px;left:200px}
\n""")
        for i in range(1,13,1):
                outfile.write( '#B1-'+str(i)+'{background-color:#D00000;text-align:center;font-size:20px;width:30px;height:50px;position:absolute;top:110px;left:'+str(170+i*32)+'px}\n')
                outfile.write( '#B2-'+str(i)+'{background-color:#00CCFF;text-align:center;font-size:20px;width:30px;height:50px;position:absolute;top:110px;left:'+str(680+i*32)+'px}\n')

        outfile.write("""
#B0-3 {background-color:green;text-align:center;font-size:20px;width:30px;height:50px;position:absolute;top:350px;left:530}
#stand1{background-color:black;width:10px;height:100px;position:absolute;top:430px;left:560}
#stand2{background-color:black;width:10px;height:100px;position:absolute;top:430px;left:620}
#tor1{position:absolute;top:518px;left:555px;text-align:center;font-family:arial;color:black;font-size:17px;}
#tor2{position:absolute;top:518px;left:615px;text-align:center;font-family:arial;color:black;font-size:17px;}
#turn{width:280px;height:25px;position:absolute;top:200px;left:510px;text-align:center;font-family:arial;color:white;font-size:20px;border:5px solid black;padding:15px;}
#pl1{position:absolute;top:45px;left:250px;font-family:arial;color:red;font-size:26px;}
#pl2{position:absolute;top:45px;left:760px;font-family:arial;color:blue;font-size:26px;}
#stat{position:absolute;top:200px;left:70px;text-align:center;font-family:arial;color:black;font-size:20px;border:2px solid black;padding:5px;}

</style>
<title>Game</title>
</head>
<body>
\n""")
        for i in range(1,13,1):
                outfile.write( '<div id="B1-'+str(i)+'"> \n')
                outfile.write( str(i)+'\n</div>\n')
                outfile.write( '<div id="B2-'+str(i)+'"> \n')
                outfile.write( str(i)+'\n</div>\n')
                
        outfile.write( """
<div id="B0-3">3</div>
<div id="stand1"></div>
<p id="tor1">6</p>
<div id="stand2"></div>
<p id="tor2">-6</p>
<p id="pl1"> Player 1</p>
<p id="pl2">Player 2</p>
<img id="bench" src="http://cs.nyu.edu/~ma2795/bench.png" width="930px" heigth="30px"/>
\n""")
        outfile.write( '<p id="stat">Player 1 time= '+end[1]+'s<br>Player 2 time= '+end[2]+'s</p>\n')
        outfile.write( """
<script>
function rotate(elem, angle){
        //Cross-browser:
        var css = ["-moz-","-webkit-","-ms-","-o-","",""]
                   .join("transform:rotate(" + angle + "deg);")
        elem.style.cssText += ";" + css;
}

document.getElementById("stat").style.visibility="hidden";
var move=new Array();
\n""")
        outfile.write( 'var winner="'+winner+'"\n')
        outfile.write( 'var angle="'+angle+'"\n')
        outfile.write( 'var p1="'+t1.split('.')[0]+'"\n')
        outfile.write( 'var p2="'+t2.split('.')[0]+'"\n')
        outfile.write( 'document.getElementById("pl1").innerHTML="Player 1: "+p1;\n')
        outfile.write( 'document.getElementById("pl2").innerHTML="Player 2: "+p2;\n')
        t=0
        endlist=[]
        endlist.append("B0-3")
        modelist=[""]*35
        modelist[11]="B0-3"
        for element in data:
                outfile.write( "move["+str(t)+"]=new Array();\n")
                if int(element[3])==1:
                        block="B1-"+str(element[2])
                elif int(element[3])==2:
                        block="B2-"+str(element[2])
                elif int(element[3])==0:
                        block="B0-3"
                if int(element[0])==1:
                        modelist[15+int(element[1])]=block
                elif int(element[0])==2:
                        block=modelist[15+int(element[1])]

                if block in endlist:
                        endlist.remove(block)
                else:
                        endlist.append(block)
                outfile.write( "move["+str(t)+"][0]="+str(element[0])+"\n")
                outfile.write( "move["+str(t)+"][1]="+str(element[1])+"\n")
                outfile.write( 'move['+str(t)+'][2]="'+block+'"\n')
                outfile.write( "move["+str(t)+"][3]="+str(element[4])+"\n")
                outfile.write( "move["+str(t)+"][4]="+str(element[5])+"\n")
                t=t+1

        outfile.write( "var steps="+str(len(data))+'\n')

        outfile.write( 'function removeEnd(){\n')
         
        for b in endlist:
                outfile.write( 'var block=document.getElementById("'+b+'");\n')
                outfile.write( "block.style.top='555px';\n")
        outfile.write( "block.style.top='555px';\n")
        outfile.write( "}\n")
        
        outfile.write("""
var animate;
var current=0;
function moveBlock(){
        var obj = document.getElementById(move[current][2]);
        obj.style.position= 'absolute';
         if(current%2==0){document.getElementById("turn").innerHTML="Player 1: "+p1;}
         else {document.getElementById("turn").innerHTML="Player 2: "+p2;}
        if (move[current][0]==1){
                obj.style.top = '350px';
                obj.style.left = 200+30*(15+move[current][1]) + 'px';
        }
        else{
                obj.style.top = '610px';
        }
         document.getElementById("tor1").innerHTML=move[current][3];
         document.getElementById("tor2").innerHTML=move[current][4];
        current++;
        if(current<steps){
         animate = setTimeout(moveBlock,1300);
        
         }
         
        else{
         removeEnd();
         rotate(document.getElementById("bench"), angle)
         document.getElementById("stat").style.visibility="visible";
        document.getElementById("turn").innerHTML="Winner is: "+winner;
        
        }
}

</script>
<p id="win"><p>
<p id="turn">Press Start</p>
<input type="button" value="Start" onclick="moveBlock();" />
</body>
</html>""")


main()
