import speedtest  
  
  
st = speedtest.Speedtest()

print(round(st.download()/1000000))  

print(round(st.upload()/1000000))  
  