public class MainClass 
{      
    public static void main(String args[]) 
    {         
        Cmd command = Cmd.valueOf(args[0]);         
        command.run();     
    }      
    
    private enum Cmd 
    {          
        extract_URL 
        {            
            @Override 
            public void run() 
            {                
                new URLFirstPage();             
            }
        },         
        extract_URL_info 
        {             
            @Override             
            public void run() 
            {                 
                new MessageExtract();             
            }
        };          
        public abstract void run();     
    } 
}
