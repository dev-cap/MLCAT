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

public class URLRestPages 
{
		
	String next_pg_link;
	public URLRestPages(String next_pg_link) 
	{
		this.next_pg_link = next_pg_link;
	}
	
	
	public void write_pagelinks()
	{
		Document doc;
		String href_list="";
		{
			
			try {
				
				// need http protocol
				doc = Jsoup.connect(next_pg_link).get();
				// get all links
				Elements links = doc.select("a[href]");	
				//to remove last few unwanted links
				for (int i = 0; i<10; i++)
					links.remove(links.size() - 1);
				
				Iterator<Element> itr = links.iterator();
				//to remove first few unwanted links
				itr.next();
				itr.remove();
				itr.next();
				itr.remove();
				
				// link for next page given to class URLRestPages
				String next_pg = itr.next().attr("href");
				next_pg_link = "http://www.spinics.net/lists/alsa-devel/" + next_pg;
				//URLRestPages urp = new URLRestPages(next_pg_link)
				//itr.remove();
				
				 try {
		             //Write labels and corresponding fields to text file
		             BufferedWriter outfile = new BufferedWriter(new FileWriter("page_list.txt", true));
		             outfile.write(next_pg_link);
		             outfile.write(System.getProperty("line.separator"));
		             outfile.close();
		         }
		         catch(Exception e) 
		         {
		             System.out.println("Exception");
		         }
						
			} catch (IOException e) {
				e.printStackTrace();
			}
			
		
		}
	}
	
	public void read_pagelinks()
	{
		BufferedReader br;
		try 
		{
			br = new BufferedReader(new FileReader("page_list.txt"));
		    String line="";
		    //sending each link in page_list.txt to get info scraped
		    while (line != null) 
		    {
		       line = br.readLine();
		       get_all_msgid(line);
		    }
		    //System.out.println(line);
		    br.close();
		} 
	    
	    catch(Exception e) 
	     	{
	         System.out.println("End");
	     	}
	    
	}
	
	public void get_all_msgid(String link)
	{
		Document doc;
		String href_list;
			 
		{
			
			try {
				// need http protocol
				doc = Jsoup.connect(link).get();
				// get all links
				Elements links = doc.select("a[href]");	
				//to remove last few unwanted links
				for (int i = 0; i<10; i++)
					links.remove(links.size() - 1);
				
				Iterator<Element> itr = links.iterator();
				//to remove first few unwanted links
				itr.next();
				itr.remove();
				itr.next();
				itr.remove();
				
				 try {
		             //Write labels and corresponding fields to text file
		             BufferedWriter outfile = new BufferedWriter(new FileWriter("msgid_list.txt", true));	
		             outfile.write(System.getProperty("line.separator"));
		             
		       
		             while(itr.hasNext()) 
		             {
		            	 // get the value from href attribute
		            	 Elements link_page = (itr.next().select("a[href]"));
		            	 href_list = link_page.attr("href");
		            	 outfile.write(href_list+"\n");
		            	System.out.println(".");
		             }
		             outfile.close(); 
				 	 }catch(Exception e)  {System.out.println("End"); }
			} catch (IOException e) {e.printStackTrace();}
				 
		}
				
	}

}
