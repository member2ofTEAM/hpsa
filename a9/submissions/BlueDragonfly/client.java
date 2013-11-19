import java.io.*;
import java.net.*;
import java.util.*;
public class client {
	//static String endmsg = "<EOM>";
	static String proName = "./a.out";
	static String host = "127.0.0.1";
	static int port;
	static Socket sock = null;
	static PrintWriter out = null;
	static BufferedReader in = null;
	static String teamname = "Blue Dragonfly";
	static int M, N;
	static char turn;

	static Runtime runtime = null;
	static Process process = null;
	static BufferedReader inexe = null;	
	static PrintWriter outexe = null;
	public static String ReceiveFromServer() throws IOException{
		int t;
		String s = "";
		while(!s.contains("<EOM>")){
			t = in.read();
			s+=(char)t;
		}
		s = s.replace("<EOM>","");
		//s = s.replace(" ", "\n");
		//System.out.println("receive " + s +" from server");
		return s;
	}
	
	public static void SendToServer(String data){
		//data+="<EOM>";
		out.println(data);
		System.out.println("c->s: " + data);
	}
	
	public static String ReceiveFromProgram() throws IOException{
		String s = inexe.readLine();
		//Scanner kb = new Scanner(System.in);
		//String s = kb.nextLine();
		//System.out.println("receive " + s + " from program");
		return s;
	}
	
	public static void SendToProgram(String data){
		outexe.println(data);
		//System.out.println("s->c: " + data);
	}
	
	public static void startProgram() throws IOException{
		runtime = Runtime.getRuntime();
		process = runtime.exec("./a.out");
		inexe = new BufferedReader(new InputStreamReader(process.getInputStream()));	
		outexe = new PrintWriter(process.getOutputStream(), true);
	}
	public static void main(String[] args) throws IOException{
		  try{
			  //Port number
			  port = Integer.parseInt(args[0]);
			  
			  //build socket
			  System.out.println("Connecting to port" + port);
			  sock = new Socket(host, port);
			  out = new PrintWriter(sock.getOutputStream(), true);
			  in = new BufferedReader(new InputStreamReader(sock.getInputStream()));
			  
			  //connected
			  System.out.println("Connected!!");
			  
			  //Get server welcome message
			  String data;
			  System.out.println("Waiting fro welcome message");
			  data = ReceiveFromServer();
			  
			  //send team name
			  System.out.println("Sending Teamname");
			  SendToServer(teamname);
			  
			  //execute program
			  System.out.println("starting program!!");
			  startProgram();
			  System.out.println("start successful!!");
			
			//start
			String line;
			System.out.println("starting the game!!");
			while(true){
				line = ReceiveFromServer();
				SendToProgram(line);
				
				line = ReceiveFromProgram();
				while(!(line.length() > 0 && line.charAt(0) == '-')){
					line = ReceiveFromProgram();
				}
				
				SendToServer(line.substring(1));
			}
			
			 
				 
		  }catch (UnknownHostException e) {
				System.err.printf("Unknown host: %s:%d\n",host,port);
				System.exit(1);
		} 
		  catch(IOException e){
			  System.out.println(e);
			  System.exit(1);
		  }
	  }//end main method
}//end class

