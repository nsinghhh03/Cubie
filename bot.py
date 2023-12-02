import random
from spellchecker import SpellChecker
import pymssql 
import pandas as pd


pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.expand_frame_repr', False)  # Do not wrap the output to multiple lines

server = '208.109.11.78'
database = 'TCube360DevDB'
username = 'sa'
password = 'svslpld@123'

help_statements = [
    'help',
    'assist',
    'assistance',
    'can you help',
    'need help',
    'I need assistance with',
    'Help me with',
    'Can you provide information on',
    'I need your help'
]

help_response = "Sure, I'd be happy to help! Please provide more details about your inquiry."


# Define a list of negative feedback statements
negative_feedback = [
    'you are worthless',
    'you are useless',
    'this is wrong',
    'you are stupid',
    'i am confused',
    'i hate you',
    'you are not good at this'
]

# Define a list of positive feedback statements
positive_feedback = [
    'you are awesome',
    'you are kind',
    'fantastic',
    'amazing',
    'thank you',
    'thanks',
    'terrific',
    'helpful'
]

About_TCube = [
    'What is TCube',
    'What can TCube do',
    'Why should I use TCube',
    "What is TCube's main website?",
    'What is Tcube',
    'What can Tcube do'
]

# Define the response for negative feedback
negative_response = "I'm sorry to hear that. Please rephrase your question or visit the Audit, Track, and/or Rate Cubes for more solutions."
positive_response = "No problem. I am glad I could help."
Tcube_responses = "TCube is a freight audit management application that uses AI solutions to digitize the supply chain. Sounds cool right? Check out tcube.ai for more information. You can also ask me a question about different tabs within this application."

jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
    "I used to be a baker, but I couldn't make enough dough.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why don't skeletons fight each other? They don't have the guts!",
]

hello = [
    "Hey",
    "hey",
    "heyyy",
    "what's up",
    "how you doing",
    "wassup",
    "yo",
    "what's good",
    "whats up"
    "hi",

]
hello_response = "Hello. How can I help you?"

def get_tracking_info(tracking_number):
    try:
        conn = pymssql.connect(server=server, user=username, password=password, database=database)
        # Execute SQL queries
        cursor = conn.cursor()
        query = "SELECT InvoiceNumber, TCubeTotalFreightCharges, TrackingStatus, ShipmentDate FROM ShipmentTracking WHERE TrackingNo = %s"
        cursor.execute(query, (tracking_number,))
        row = cursor.fetchone()
        cursor.close()
        # Close the connection when done
        conn.close()
        return row if row else None
    except pymssql.Error as e:
        print("Error while connecting to SQL Server:", e)
        return None
    
def get_dispute_status(dispute_id):
    try:
        conn = pymssql.connect(server=server, user=username, password=password, database=database)
        # Execute SQL queries
        cursor = conn.cursor()
        query = "SELECT DisputeStatus, TrackingNumber, InvoiceNumber, ShipmentID, DisputeAmount, DisputeCategory, CarrierCode FROM DisputeManagement WHERE DisputeID = %s"
        cursor.execute(query, (dispute_id,))
        row = cursor.fetchone()
        cursor.close()
        # Close the connection when done
        conn.close()
        return row if row else None
    except pymssql.Error as e:
        print("Error while connecting to SQL Server:", e)
        return None

def get_invoice_status(invoice_number):
    try:
        conn = pymssql.connect(server=server, user=username, password=password, database=database)
        # Execute SQL queries
        cursor = conn.cursor()
        query = "SELECT AuditStatus, TrackingNo, TCCarrierCode FROM ShipmentTracking WHERE InvoiceNumber = %s"
        cursor.execute(query, (invoice_number,))
        row = cursor.fetchone()
        cursor.close()
        # Close the connection when done
        conn.close()
        return row if row else None
    except pymssql.Error as e:
        print("Error while connecting to SQL Server:", e)
        return None
    

def process_input(user_input):
    spell = SpellChecker() # Makes it so that the chatbot accepts human spelling errors
    misspelled = spell.unknown(user_input.split())
    for word in misspelled: 
        corrected_word = spell.correction(word)
        if corrected_word is not None:  # Check if the corrected word is not None
            user_input = user_input.replace(word, corrected_word)

    user_input = user_input.lower()
    dispute_definitions = {
        'rate issue': 'Rate Issue: Refers to disputes related to discrepancies in the rates charged for a particular service or carrier. If you believe that you have been overcharged or that the rates applied to your shipment are incorrect, you can raise a dispute under this category.',
        'duplicate': 'Duplicate: Refers to disputes involving duplicate charges or duplicate entries in the billing or invoicing process. If you have identified duplicate charges or entries in your invoice, you can raise a dispute under this category.',
        'cost calculation': 'Cost Calculation: Refers to disputes related to the calculation of costs associated with a shipment or service. If you have concerns or discrepancies regarding the cost calculation for a particular shipment, you can raise a dispute under this category.',
        'carrier data': 'Carrier Data: Refers to disputes related to discrepancies or issues with the data provided by the carrier. If you have identified incorrect or incomplete data provided by the carrier, you can raise a dispute under this category.',
        'mismatch': 'Mismatch: Refers to disputes involving mismatches or discrepancies between the documented information and the actual shipment or service details. If you have identified discrepancies or inconsistencies between the documented information and the actual shipment or service, you can raise a dispute under this category.',
        'fuel surcharge': 'Fuel Surcharge: Refers to disputes related to the application or calculation of fuel surcharges for a shipment or service. If you have concerns or discrepancies regarding the fuel surcharge applied to your shipment, you can raise a dispute under this category.'
    }
    
    for feedback in negative_feedback:
        if feedback in user_input:
            return negative_response
    for feedback in positive_feedback:
        if feedback in user_input:
            return positive_response
    for feedback in About_TCube:
        if feedback in user_input:
            return Tcube_responses
    if 'joke' in user_input:
        return random.choice(jokes)
    for feedback in hello:
        if feedback in user_input:
            return hello_response
    for help_statement in help_statements:
        if help_statement in user_input:
            return help_response
    for keyword, definition in dispute_definitions.items():
        if keyword in user_input:
            return "The Dispute Dashboard under Audit Cube may be able to help you. Here is what the dispute category means:\n\n" + definition




    if 'tracking number' in user_input:
        tracking_number = user_input.split()[-1]  # assuming tracking number is the last word in the input
        tracking_info = get_tracking_info(tracking_number)
        if tracking_info:
            invoice_number, total_freight_charges, tracking_status, shipment_date = tracking_info
            response = f"Here is the information for Tracking Number {tracking_number}:\n"
            response += f"Invoice Number: {invoice_number}\n"
            response += f"Total Freight Charges: {total_freight_charges}\n"
            response += f"Tracking Status: {tracking_status}\n"
            response += f"Shipment Date: {shipment_date}\n"
            return response
        else:
            return f"I could not find any information for Tracking Number {tracking_number}. Please check if it is correct or visit the <a href='http://tcube360.sveltoz.com/#/track-tool'>Track Tool</a> under Track Cube and manually input the number."
    
    if 'dispute status' in user_input:
        return "Sure, please type 'Dispute Id' followed by the dispute ID number so I can correctly access the data."

    if 'dispute id' in user_input:
        #dispute_id = user_input.split()[-1]  # assuming dispute ID is the last word in the input
        dispute_info = get_dispute_status(dispute_id)
        if dispute_info:
            dispute_status, tracking_id, invoice_number, shipment_id, dispute_amount, dispute_category, carrier_code = dispute_info
            response = f"- Here is the information for Dispute ID: {dispute_id}:\n"
            response += f" - Dispute Status: {dispute_status}\n"
            response += f" - Tracking ID: {tracking_id}\n"
            response += f" - Invoice Number: {invoice_number}\n"
            response += f" - Shipment ID: {shipment_id}\n"
            response += f" - Dispute Amount: {dispute_amount}\n"
            response += f" - Carrier: {carrier_code}\n"

            if dispute_category:
                response += f" - Dispute Category: {dispute_category}\n"
            response += f"\nDon't see all the information you were looking for? Visit the <a href='http://tcube360.sveltoz.com/#/dispute-management'>Dispute Management Dashboard</a> and use our search tool."

            return response
        else:
            return f"I could not find any information for Dispute ID {dispute_id}. Please check if it is correct or visit the DIspute Management Dashboard."
    
    if 'invoice status' in user_input:
        # Ask the user for the invoice number
        bot_response = "Sure, please provide me with the Invoice Number of the shipment:"
        return bot_response

    elif 'invoice number' in user_input:
        # Extract the invoice number from the user input
        invoice_number = user_input.split()[-1]

        # Call the get_invoice_status function to retrieve the relevant information
        invoice_status_info = get_invoice_status(invoice_number)
        
        if invoice_status_info:
            # Unpack the retrieved information
            audit_status, tracking_no, tc_carrier_code = invoice_status_info

            # Generate the response with the retrieved information
            bot_response = f"The InvoiceNumber: {invoice_number} has the following status:\n"
            bot_response += f"Audit Status: {audit_status}\n"
            bot_response += f"Tracking Number: {tracking_no}\n"
            bot_response += f"TC Carrier Code: {tc_carrier_code}\n"
            bot_response += f"If you require more information about this invoice or shipment, please self-search on the Audit Cube dashboards <a href='http://tcube360.sveltoz.com/#/freight-audit'>here</a> "
        else:
            bot_response = f"Sorry, I could not find any information for Invoice Number: {invoice_number}. Please use the search tool in the Invoice Dashboard under Audit Cube <a href='http://tcube360.sveltoz.com/#/invoice-details'>here</a."

        return bot_response
    elif any(word in user_input for word in ['rate cube', 'Rate cube page']):
        return 'Rate Cube allows you to simulate rates. You can enter the necessary information such as shipping address, destination, and weight of the package to get rates for a service and/or carrier. To reach Rate Cube, you can click the Rate Cube icon on the main page.'
    elif any(word in user_input for word in ['track cube', 'what is the track cube', 'how do i use track cube', 'navigate track cube', 'navigating track']):
        return 'Track Cube allows users to see package delivery status and Proof Of Delivery (POD). To reach the Track Cube, you can click on the Track Cube icon on the main page or click <a href="http://tcube360.sveltoz.com/#/tracking-details">here</a>..'
    elif any(word in user_input for word in ['upload file', 'upload shipment', 'upload invoice', 'how to upload', 'how do i upload', 'invoice upload', 'shipment upload', 'upload shipment file', 'upload invoice file', 'export data', 'view data']):
        return 'To upload your shipment and invoice files, you need to navigate to Audit Cube and choose the corresponding option for file upload. Shipment files should be in Microsoft Excel format whereas invoice files should be in CSV (Comma Separated Values) format. If you want to download all the data from your dashboard(s), you can click the "Export all data" button above the designated tables in Audit Cube.'
    elif any(word in user_input for word in ['get rate', 'calculate rates', 'rates', 'get rates']):
        return 'You can use the Rate Simulation tool under Rate cube to get rates for your package. Please proceed by clicking <a href="http://tcube360.sveltoz.com/#/track-tool">here</a>. Make sure to have precise shipment addresses and package details ready in order to simulate the most accurate calculation!'
    elif any(word in user_input for word in ['proof of delivery', "POD"]):
        return 'To see Proof of Delivery, please visit the Track Tool under Track Cube or click <a href="http://tcube360.sveltoz.com/#/carrier-master">here</a>. You can download the POD as a pdf in this tab as well!'
    elif any(word in user_input for word in ['dispute dashboard', 'invoice dashboard', 'shipment dashboard']):
        return 'To reach this dashboard, please click the Audit Cube on the main page and choose the desired dashboard or click <a href="http://tcube360.sveltoz.com/#/freight-audit">here</a>'
    elif any(word in user_input for word in ['status for my invoice', 'audit status', 'need to get status for invoice', 'status on invoice']):
        return "To get invoice status type you 'invoice number' followed by the actual number so that I can properly retrieve the information for you."
    elif any(word in user_input for word in ['tracking details page', 'tracking details']):
        return 'The tracking details page allows users to see a summary of their package delivery statuses, sorted by analysis period and carrier name.'
    elif any(word in user_input for word in ['admin cube', 'administration', 'administration cube', ' what is the admin']):
        return "The Administration cube allows users to see an overview of carriers, carrier services, and personal account information. You can reach the Administration Cube from the main page or by clicking <a href='http://tcube360.sveltoz.com/#/carrier-master'>here</a>."
    elif any(word in user_input for word in ['upload issue', 'upload failed', 'upload error', 'failed upload']):
        return 'If you are having troubles uploading shipment and/or invoice files, make sure you have the following: proper file formatting, proper column names, proper date format, and correct shipment and destination addresses. To further investigate, try putting random package details from your file into the Rate Simulation tool, which will confirm a valid entry. You can also verify carrier information in the Audit Cube <a href="http://tcube360.sveltoz.com/#/carrier-master">here</a> '
    elif any(word in user_input for word in ['okay', 'ok', 'oh']):
        return "What else would you like assistance with?"
    elif any(word in user_input for word in ['download shipment file', 'download invoice file', 'download file in audit cube', 'export data','see shipment file in exce', 'see invoice file in excel', 'download data']):
        return 'To export you uploaded files, please visit the Audit Cube. You can either export all data from the main dashboard, or go to the shipment, invoice, and/pr dispute dashboard to export specific data. Click the small paper icon above the table for download to start.' 
    elif any(word in user_input for word in ['Tcube', 'TCube', 'What is Tcube', 'What is TCube', 'What can Tcube do', 'What can TCube do']):
        return "TCube is a freight audit management application that uses AI solutions to digitize the supply chain. Sounds cool right? You can ask me a question about different tabs within this application."
    elif any(word in user_input for word in ['get shipment info', 'find invoice for', 'freight spend', 'locate pacakage',  'track package', 'track']):
        return "Please input 'tracking number *desired tracking number* for more details. Specifying that you are inputting a tracking number will allow me to effectively parse through your data. "
    elif any(word in user_input for word in ['change password', 'change permission', 'assign role', 'assign new role', 'change email id','change my password']):
        return "In order to make changes to your User Profile please visit Admin Cube or click <a href='http://tcube360.sveltoz.com/#/user-master'>here</a> "
    elif any(word in user_input for word in ['shipment staus', 'find an invoice', 'shipment costs', 'tracking']):
        return "In order to find an invoice for a tracking number, getting delivery status, and the total freight spend for a shipment, please type 'retrieve *your tracking number*'"
    elif any(word in user_input for word in ['nothing', "that's all", 'all set']):
        return "Okay. Please let me know if I can help you with anything else."
    elif any(word in user_input for word in ['hi', 'hello']):
        return "Hello! How can I help you today!?."
    elif any(word in user_input for word in ['bye', 'take care', 'leaving', 'goodbye']):
        return "Bye! Let me know if I can help with future inquiries"
    elif any(word in user_input for word in ["I can't find my tracking number", "I can't find tracking number", "I can't see tracking", "I can't find invoice"]):
        return "Hmm. The best solution is to use the search filter button in the Audit Cube Dashboards to find the shipment."
    elif any(word in user_input for word in ['still have an issue', "doesn't work",]):
        return "if you are having persistent issues, please manually visit the rate, audit,track, and/or admin cube(s) to get more information. There are a plethora of features available with a few clicks! If your problem still isn't solved, please contact support via our main website: www.tcube.ai"
    elif any(word in user_input for word in ["can't find"]):
        return "If you cannot locate that information, I advise you to check if your files were uploaded correctly. If neither the Audit Cube dashboard or Track tool have helped you, the information is not in our records."
    else:
        return "I'm sorry, I couldn't understand your request. Please provide more specific information or try rephrasing your question."
   

# Get a response from the chatbot
response = process_input('tcube is awesome!')
print(response)