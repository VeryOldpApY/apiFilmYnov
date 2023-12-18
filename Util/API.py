def returnAPIFormat(data, link, method, status=200, message=None):
	return {
		"_status": status,
		"_link": link,
		"_method": method,
		"data": data,
		"message": message
	}