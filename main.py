from requests import request
from sys import exit as Exit
from datetime import datetime as dt
import argparse as ap
import json

null = None
true = True
false = False

config_file = open('config.json')
config = json.load(config_file)
config_file.close()


functions = config.get('functions')
func_querystring = config.get('func_querystring')
models = config.get('models')
visuals = config.get('visualFeatures')
languages = config.get('languages')
payload = config.get('payload')
headers = config.get('headers')
url = config.get('url')

def gen_querystring(func):
	"""
	The function `gen_querystring` generates a query string dictionary based on the input function.
	
	:param func: The parameter `func` is a function that is passed as an argument to the
	`gen_querystring` function

	:return: The function `gen_querystring` returns a dictionary object containing the query string
	parameters extracted from the input function.
	"""
	querystring = {}
	for i in func_querystring.get(functions.get(func)):
		if len(i) > 0:
			q = {i[0]:i[1]}
			querystring.update(q)
		else:
			pass

	return querystring

def make_post_request(api_url,payload_dict,qs):
	"""
	The function `make_post_request` sends a POST request to an API URL with a payload dictionary,
	headers, and query string parameters, and returns the JSON response or the response text if the JSON
	decoding fails.
	
	:param api_url: The URL of the API endpoint where the POST request will be sent

	:param payload_dict: The payload_dict parameter is a dictionary that contains the data that you want
	to send in the request body. This data will be converted to JSON format before sending the request
	
	:param qs: The `qs` parameter is a dictionary of query string parameters that will be appended to
	the URL. These parameters are used to provide additional information to the server
	
	:return: the response from the API request. If the response can be parsed as JSON, it will return
	the JSON data. Otherwise, it will return the response text.
	"""

	response = request("POST", api_url, json=payload_dict, headers=headers, params=qs)
	try:
		return response.json()
	except json.decoder.JSONDecodeError:
		return response.text


def return_response(response):
	"""
	To return `response` when it is called outside a function
	"""

	return response

def cur_timestamp():
	"""
	Generate the current timestamp
	"""

	return str(int(round(dt.now().timestamp())))


def count_value(value):
	"""
	The function `count_value` takes a value as input and returns the value if it is greater than 1,
	returns 1 if the value is 1 or less, and prints an error message and returns 1 if the value is
	negative.
	
	:param value: The parameter "value" is a variable that represents the input value that needs to be
	counted
	:return: the value passed as an argument if it is not equal to 1 or less than 0. If the value is
	equal to 1, it will return 1 and print a message if the 'auto' key in the 'config' dictionary is not
	set to True. If the value is less than 0, it will return 1 and print a message if the
	"""

	if value == 1:
		if not config.get('auto'):
			print('1 is the default value')
		return 1
	elif value < 0:
		if not config.get('auto'):
			print('Invalid value. Set to default value')
		return 1
	else:
		return value



parser = ap.ArgumentParser()



parser.add_argument("--setdefault",type=str)
# ------------------------------------
parser.add_argument("--analyze",type=str)
parser.add_argument("--visual",type=str,choices=[i for i in visuals.values()]) # analyze
parser.add_argument("--detail",type=str,choices=[i for i in models.values()]) # analyze
# ------------------------------------
parser.add_argument("--describe",type=str)
parser.add_argument("--count",type=int) # describe
parser.add_argument("--lang",type=str,choices=[i for i in languages.values()]) # describe, analyze, models, ocr, tag
parser.add_argument("--exclude",type=str,choices=[i for i in models.values()]) # describe, analyze
# ------------------------------------
parser.add_argument("--detect",type=str)
# ------------------------------------
parser.add_argument("--models",type=str)
parser.add_argument("--use",type=str,choices=[i for i in models.values()]) # models
# ------------------------------------
parser.add_argument("--ocr",type=str)
parser.add_argument("--orient",type=str,choices=['True','False']) # ocr
# ------------------------------------
parser.add_argument("--tag",type=str)
# ------------------------------------
parser.add_argument("--thumbnail",type=str)
parser.add_argument("--width",type=int) # thumbnail
parser.add_argument("--height",type=int) # thumbnail
parser.add_argument("--crop",type=str,choices=["True","False"]) # thumbnail
parser.add_argument("--save",type=str) # thumbnail
# ------------------------------------
parser.add_argument("--aoi",type=str)


args = parser.parse_args()



def set_default():
	"""
	The function `set_default()` checks if the default language and default value are valid, and then
	prints the default configuration.
	"""
	defaults = str(args.setdefault).split(',')
	if defaults[0] not in languages.values():
		raise Exception('English - en\nSpanish - es\nJapanese - ja\nPortuguese - pt\nSimplified Chinese - zh')
	if defaults[3] not in ['0','1']:
		raise Exception('Only 0 or 1 allowed')
	print(config.get('defaults'))



def analyze_func_url(passed_url,language=config.get('defaults')[0].get('language'),descExclude=config.get('defaults')[0].get('descriptionExclude[0]'),visualFeatures=config.get('defaults')[0].get('visualFeatures[0]'),details=config.get('defaults')[0].get('details[0]')):
	"""
	The function `analyze_func_url` takes a URL as input and makes a POST request to an API to analyze
	the image at the given URL, using specified parameters for language, description exclusion, visual
	features, and details.
	
	:param passed_url: The URL of the image that you want to analyze
	
	:param language: The language parameter specifies the language of the text in the image. It is set
	to the default language specified in the config file
	
	:param descExclude: The `descExclude` parameter is used to exclude certain types of descriptions
	from the analysis. In this code, it is set to the value
	`config.get('defaults')[0].get('descriptionExclude[0]')`, which means it will use the default value
	specified in the configuration file
	
	:param visualFeatures: The `visualFeatures` parameter is used to specify the types of visual
	features to be analyzed in the image. It can have values like "Categories", "Tags", "Description",
	"Faces", "ImageType", "Color", "Adult", "Objects", etc. These features provide information about the

	:param details: The "details" parameter specifies the level of detail in the analysis results. It
	can be set to "Celebrities" or "Landmarks" to include information about celebrities or landmarks in
	the image, respectively. If set to None or any other value, the analysis results will not include
	information about celebrities
	
	:return: the result of a POST request made to the API endpoint specified by the `desc_url` variable.
	The request payload is specified by the `desc_payload` variable, and the query parameters are
	specified by the `describe_qs` variable.
	"""

	describe_qs = gen_querystring(func='analyze')
	describe_qs = eval(str(describe_qs)%(language,descExclude,visualFeatures,details))

	if describe_qs.get("descriptionExclude[0]") != 'Celebrites' or describe_qs.get("descriptionExclude[0]") != 'Landmarks' or describe_qs.get("descriptionExclude[0]") == None:
		describe_qs.pop('descriptionExclude[0]')
	else:
		pass

	if describe_qs.get("visualFeatures[0]") not in config.get('visualFeatures').values() or describe_qs.get("visualFeatures[0]") == None:
		describe_qs.pop('visualFeatures[0]')
	else:
		pass

	if describe_qs.get("details[0]") != 'Celebrites' or describe_qs.get("details[0]") != 'Landmarks' or describe_qs.get("details[0]") == None:
		describe_qs.pop('details[0]')
	else:
		pass


	desc_url = url.format('analyze') # API url to be called
	desc_payload = eval(str(payload)%(passed_url)) # has the image url

	return make_post_request(api_url=desc_url,payload_dict=desc_payload,qs=describe_qs)



def describe_func_url(passed_url,language=config.get('defaults')[0].get('language'),count=config.get('defaults')[0].get('maxCandidates'),descExclude=config.get('defaults')[0].get('descriptionExclude[0]')):
	"""
	The function `describe_func_url` takes a URL, language, count, and description exclude as
	parameters, generates a query string, and makes a POST request to an API endpoint.
	
	:param passed_url: The URL of the image that you want to describe

	:param language: The language parameter specifies the language in which the description should be
	generated. It is set to the value obtained from the 'defaults' configuration, specifically the
	'language' field
	
	:param count: The `count` parameter specifies the maximum number of candidates to be returned in the
	response. It is set to the value specified in the `maxCandidates` field of the `defaults`
	configuration
	
	:param descExclude: The `descExclude` parameter is used to exclude certain types of descriptions
	from the result. In this code, it is set to the value
	`config.get('defaults')[0].get('descriptionExclude[0]')`, which means it will use the first value
	from the `descriptionExclude` list
	
	:return: the result of a POST request made to the API endpoint specified by `desc_url`. The request
	is made with the payload `desc_payload` and query parameters `describe_qs`.
	"""

	describe_qs = gen_querystring(func='describe')
	describe_qs = eval(str(describe_qs)%(language,count,descExclude))

	if describe_qs.get("descriptionExclude[0]") != 'Celebrites' or describe_qs.get("descriptionExclude[0]") != 'Landmarks' or describe_qs.get("descriptionExclude[0]") == None:
		describe_qs.pop('descriptionExclude[0]')
	else:
		pass

	if describe_qs.get("maxCandidates") == '1':
		describe_qs.pop('maxCandidates')
	else:
		pass

	desc_url = url.format('describe') # API url to be called
	desc_payload = eval(str(payload)%(passed_url)) # has the image url

	return make_post_request(api_url=desc_url,payload_dict=desc_payload,qs=describe_qs)

def detect_func_url(passed_url):
	"""
	The function `detect_func_url` takes a URL as input, generates a query string, constructs an API
	URL, creates a payload with the passed URL, and makes a POST request to the API URL with the payload
	and query string.
	
	:param passed_url: The URL of the image that you want to detect

	:return: the result of a POST request made to the API URL with the payload and query string
	provided.
	"""

	detect_qs = gen_querystring(func='detect')

	detect_url = url.format('detect') # API url to be called
	detect_payload = eval(str(payload)%(passed_url)) # has the image url

	return make_post_request(api_url=detect_url,payload_dict=detect_payload,qs=detect_qs)

def models_func_url(passed_url,model_used,language=config.get('defaults')[0].get('language')):
	"""
	The function `models_func_url` takes a URL, a model name, and an optional language parameter, and
	makes a POST request to the API endpoint for analyzing the image using the specified model.
	
	:param passed_url: The URL of the image that you want to analyze using the model

	:param model_used: The model ID or name that you want to use for analysis. This is used to specify
	which model should be used for the analysis
	
	:param language: The language parameter is the language code used for the analysis. It is obtained
	from the configuration file, specifically from the 'defaults' section
	
	:return: the result of a POST request made to the API endpoint specified by the `models_url`
	variable. The request is made with the `models_payload` as the payload and the `models_qs` as the
	query string.
	"""

	models_qs = gen_querystring(func='models')
	models_qs = eval(str(models_qs)%(language))

	models_url = url.format('models')+'{}/analyze'.format(model_used) # API url to be called
	models_payload = eval(str(payload)%(passed_url)) # has the image url

	return make_post_request(api_url=models_url,payload_dict=models_payload,qs=models_qs)

def ocr_func_url(passed_url,language=config.get('defaults')[0].get('language'),orientation=config.get('defaults')[0].get('detectOrientation')):
	"""
	The function `ocr_func_url` takes a URL of an image, along with optional parameters for language and
	orientation, and makes a POST request to an OCR API to extract text from the image.
	
	:param passed_url: The URL of the image that you want to perform OCR (Optical Character Recognition)
	on

	:param language: The language parameter is used to specify the language of the text in the image. It
	determines the OCR engine to be used for processing the image. The default value is obtained from
	the config file
	
	:param orientation: The orientation parameter determines whether the API should automatically detect
	the orientation of the image or not. If set to "true", the API will attempt to detect the
	orientation. If set to "false", the API will not attempt to detect the orientation and will assume
	the image is in the correct orientation
	
	:return: the result of a POST request made to an OCR API.
	"""

	ocr_qs = gen_querystring(func='ocr')
	ocr_qs = eval(str(ocr_qs)%(orientation,language))

	ocr_url = url.format('ocr') # API url to be called
	ocr_payload = eval(str(payload)%(passed_url)) # has the image url

	return make_post_request(api_url=ocr_url,payload_dict=ocr_payload,qs=ocr_qs)

def tag_func_url(passed_url,language=config.get('defaults')[0].get('language')):
	"""
	The function `tag_func_url` takes a URL and an optional language parameter, generates a query
	string, constructs a tag URL, creates a payload dictionary with the passed URL, and makes a POST
	request to the tag URL with the payload and query string.
	
	:param passed_url: The `passed_url` parameter is the URL of the image that you want to tag. It is
	the input to the function and is used to generate the payload for the API request

	:param language: The `language` parameter is the language code that specifies the language of the
	content in the image. It is optional and if not provided, it will use the default language specified
	in the configuration file
	
	:return: the result of a POST request made to the API URL with the payload and query string
	parameters.
	"""

	tag_qs = gen_querystring(func='tag')
	tag_qs = eval(str(tag_qs)%(language))

	tag_url = url.format('tag') # API url to be called
	tag_payload = eval(str(payload)%(passed_url)) # has the image url

	return make_post_request(api_url=tag_url,payload_dict=tag_payload,qs=tag_qs)

def thumbnail_func_url(passed_url,width=config.get('defaults')[0].get('width'),height=config.get('defaults')[0].get('height'),crop=config.get('defaults')[0].get('smartCropping'),save=config.get('defaults')[0].get('save'.format(cur_timestamp()))):
	"""
	The function `thumbnail_func_url` generates a thumbnail image from a given URL and saves it to a
	specified location.
	
	:param passed_url: The URL of the image that you want to generate a thumbnail for
	
	:param width: The width of the thumbnail image. It is set to the default width value from the config
	file if not provided
	
	:param height: The height parameter specifies the desired height of the thumbnail image
	
	:param crop: The "crop" parameter determines whether smart cropping should be applied to the
	thumbnail. If set to "True", smart cropping will be applied. If set to "False" or not provided,
	smart cropping will not be applied
	
	:param save: The `save` parameter is used to specify the file path where the generated thumbnail
	image will be saved

	:return: a boolean value, specifically `True`.
	"""

	thumbnail_qs = gen_querystring(func='generateThumbnail')
	thumbnail_qs = eval(str(thumbnail_qs)%(width,height,crop))

	if thumbnail_qs.get("smartCropping") == None or thumbnail_qs.get("smartCropping") == 'None':
		thumbnail_qs.pop('smartCropping')

	thumbnail_url = url.format('generateThumbnail') # API url to be called
	thumbnail_payload = eval(str(payload)%(passed_url)) # has the image url

	thumbnail_data = make_post_request(api_url=thumbnail_url,payload_dict=thumbnail_payload,qs=thumbnail_qs)

	with open(save,'wb') as f_in:
		f_in.write(thumbnail_data)
		f_in.flush()
		f_in.close()
	
	return True



def aoi_func_url(passed_url):
	"""
	The function `aoi_func_url` takes a URL as input, generates a query string, constructs an API URL,
	creates a payload with the passed URL, and makes a POST request with the API URL, payload, and query
	string.
	
	:param passed_url: The URL of the image that you want to pass to the API

	:return: the result of a POST request made to the API URL with the payload dictionary and query
	string.
	"""

	aoi_qs = gen_querystring(func='areaOfInterest')

	aoi_url = url.format('areaOfInterest') # API url to be called
	aoi_payload = eval(str(payload)%(passed_url)) # has the image url

	return make_post_request(api_url=aoi_url,payload_dict=aoi_payload,qs=aoi_qs)






if args.setdefault is not None:
	set_default()


"""
For `analyze` function of the API
"""
if args.analyze is not None:
	passed_url = args.analyze

	if args.lang is not None:
		lang_code = args.lang
	else:
		lang_code = config.get('defaults')[0].get('language')

	if args.exclude is not None:
		exclude = args.exclude
	else:
		exclude = config.get('defaults')[0].get('descriptionExclude[0]')

	if args.visual is not None:
		visual = args.visual
	else:
		visual = config.get('defaults')[0].get('visualFeatures[0]')

	if args.detail is not None:
		detail = args.detail
	else:
		detail = config.get('defaults')[0].get('details[0]')


	image_analysis = analyze_func_url(passed_url=passed_url,language=lang_code,descExclude=exclude,visualFeatures=visual,details=detail)


	if not config.get('auto'):
		print(json.dumps(image_analysis,indent=4))
	else:
		return_response(image_analysis)


"""
For `describe` function of the API
"""
if args.describe is not None:
	passed_url = args.describe

	if args.count is not None:
		max_response = count_value(args.count)
	else:
		max_response = config.get('defaults')[0].get('maxCandidates')

	if args.lang is not None:
		lang_code = args.lang
	else:
		lang_code = config.get('defaults')[0].get('language')

	if args.exclude is not None:
		exclude = args.exclude
	else:
		exclude = config.get('defaults')[0].get('descriptionExclude[0]')

	image_description = describe_func_url(passed_url=passed_url,language=lang_code,count=max_response,descExclude=exclude)

	if not config.get('auto'):
		print(json.dumps(image_description,indent=4))
	else:
		return_response(image_description)

"""
For `detect` function of the API
"""
if args.detect is not None:
	passed_url = args.detect

	object_detection = detect_func_url(passed_url=passed_url)

	if not config.get('auto'):
		print(json.dumps(object_detection,indent=4))
	else:
		return_response(object_detection)

"""
For `models` function of the API
"""
if args.models is not None:
	passed_url = args.models

	if args.lang is not None:
		lang_code = args.lang
	else:
		lang_code = config.get('defaults')[0].get('language')

	if args.use is not None:
		use_model = args.use
	else:
		print('Specify the model to use. Available models are')
		for i in [i for i in models.values()]:print('.'+i)
		Exit()
		# if not config.get('auto'):
		# 	print('Specify the model to use. Available models are',models.values())
		# else:
		# 	pass

	model_analysis = models_func_url(passed_url=passed_url,language=lang_code,model_used=use_model)

	if not config.get('auto'):
		print(json.dumps(model_analysis,indent=4))
	else:
		return_response(model_analysis)

"""
For `ocr`(optical character recognition) function of the API
"""
if args.ocr is not None:
	passed_url = args.ocr

	if args.lang is not None:
		lang_code = args.lang
	else:
		lang_code = config.get('defaults')[0].get('language')

	if args.orient is not None:
		detect_orient = args.orient
	else:
		detect_orient = config.get('defaults')[0].get('detectOrientation')

	ocr_response = ocr_func_url(passed_url,language=lang_code,orientation=detect_orient)

	if not config.get('auto'):
		print(json.dumps(ocr_response,indent=4))
	else:
		return_response(ocr_response)

"""
For `tag` function of the API
"""
if args.tag is not None:
	passed_url = args.tag

	if args.lang is not None:
		lang_code = args.lang
	else:
		lang_code = config.get('defaults')[0].get('language')

	tag_response = tag_func_url(passed_url,language=lang_code)

	if not config.get('auto'):
		print(json.dumps(tag_response,indent=4))
	else:
		return_response(tag_response)

"""
For `generateThumbnail` function of the API
"""
if args.thumbnail is not None:
	passed_url = args.thumbnail

	if args.height is not None:
		height = args.height
	else:
		height = config.get('defaults')[0].get('height')

	if args.width is not None:
		width = args.width
	else:
		width = config.get('defaults')[0].get('width')

	if args.crop is not None:
		crop = args.crop
	else:
		crop = config.get('defaults')[0].get('smartCropping')

	if args.save is not None:
		save = args.save
	else:
		save = config.get('defaults')[0].get('save'.format(cur_timestamp()))


	generate_thumbnail_response = thumbnail_func_url(passed_url=passed_url,width=width,height=height,crop=crop,save=save)

	if not config.get('auto'):
		print(json.dumps(generate_thumbnail_response,indent=4))
	else:
		return_response(generate_thumbnail_response)

"""
For `aoi`(area of interest) function of the API
"""
if args.aoi is not None:
	passed_url = args.aoi

	aoi_response = aoi_func_url(passed_url=passed_url)

	if not config.get('auto'):
		print(json.dumps(aoi_response,indent=4))
	else:
		return_response(aoi_response)
