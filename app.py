from flask import*
import mysql.connector
import random
import datetime
import socket

#connection_timeout=3000
my=mysql.connector.connect(host="b674oycwegn7xfg3iltb-mysql.services.clever-cloud.com",user="un4d7o5fdqli8v4n",password="GvUQkj5im2FvXGp4qVmp",database="b674oycwegn7xfg3iltb",connection_timeout=30000)
cur=my.cursor(buffered=True)
#cur=my.cursor()


app=Flask(__name__)
app.secret_key="fhwekfiweljlsdjo"


  
@app.route("/")
def cookies():
    c=request.cookies.get("cookieid")

    if c:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("setcookie"))
    


@app.route("/Settingcookies")
def setcookie():

    ran=random.randint(1,100000)

    cval = socket.gethostname()
    ip = socket.gethostbyname(cval)

    ran=str(ran)
    

    ipad=str(ip)
    coval=str(cval+ran)



   
    cur.execute("INSERT INTO users (cookiesid,ipadd) VALUES(%s,%s)", (coval,ipad,))

    
   

    max_age_in_years = 500
    max_age_in_seconds = max_age_in_years * 365.25 * 24 * 60 * 60

    



    co=make_response(redirect(url_for("cookies")))
    co.set_cookie("cookieid",value=str(coval),max_age=int(max_age_in_seconds))

    my.commit()

    return co
    
@app.route("/Home",methods=["POST","GET"])
def home():

    lis=None
    showdat=None

    

    lis=[]


    co=request.cookies.get("cookieid")
    if co:
        pass
    else:
        return redirect(url_for("setcookie"))

   
    
   
    
   
    cur.execute("SELECT question,answer FROM usersrequest WHERE cookiesid=%s",(co,))
    datafetch=cur.fetchall()

    
    if datafetch:
            for question,answer  in datafetch:
               
                    
                lis.append({"question":question,"answers":answer})
        
        
        
    else:
            showdat=" "
   
           
    
    
   
           
            
   
            
            
    if request.method=="POST":
        q=request.form["query"]

        pattern = f"%{q}%"

        try:
          cur.execute("SELECT answers FROM responses WHERE prompt LIKE %s or prompt REGEXP %s",(pattern,q,))
          al=cur.fetchall()
          if al:
                ran=random.choice(al)[0]
          else:
                ran=f"TrainIt don't have a response for this query.You can train TrainIt for this query"

            
          cur.execute("INSERT INTO usersrequest (cookiesid,question,answer) VALUES(%s,%s,%s)",(co,q,ran,))
          my.commit()
        
   

          return redirect(url_for("home"))
         except Exception as e:
           return f"{e}"
        
        
        
    return render_template("home.html",showdat=showdat,lis=lis)


@app.route("/Addingaflagtoanswer<answerid>")
def addflag(answerid):
    answerk=str(answerid)

    try:
        cur.execute("UPDATE responses SET flagged=COALESCE(flagged, 0) + 1 WHERE answers=%s", (answerk,))
        my.commit()
        return render_template("reporting.html")
    except:
        pass

    try:
        cur.execute("SELECT flagged FROM responses where answers=%s",(answerk,))
        num=cur.fetchall()

        for nu in num:
            numb=int(nu[0])
            if numb>=5:
                cur.execute("DELETE FROM responses WHERE answers=%s",(answerk,))
                my.commit()
                
            else:
                pass
    except:
        pass
    
    return redirect(url_for("home"))

@app.route("/SubmitResponses",methods=["POST","GET"])
def submit():
    if request.method=="POST":
        ques=request.form["query"]
        ans=request.form["answer"]

        cur.execute("INSERT INTO responses (prompt,answers) VALUES(%s,%s)",(ques,ans,))
        my.commit()

        return render_template("thankyou.html")
        
    return render_template("submit.html")
#app.run(debug=True,host="0.0.0.0",port=8000)
    
#{{url_for('addflag',answerid=i['answers'])}}

        
