# Flask backend API for fleet

## Login:
- **/Authorize**  [POST]
- _Request_  : 
    - {"**email_id**":"xxxx@mail.com","**passwd**":"yyyy"}
- _Response_ : 
    - {"**status**":"True","**reason**":"successfull"}
    - {"**status**":"False","**reason**":"Incorrect Password"}
    - {"**status**":"False","**reason**":"Incorrect Username"}

## Signup OTP generate:
- __/SignUpOTP__  [POST]
- _Request_  :  
    - {"**email_id**":"xxxx@mail.com"}
- _Response_ : 
    - {"**status**":"True","**reason**":"not exist and OTP send"}
    - {"**status**":"False","**reason**":"already exist"}

## Signup OTP verify:
- __/VerifyOTP__  [POST]
- _Request_  : 
    - {"**email_id**":"xxxx@mail.com","**otp**":"yyyy"}
- _Response_ : 
    - {"**status**":"True","**reason**":"successfull"}
    - {"**status**":"False","**reason**":"Wrong OTP"}
    - {"**status**":"False","**reason**":"Wrong email"}

## Signup register:
- __/Signup__  [POST]
- _Request_  : 
    - {"**email_id**":"xxxx@mail.com","**passwd**":"yyyy","**company_name**":"zzz","**address**":"aaa","**phonenumber**":"1234567890","**zipcode**":"123456","**country**":"bbb"}
- _Response_ : 
    - {"**status**":"True","**reason**":"successfull"}
    - {"**status**":"False","**reason**":"OTP not verified"}
    - {"**status**":"False","**reason**":"OTP expired"}

## App Register:
- __/AppReg__  [POST]
- _Request_  :
    - {"**email_id**":"xxxx@mail.com","**employee_name**":"xxxx","**phonenumber**":"1234567890","**designation**":"yyyy"}
- _Response_ : 
    - {"**status**":"True","**reason**":"successful","**appid**":"xxx"}
    - {"**status**":"False","**reason**":"Wrong email"}

## App List:
- __/AppList__  [POST]
- _Request_  :
    - {"**email_id**":"xxxx@mail.com"}
- _Response_ : 
    - {"**status**":"True","**reason**":"successful","**applist**":[{"x":"xxx", "y":"123456789", "z":"yyy", "a":"appxxx"}]}
    - {"**status**":"False","**reason**":"Wrong email"}

## App Detail:
- __/AppDetail__  [POST]
- _Request_  :
    - {"**email_id**":"xxxx@mail.com","**appid**","xxx"}
- _Response_ : 
    - {"**status**":"True","**reason**":"successful","**appdetail**":{"x":"xxx", "y":"123456789", "z":"yyy", "a":"appxxx"}]}
    - {"**status**":"False","**reason**":"appid not exist"}
    - {"**status**":"False","**reason**":"Wrong email"}

## App Edit:
- __/AppEdit__  [POST]
- _Request_  :
    - {"**email_id**":"xxxx@mail.com","**appid**","xxx"}
- _Response_ : 
    - {"**status**":"True","**reason**":"successful"}
    - {"**status**":"False","**reason**":"appid not exist"}
    - {"**status**":"False","**reason**":"Wrong email"}

## App Remove:
- __/AppRemove__  [POST]
- _Request_  :
    - {"**email_id**":"xxxx@mail.com","**appid**","xxx"}
- _Response_ : 
    - {"**status**":"True","**reason**":"successful"}
    - {"**status**":"False","**reason**":"appid not exist"}
    - {"**status**":"False","**reason**":"Wrong email"}

## User Detail:
- __/UserDetail__  [POST]
- _Request_  :
    - {"**email_id**":"xxxx@mail.com"}
- _Response_ : 
    - {"**status**":"True","**reason**":"successful","**userdetail**":{"x":"xxx", "y":"123456789", "z":"yyy", "a":"appxxx"}]}
    - {"**status**":"False","**reason**":"Wrong email"}

## Location:
- __/Location__  [POST]
- _Request_  :
    - {"**email_id**":"xxxx@mail.com","**appid**","xxx"}
- _Response_ : 
    - {"**status**":"True","**reason**":"successful","**trackingdetail**":{"location":{"type": "POINT", "coordinates":[80.2,13.01]},"datetime":"1997-04-22 06:30:45"}]}
    - {"**status**":"False","**reason**":"appid not exist"}
    - {"**status**":"False","**reason**":"Wrong email"}