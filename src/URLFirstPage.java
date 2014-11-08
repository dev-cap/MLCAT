import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.util.*;


public class URLFirstPage
{
	
	Document doc;
	String href_list;
		 
	{
		
		try {
			// need http protocol
			doc = Jsoup.connect("http://www.spinics.net/lists/alsa-devel/").get();
			// get all links
			Elements links = doc.select("a[href]");	
			//to remove last few unwanted links
			for (int i = 0; i<10; i++)
				links.remove(links.size() - 1);
			
			Iterator<Element> itr = links.iterator();
			//to remove first few unwanted links
			itr.next();
			itr.remove();
			
			//getting the link of next page of the mailing list
			String next_pg = itr.next().attr("href");
			String next_pg_link = "http://www.spinics.net/lists/alsa-devel/" + next_pg;
			URLRestPages urp = new URLRestPages(next_pg_link);
				
			//System.out.println(next_pg_link);
			
			
			//itr.remove();
			
		
			
			while(itr.hasNext()) 
			{
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
				 	 }catch(Exception e)  {System.out.println("End"); 
				 	e.printStackTrace();
				 	 
				 	 }
			}
			/*
			itr = links.iterator();
			while(itr.hasNext()) 
			{
				// get the value from href attribute
				System.out.println("...." + href_list);
			}
			*/
	
			while (urp.next_pg_link.toLowerCase().contains("thrd"))
			{
				
				System.out.println("*");
				urp.write_pagelinks();	
			}
	
			
			urp.read_pagelinks();	
	 
		} catch (IOException e) {
			e.printStackTrace();
		}
	
	}

}
