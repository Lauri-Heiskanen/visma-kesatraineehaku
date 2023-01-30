class uri_parser:
    #set allowed uris and their requirements
    allowed_uris = {"visma-identity": {"login": {"source": str},
                                        "confirm": {"source": str, "paymentnumber": int}, 
                                        "sign": {"source": str, "documentid": str}}}    

    def parse_from_string(uri_string: str):
        # returns (path <str>, parameters <dict>)

        if type(uri_string) != str: # check a str was passed
            raise Exception("Expected str not {}".format(type(uri_string)))
        try: #incase uri is not in expected form
            splitted_uri = uri_string.split("://") #seperate scheme
            scheme = splitted_uri[0] #save scheme to appropriate var

            splitted_uri = splitted_uri[1].split("?") #seperate path
            path = splitted_uri[0] #save path to appropriate var

            parameters = {} #initialize parameters as a dict
            parameters_list = splitted_uri[1].split("&") #seperate parameters
            
            for parameter_string in parameters_list:
                parameters[parameter_string.split("=")[0]] = parameter_string.split("=")[1] #store parameters in dict
                key = parameter_string.split("=")[0]
        except IndexError:
            raise Exception("Unexpected URI form. Expected form: {scheme}://{path}?{key}={value}[&{key}={value}]")
            
        uri_parser.validate_scheme(scheme) #check if scheme is valid
        uri_parser.validate_path(scheme, path) #check if path is valid
        uri_parser.validate_parameters(scheme, path, parameters) #check if parameter keys are valid and fulfil required parameters

        required_parameters = uri_parser.allowed_uris[scheme][path] # get required parameters for easy access
        #at this point it is certain parameters keys match required keys
        for key in parameters: 
            if required_parameters[key] != type(parameters[key]): #check if parameters value-type doesn't matches required type
                try:
                    parameters[key] = required_parameters[key](parameters[key]) #change parameters value-type
                except:
                    raise Exception("Invalid parameter type: {}: {}".format(key, type(parameters[key]))) #raise exception if value-type cannot be converted

        return path, parameters

    def validate_scheme(scheme: str):
        if scheme in uri_parser.allowed_uris: #check if scheme is in allowed schemes
            return None #return if scheme is valid
        else:
            raise Exception("Invalid scheme") #raise exception if scheme is not valid
    
    def validate_path(scheme: str, path: str):
        if path in uri_parser.allowed_uris[scheme]: #check if path is in allowed paths
            return None #return if path is valid
        else:
            raise Exception("Invalid path") #raise exception if path is not valid

    def validate_parameters(scheme: str, path: str, parameters: dict):
        required_parameters = uri_parser.allowed_uris[scheme][path] # get required parameters for easy access

        for key in parameters:
            if key not in required_parameters: #check if parameter key is in requirements
                raise Exception("Invalid parameter {}".format(key)) #raise exception if unexpected parameter
        
        for key in required_parameters:
            if key not in parameters: #check all required parameters are present
                raise Exception("Missing parameter {}".format(key)) #raise exception if missing required parameter

        return None #return if parameters break no rules
