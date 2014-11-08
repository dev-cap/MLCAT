import java.io.BufferedWriter;
import java.io.FileWriter;

import org.jsoup.select.Elements;


public class To_CC_Sum
{
	String msgid;
	String To;
	String CC;
	int to_no; 
	int cc_no;
	
	int total_to_cc;
	
	To_CC_Sum(String msgid)
	{
		this.msgid = msgid;
	}
	
	public void SetTo(String to_list)
	{
		this.To = to_list;
		calc_To();
	}
	
	public void SetCC(String cc_list)
	{
		this.CC = cc_list;	
		calc_CC();
	}
	
	public void calc_To()
	{
		String to_arr[] = To.split(" ");
		to_no  = to_arr.length;
	}
	
	public void calc_CC()
	{
		String cc_arr[] = CC.split(" ");
		cc_no  = cc_arr.length;
	}
	
	public void write_to_cc()
	{
		total_to_cc = to_no + cc_no;
		try {
            BufferedWriter outfile = new BufferedWriter(new FileWriter("to_cc_info.txt", true));	
            outfile.write(System.getProperty("line.separator"));
           	outfile.write(msgid+" , "+total_to_cc);
            outfile.close(); 
		 	 }catch(Exception e)  {System.out.println("exception"); }
	}
	
	
	
	
	
}
