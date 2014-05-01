import simplejson as json
import sys

error_codes ={
	#global
	'200' : {"msg_en": 'Success',"msg_cn":""},
	'400' : {"msg_en": 'Bad request',"msg_cn":""},
	'401' : {"msg_en": 'You are not authoried to access this service',"msg_cn":""},
	'403' : {"msg_en": 'Forbidden by server',"msg_cn":""},
	'404' : {"msg_en": 'Service not found',"msg_cn":""},
	'414' : {"msg_en": 'Prameters missing',"msg_cn":""},
	'500' : {"msg_en": 'Internal error happen',"msg_cn":""},
	#login 
	'001' : {"msg_en": "Email or password is not correct.","msg_cn":""}, 
	#register
	'011' : {"msg_en": "Email is exist","msg_cn":""},
	'012' : {"msg_en": "Password is too simple","msg_cn":""},
	'013' : {"msg_en": "","msg_cn":""},
	'014' : {"msg_en": "","msg_cn":""},
}

def get_config(key):
    config = {
        'session_expire' : 30,
        'md5_random' : 'youdontknow',
        'default_portrait_name' : 'default_portrait.png',
    }
    return config[key]

def get_result(code=None):
	if(type(code)==int):
		code = "%03d"%code
	if(code!=None and error_codes.has_key(code)):
		return json.dumps(error_codes[code])
	else:
		return None

def dumps_error_config():
	return json.dumps(error_codes)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print 'please give function you want to access...'
		sys.exit(0)
	if 'dumps' == sys.argv[1]:
		print dumps_error_config()
	elif 'config_test' == sys.argv[1]:
		get_config(001)
