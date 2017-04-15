for f in ./data/*;
do (cat "${f}"; echo) >> sakai-devel.mbox; 
done
