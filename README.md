# Flask backend API for fleet

## Login:
- **/Authorize**  [POST]
- _Request_  : 
    - {"**email_id**":"xxxx@mail.com","**passwd**":"yyyy"}
- _Response_ : 
    - {"**status**":"True","**reason**":"successfull"}
    - {"**status**":"True","**reason**":"Incorrect Password"}
    - {"**status**":"True","**reason**":"Incorrect Username"}

## Signup OTP generate:
- __/SignUpOTP__  [POST]
- _Request_  :  
    - {"**email_id**":"xxxx@mail.com"}
- _Response_ : 
    - {"**status**":"True","**reason**":"not exist and OTP send"}
    - {"**status**":"True","**reason**":"already exist"}

## Signup OTP verify:
- __/VerifyOTP__  [POST]
- _Request_  : 
    - {"**email_id**":"xxxx@mail.com","**otp**":"yyyy"}
- _Response_ : 
    - {"**status**":"True","**reason**":"successfull"}
    - {"**status**":"True","**reason**":"Wrong OTP"}
    - {"**status**":"True","**reason**":"Wrong email"}

## Signup register:
- __/Signup__  [POST]
- _Request_  : 
    - {"**email_id**":"xxxx@mail.com","**passwd**":"yyyy","**company_name**":"zzz","**address**":"aaa","**phonenumber**":"1234567890","**zipcode**":"123456","**country**":"bbb"}
- _Response_ : 
    - {"**status**":"True","**reason**":"successfull"}
    - {"**status**":"True","**reason**":"OTP not verified"}
    - {"**status**":"True","**reason**":"OTP expired"}

## App Register:
- __/AppReg__  [POST]
- _Request_  :
    - {"**email_id**":"xxxx@mail.com","**employee_name**":"xxxx","**phonenumber**":"1234567890","**designation**":"yyyy"}
- _Response_ : 
    - {"**status**":"True","**reason**":"successful","**appid**":"xxx"}
    - {"**status**":"True","**reason**":"Wrong email"}

## App List:
- __/AppList__  [POST]
- _Request_  :
    - {"**email_id**":"xxxx@mail.com"}
- _Response_ : 
    - {"**status**":"True","**reason**":"successful","**applist**":[["xxx", "123456789", "yyy", "appxxx"]]}
    - {"**status**":"True","**reason**":"Wrong email"}