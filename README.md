# Flask backend API for fleet

## Login:
    **/Authorize** [POST]
    *Request*  : {"email_id":"xxxx@mail.com","passwd":"yyyy"}
    *Response* : {"status":"True","reason":"successfull"}
               {"status":"True","reason":"Incorrect Password"}
               {"status":"True","reason":"Incorrect Username"}

## Signup OTP generate:
    **/SignUpOTP** [POST]
    *Request*  : {"email_id":"xxxx@mail.com"}
    *Response* : {"status":"True","reason":"not exist and OTP send"}
               {"status":"True","reason":"already exist"}

## Signup OTP verify:
    **/VerifyOTP** [POST]
    *Request*  : {"email_id":"xxxx@mail.com","otp":"yyyy"}
    *Response* : {"status":"True","reason":"successfull"}
               {"status":"True","reason":"Wrong OTP"}
               {"status":"True","reason":"Wrong email"}

## Signup register:
    **/Signup** [POST]
    *Request*  : {"email_id":"xxxx@mail.com","passwd":"yyyy","company_name":"zzz","address":"aaa","phonenumber":"1234567890","zipcode":"123456","country":"bbb"}
    *Response* : {"status":"True","reason":"successfull"}
               {"status":"True","reason":"OTP not verified"}
               {"status":"True","reason":"OTP expired"}