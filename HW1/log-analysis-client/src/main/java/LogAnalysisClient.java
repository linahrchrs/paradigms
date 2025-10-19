
import javax.xml.namespace.QName;
import javax.xml.soap.*;
import javax.xml.ws.Service;
import javax.xml.ws.Dispatch;
import java.net.URL;

public class LogAnalysisClient {
    
    private static final String NAMESPACE = "http://loganalysis.example.com/";
    private static final String WSDL_URL = "http://localhost:7500/?wsdl";
    
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java LogAnalysisClient <command> <filename>");
            System.out.println("Commands: count, status");
            System.exit(1);
        }
        
        String command = args[0].toLowerCase();
        String filename = args[1];
        
        try {
            LogAnalysisClient client = new LogAnalysisClient();
            
            if (command.equals("count")) {
                client.countRequests(filename);
            } else if (command.equals("status")) {
                client.statusDistribution(filename);
            } else {
                System.out.println("Invalid command. Use 'count' or 'status'");
            }
            
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * Call countRequests operation
     */
    public void countRequests(String filename) throws Exception {
        // Create SOAP message
        MessageFactory messageFactory = MessageFactory.newInstance();
        SOAPMessage request = messageFactory.createMessage();
        SOAPPart soapPart = request.getSOAPPart();
        SOAPEnvelope envelope = soapPart.getEnvelope();
        SOAPBody body = envelope.getBody();
        
        // Build request
        QName qname = new QName(NAMESPACE, "countRequests");
        SOAPBodyElement bodyElement = body.addBodyElement(qname);
        SOAPElement filenameElement = bodyElement.addChildElement("filename");
        filenameElement.addTextNode(filename);
        
        request.saveChanges();
        
        // Send request and get response
        SOAPMessage response = sendSOAPMessage(request);
        
        // Parse response
        SOAPBody responseBody = response.getSOAPBody();
        
        if (responseBody.hasFault()) {
            SOAPFault fault = responseBody.getFault();
            System.out.println("Error: " + fault.getFaultString());
        } else {
            // Extract total count
            SOAPElement countResponse = (SOAPElement) responseBody.getChildElements(
                new QName(NAMESPACE, "countRequestsResponse")).next();
            SOAPElement totalElement = (SOAPElement) countResponse.getChildElements(
                new QName(NAMESPACE, "countRequestsResult")).next();
            String total = totalElement.getTextContent();
            
            System.out.println("Total requests: " + total);
        }
    }
    
    /**
     * Call statusDistribution operation
     */
    /**
 * Call statusDistribution operation
 */
    public void statusDistribution(String filename) throws Exception {
        // Create SOAP message
        MessageFactory messageFactory = MessageFactory.newInstance();
        SOAPMessage request = messageFactory.createMessage();
        SOAPPart soapPart = request.getSOAPPart();
        SOAPEnvelope envelope = soapPart.getEnvelope();
        SOAPBody body = envelope.getBody();
        
        // Build request
        QName qname = new QName(NAMESPACE, "statusDistribution");
        SOAPBodyElement bodyElement = body.addBodyElement(qname);
        SOAPElement filenameElement = bodyElement.addChildElement("filename");
        filenameElement.addTextNode(filename);
        
        request.saveChanges();
        
        // Send request and get response
        SOAPMessage response = sendSOAPMessage(request);
        
        // Parse response
        SOAPBody responseBody = response.getSOAPBody();
        
        if (responseBody.hasFault()) {
            SOAPFault fault = responseBody.getFault();
            System.out.println("Error: " + fault.getFaultString());
        } else {
            // Extract status entries - need to go one level deeper!
            SOAPElement statusResponse = (SOAPElement) responseBody.getChildElements(
                new QName(NAMESPACE, "statusDistributionResponse")).next();
            
            // Get the statusDistributionResult element (the container for the array)
            SOAPElement resultElement = (SOAPElement) statusResponse.getChildElements(
                new QName(NAMESPACE, "statusDistributionResult")).next();
            
            System.out.println("Status Code Distribution:");
            
            // Now get the StatusEntry elements from inside statusDistributionResult
            java.util.Iterator<?> entries = resultElement.getChildElements(
                new QName(NAMESPACE, "StatusEntry"));
            
            while (entries.hasNext()) {
                SOAPElement entry = (SOAPElement) entries.next();
                
                String statusCode = ((SOAPElement) entry.getChildElements(
                    new QName(NAMESPACE, "statusCode")).next()).getTextContent();
                String count = ((SOAPElement) entry.getChildElements(
                    new QName(NAMESPACE, "count")).next()).getTextContent();
                
                System.out.println("  " + statusCode + ": " + count + " occurrences");
            }
        }
    }
    /**
     * Helper method to send SOAP message
     */
    private SOAPMessage sendSOAPMessage(SOAPMessage request) throws Exception {
        SOAPConnectionFactory connectionFactory = SOAPConnectionFactory.newInstance();
        SOAPConnection connection = connectionFactory.createConnection();
        
        URL endpoint = new URL("http://localhost:7500/loganalysis");
        SOAPMessage response = connection.call(request, endpoint);
        
        connection.close();
        return response;
    }
}