

from surveys import *

# db.create_all()
def login_required(f):
    """ Checks if the user is logged in or not """
    @wraps(f)
    def decorated_function(*args, **kwargs):


        email =kwargs["email"]
        exist = survey.query.filter_by(email=email).first()
        if  exist is not None:
            abort(401,'you are not authorized to make survey again ') 
        check =bcrypt.check_password_hash(kwargs["token"].replace("ahmed","/"),str( email+''+app.secret_key))
        
        if check:
            return f(*args, **kwargs)
        else :

            abort(401)




    return decorated_function
#take file name file ext csv and read the data 
def readcsv(filename):
    File = open(filename)
    Reader = csv.reader(File)
    Data = list(Reader)

    return Data



def SendMail(sendermail,recipient,body):
    subject =  "Survey For You %s" %recipient[1]
    msg = Message(subject, sender = "cervisoft", recipients = recipient)
    msg.body = "Please visit this link (%s) Link will redirect to page" %(body)

    mail.send(msg)


def MakeUrlThatWillBeSent(email):
    token = bcrypt.generate_password_hash(str( email+''+app.secret_key))
    token= token.replace("/", "ahmed")
    url = str("http://192.168.1.6:5000/"+'survey/%s/%s/'%(email,token))
    # request.base_url[:-9]
    return url

#read file of contacts and get mail send mails to them 
@app.route('/SendMails', methods=['POST','GET'])
def sendMailsToAllrecps():
    emails =readcsv("mails.csv")
    emails = emails[1:]
    for email in emails :
        body =MakeUrlThatWillBeSent(email[0])
        SendMail(app.config['MAIL_USERNAME'],email,body)
        

    return str(emails)


''' Views  '''
@app.route('/survey/<string:email>/<string:token>/', methods=['GET','POST'])

@login_required
def HomePage(email=None,token=None):
    if request.method == 'POST':
        
        
        name= request.form['name']
        
        rad = request.form['rad']

        ip  = request.remote_addr

        
        s1 = survey(name=name,email= email,ip =ip,answer=rad)
        db.session.add(s1)

        db.session.commit() 
        return str("thanks %s for your survey " %(name))
    else :
        return render_template('survey.html')

def makeSurveysSerializable():

    surveys =survey.query.filter().all()

    listSurveys =[]

    
    for s in surveys:

            
        listSurveys.append({"name":s.name,"ip":s.ip, "email":s.email,
        "answer":s.answer})
    
    return listSurveys



@app.route('/getSurveys', methods=['GET'])
def home():

    
    surveys =makeSurveysSerializable()
    js = json.dumps(surveys)
    resp = Response(js, status=200, mimetype='application/json')
    

    return resp

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jJHDmN]LWX/,?RT'
    app.debug = True
    
    app.run(host='0.0.0.0', threaded = True)
            
