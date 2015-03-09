#!/usr/bin/python

import webapp
import urllib
import string

class otroServidor(webapp.webApp):

    def parse(self, request):
    
        try:
            rec = request.split()[1][1:]
            self.cab1 = request.split("HTTP/1.1")[1][1:]
        except IndexError:
            rec = None
        return rec
        
    def process(self, parsedRequest):
    
        headers = "Conecction: keep-alive\nContent-Language: es\n"
        if parsedRequest == None:
            resp = "Solicitud erronea"
            code = "404 Not Found"
        elif len(parsedRequest.split('/')) == 1:
            code = "200 OK"
            url_orig = "http://" + parsedRequest
            f = urllib.urlopen(url_orig)
            content = f.read()
            index = string.find(content, "<body ")
            index = string.find(content, ">", index)
            original = "\n<a href='" + url_orig + "'>Original</a>\n"
            url_ref = "http://localhost:1234/" + parsedRequest
            refresh = "<a href='" + url_ref + "'>Recargar</a>\n"
            url_cache = "http://localhost:1234/cache/" + parsedRequest
            cache = "<a href='" + url_cache + "'>Cache</a>\n"
            url_cab1 = "http://localhost:1234/cab1/" + parsedRequest
            cab1 = "<a href='" + url_cab1 + "'>Cab1</a>\n"
            url_cab2 = "http://localhost:1234/cab2/" + parsedRequest
            cab2 = "<a href='" + url_cab2 + "'>Cab2</a>\n"
            url_cab3 = "http://localhost:1234/cab3/" + parsedRequest
            cab3 = "<a href='" + url_cab3 + "'>Cab3</a>\n"            
            url_cab4 = "http://localhost:1234/cab4/" + parsedRequest
            cab4 = "<a href='" + url_cab4 + "'>Cab4</a>\n"
            resp = content[:index+1] + original + refresh + cache + cab1 + cab2
            resp = resp + cab3 + cab4 + content[index+1:]
            cache_dicc[parsedRequest] = resp
            cab1_dicc[parsedRequest] = self.cab1
            cab2_dicc[parsedRequest] = self.cab1 #considero que manda las mismas
            cab3_dicc[parsedRequest] = str(f.info())
            cab4_dicc[parsedRequest] = headers
        else:
            try:
                if parsedRequest.split('/')[0] == "cache":
                    resp = cache_dicc[parsedRequest.split('/')[1]]
                    code = "200 OK"
                elif parsedRequest.split('/')[0] == "cab1":
                    resp = cab1_dicc[parsedRequest.split('/')[1]]
                    code = "200 OK"
                elif parsedRequest.split('/')[0] == "cab2":
                    resp = cab2_dicc[parsedRequest.split('/')[1]]
                    code = "200 OK"
                elif parsedRequest.split('/')[0] == "cab3":
                    resp = cab3_dicc[parsedRequest.split('/')[1]]
                    code = "200 OK"
                elif parsedRequest.split('/')[0] == "cab4":
                    resp = cab4_dicc[parsedRequest.split('/')[1]]
                    code = "200 OK"
            except KeyError:
                resp = "Esta pagina todavia no tiene datos almacenados"
                code = "404 Not Found"

        return (code, headers + "\r\n" + resp)
        

if __name__ == "__main__":
    cache_dicc = {}
    cab1_dicc = {}
    cab2_dicc = {}
    cab3_dicc = {}
    cab4_dicc = {}
    serv = otroServidor("localhost", 1234)

