import java.io.IOException;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.util.*;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.BufferedReader;
import java.io.FileReader;

public class MessageExtract 
{

	{
	try 
	{
		BufferedReader br;
		br = new BufferedReader(new FileReader("msgid_list.txt"));
	    String line="";
	    //sending each link in page_list.txt to get info scraped
	    while ((line != null)) 
	    {
	       System.out.println("Hello");
	       line = br.readLine();
	       
	       if (line.toLowerCase().contains("msg"))
	       write_msg_info(line);
	    }
	    //System.out.println(line);
	    br.close();
	} 
    
    catch(Exception e) 
     	{
         System.out.println("End");
     	}
	}

	public void write_msg_info(String msgId)
	{
		String infoFrmURL= "http://www.spinics.net/lists/alsa-devel/"+msgId;
		Document doc;
		//String href_list="";
		{
			
			try {
				
				// need http protocol
				doc = Jsoup.connect(infoFrmURL).get();
				Elements ul = doc.select("ul");
				//System.out.println("ul :" + ul);
				Iterator<Element> itr = ul.iterator();
				Element first = itr.next();
				Elements li_list = first.select("li");
				Iterator<Element> itr_li_list = li_list.iterator();
				itr_li_list .next();
				itr_li_list .next();
				itr_li_list .remove();
				itr_li_list .next();
				itr_li_list .next();
				itr_li_list .remove();
				//itr_li_list .next();
				//itr_li_list .next();
				
				//System.out.println("li :" + li_list);
				try {
		             //Write labels and corresponding fields to text file
		             BufferedWriter outfile = new BufferedWriter(new FileWriter("msg_info.txt", true));
		             outfile.write(System.getProperty("line.separator"));
		             outfile.write("---"+msgId);
		             // give msg id to To_CC_Sum to calculate the sum of its to and cc
		             To_CC_Sum tcs = new To_CC_Sum(msgId);
		             
		             //System.out.println("---"+msgId);
		             
		             for(Element i: li_list)
		             {
		            	 Element str = i.select("em").first();
		            	 Document dc = Jsoup.parse(str.toString());
					
		            	 String em = dc.text();
					
		            	 //String attr =i.select("a[href]").attr("href");
		            	 String attr =i.select("a[href]").text();
		            	 
		            	 outfile.write("\n*"+em+":"+attr);
		            	 System.out.println("^");
		            	 //System.out.println("\n*"+em+":"+attr);
		            	 
		            	 //to pass to and from of corresponding msgid
		            	 
		            	 if (em.equals("To"))
		            	 {
		            		 tcs.SetTo(attr);
		            	 }
		            	 else if(em.equals("Cc"))
		            	 {
		            		 tcs.SetCC(attr);
		            	 }
		        
		             }
		             //add to and cc and write back to file
		             tcs.write_to_cc();
		           		             
		             outfile.close();
		         	}catch(Exception e) 
		         	{System.out.println("Exception");}
						
			} catch (IOException e) {
				e.printStackTrace();
			}
			
		
		}
	}


}
