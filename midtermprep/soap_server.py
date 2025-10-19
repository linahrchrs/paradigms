"""
SOAP Server for Log Analysis (Python)
Install: pip install spyne lxml
Run: python server_soap.py
"""

import os
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Array, ComplexModel, Fault
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import re

LOG_PATTERN = re.compile(r'"\S+ \S+ \S+" (\d{3})')

# Complex type for status entries
class StatusEntry(ComplexModel):
    statusCode = Unicode
    count = Integer


# Custom fault for file not found
class FileNotFoundFault(Fault):
    def __init__(self, filename):
        super(FileNotFoundFault, self).__init__(
            faultcode='Client',
            faultstring=f'File not found: {filename}'
        )


# Service implementation
class LogAnalysisService(ServiceBase):
    
    @rpc(Unicode, _returns=Integer, _faults=(FileNotFoundFault,))
    def countRequests(ctx, filename):
        """Count total number of requests in CLF log file"""
        if not os.path.exists(filename):
            raise FileNotFoundFault(filename)
        
        try:
            count = 0
            with open(filename, 'r') as f:
                for line in f:
                    if line.strip():
                        count += 1
            return count
        except Exception as e:
            raise FileNotFoundFault(filename)
    
    # @rpc(Unicode, _returns=Array(StatusEntry), _faults=(FileNotFoundFault,))
    # def statusDistribution(ctx, filename):
    #     """Get distribution of HTTP status codes"""
    #     if not os.path.exists(filename):
    #         raise FileNotFoundFault(filename)
        
    #     try:
    #         status_dict = {}
    #         with open(filename, 'r') as f:
    #             for line in f:
    #                 if line.strip():
    #                     parts = line.split()
    #                     if len(parts) >= 9:
    #                         status = parts[8]
    #                         status_dict[status] = status_dict.get(status, 0) + 1
            
    #         # Convert dictionary to array of StatusEntry objects
    #         result = []
    #         for status_code, count in status_dict.items():
    #             entry = StatusEntry()
    #             entry.statusCode = status_code
    #             entry.count = count
    #             result.append(entry)
            
    #         return result
    #     except Exception as e:
    #         raise FileNotFoundFault(filename)


    @rpc(Unicode, _returns=Array(StatusEntry), _faults=(FileNotFoundFault,))
    def statusDistribution(ctx, filename):
        """Get distribution of HTTP status codes"""
        if not os.path.exists(filename):
            raise FileNotFoundFault(filename)
        
        try:
            status_dict = {}
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.encode('ascii', 'ignore').decode()  # remove weird chars like Â
                    match = re.search(r'"[A-Z]+\s+\S+\s+HTTP/\d\.\d"\s*(\d{3})', line)
                    if match:
                        status = match.group(1)
                        print(f"Matched status: {status}")  # Debugging info
                        status_dict[status] = status_dict.get(status, 0) + 1
                    else:
                        print(f"No match for: {line.strip()}")  # Debugging info
            
            # Convert dictionary to array of StatusEntry objects
            result = []
            for status_code, count in status_dict.items():
                entry = StatusEntry()
                entry.statusCode = status_code
                entry.count = count
                result.append(entry)
            
            print(f"Returning {len(result)} entries")  # Debugging info
            return result
        except Exception as e:
            print(f"Error processing file: {e}")
            raise FileNotFoundFault(filename)



# Create SOAP application
application = Application(
    [LogAnalysisService],
    tns='http://loganalysis.example.com/',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    server = make_server('0.0.0.0', 7500, wsgi_application)
    print("SOAP Server running on http://localhost:7500")
    print("WSDL available at: http://localhost:7500/?wsdl")
    server.serve_forever()
