# -*- coding: utf-8 -*-
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity

import os

import time
import datetime
import urllib
import json
import unirest
from random import shuffle, randint


class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and over

        if True:
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())

        user_keyword = messageProtocolEntity.getBody()        
        if user_keyword == "quote":
            response = ""
        elif user_keyword[0:2] == "tt":
            response = self.get_tt(user_keyword)
        elif "fullform" in user_keyword:
            response = self.get_fullform(user_keyword)
        elif "gtu" in user_keyword:
            response = self.get_gtu_info(user_keyword)
        elif "msg" in user_keyword:
            response = self.get_msg(user_keyword)
        elif "tollfree" in user_keyword:
            response = self.get_tollfree(user_keyword)
        elif "yt" in user_keyword.lower():
            response = self.yt(user_keyword)
        elif "chemist" in user_keyword:
            response = self.get_chemist(user_keyword)
        else:
            response = self.default()

        outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                response,
                to = messageProtocolEntity.getFrom())

        self.toLower(receipt)
        self.toLower(outgoingMessageProtocolEntity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery", entity.getFrom())
        self.toLower(ack)



# =================MY FUNCTIONS=================


# ----------------- Time table function -----------------        
    def get_tt(self, text):
        final = ""
        if len(text.split()) == 2:
            day = text.split()[1]
            if day == "monday":
                final = "Monday \n\nLectures\n============\nDS\nDBMS\nAEM\nEEM\n\nLab\n============\nE1 : DE\nE2 : DS\nE3 : DBMS"
            elif day == "tuesday":
                final = "Tuesday \n\nLab\n============\nE1 : Ds\nE2 : AEM\nE3 : DS\n\nLectures\n============\nDE\nDS\n\nLab\n============\nE1 : DBMSE\nE2 : DE\nE3 : DBMS"
            elif day == "wednesday":
                final = "Wednesday \n\nLectures\n============\nAEM\nDBMS\nDBMS\nDE\n\nLab\n============\nE1 : DS\nE2 : DBMS\nE3 : DE"
            elif day == "thursday":
                final = "Thursday \n\nLectures\n============\nDS\nDE\nAEM\nEEM\n\nLab\n============\nE1 : AEM\nE2 : DS\nE3 : DS"
            elif day == "friday":
                final = "Friday \n\nLectures\n============\nDE\nDS\nEEM\nDBMS\n\nLab\n============\nE1 : DBMS\nE2 : DBMS\nE3 : AEM"
            else:
                final == "Invalid day...."
        else:
            final = "Try this : tt monday"
            
        return str(final)

# ----------------- Fullform function -----------------
    def get_fullform(self, text):
        final = ""
        split = text.split()
        if len(split) == 1:
            final = "Please enter shortform."
        elif len(split) == 2:
            shortform = split[1]
            url = "https://api.import.io/store/data/243985c9-40aa-491e-9b0a-e3de4a7e32c5/_query?input/webpage/url=http%3A%2F%2Ffullforms.com%2F" + shortform + "&_user=5b5fd39b-293d-467a-96a3-ae991b8af88b&_apikey=5b5fd39b293d467a96a3ae991b8af88bf05390ea32dede72c808e95892bd1eff9549aed258aa36b1c0beca77e7d58f9efd66f8680ba152e7f7599f1e7056cd8f211ae67c876c4107da3a9e19a7b396ff"
            response = urllib.urlopen(url);
            data = json.loads(response.read())
            if len(data["results"]) == 0:
                final = "Not found!"
            else:
                if "Maybe you were" in data["results"][0]["mean"]:
                    final = "Not found!"
                else:
                    fullform = data["results"][0]["ff"]
                    mean = data["results"][0]["mean"]
                    final = "Shortform : " + shortform + "\n\nFullform : " + fullform + "\n\nMeaning : " + mean
        else:
            final = "NinjaBot can find only one full form at a time."
        return str(final.encode('ascii', 'ignore'))

# ----------------- Enrollment function -----------------
    def get_gtu_info(self, text):
        final = ""
        split = text.split()
        if len(split) == 2:
            enrollment_num = split[1]
            url = "https://api.import.io/store/data/1cd3f979-726a-4538-b4f5-e6402909989f/_query?input/webpage/url=http%3A%2F%2Fwww.gtuinfo.in%2FStudent-2013%2F" + enrollment_num + "%2Fabc&_user=5b5fd39b-293d-467a-96a3-ae991b8af88b&_apikey=5b5fd39b293d467a96a3ae991b8af88bf05390ea32dede72c808e95892bd1eff9549aed258aa36b1c0beca77e7d58f9efd66f8680ba152e7f7599f1e7056cd8f211ae67c876c4107da3a9e19a7b396ff"
            response = urllib.urlopen(url);
            data = json.loads(response.read())
            if len(data["results"]) == 0:
                final = "Invalid Enrollment Number!"
            else:
                name = data["results"][0]["data"][0]
                college = data["results"][0]["data"][1]
                branch = data["results"][0]["data"][2]
                admission_year = data["results"][0]["data"][4]
                cpi = data["results"][0]["data"][8]
                cgpa = data["results"][0]["data"][9]
                total_bl = data["results"][0]["data"][7]
                final = "Enrollment : " + enrollment_num + "\n\nName : " + name + "\n\nCollege : " + college + "\n\nBranch : " + branch + "\n\nYear of Admission : " + admission_year + "\n\nCPI : " + cpi + "\n\nCGPA : " + cgpa + "\n\nBacklogs : " + total_bl
        else:
            final = "Please enter enrollment number."
        return str(final)

# ----------------- Love function -----------------
    def get_msg(self, text):

        info = {
                    "love": [9,2318],
                    "friendship": [8,300],
                    "quote": [16,453],
                    "funny": [10,435],
                    "special": [19,66],
                    "story": [18,17]
                }
        cut = text.split()
        if len(cut) == 1:
            final = "Please provide sms type and try again!"
        elif len(cut) == 2:
            msg_type = cut[1].lower()
            if msg_type in info:
                page = randint(1,info[msg_type][1])
                url = "https://api.import.io/store/data/5fa01e9e-1cbc-4fe5-a4cc-9ea412e6e8f0/_query?input/webpage/url=http%3A%2F%2Fwww.dilsesms.com%2Fsmslist%2Flang%2FA%2Fcid%2F" + str(info[msg_type][0]) + "%2Fpage%2F" + str(page) + "&_user=5b5fd39b-293d-467a-96a3-ae991b8af88b&_apikey=5b5fd39b293d467a96a3ae991b8af88bf05390ea32dede72c808e95892bd1eff9549aed258aa36b1c0beca77e7d58f9efd66f8680ba152e7f7599f1e7056cd8f211ae67c876c4107da3a9e19a7b396ff"
                response = urllib.urlopen(url);
                data = json.loads(response.read())
                if len(data["results"]) == 0:
                    final = "Technical error!"
                else:
                    all_data = data["results"]
                    shuffle(all_data)
                    for i in range(0,6):
                        quote = all_data[i]["shayari"]
                        final = quote
            else:
                final = "Invalid sms type."
        else:
            final = "Please provide one sms type at a time."

        return str(final)

# ----------------- tollfree function -----------------
    def get_tollfree(self, text):
        final = 0
        fetched = []
        query = text[(text.find("ee")+3)::]
        data = ["Air India - 1800 22 7722","Go Air – 1800 223 001","Indian Airlines – 1800 180 1407","Indigo Airlines – 1800 180 3838","Jet Airways – 1800 22 5522","KingFisher – 1800 180 0101","SpiceJet – 1800 180 3333","Audi – 1800 103 6800","Bentley – 0008001006243","Ford – 1800 209 5556","Honda – 1800 1033121","Hyundai – 1800 11 4645","Mercedez Benz – 1800 102 9222","Mahindra Scorpio – 1800 22 6006","Maruti Suzuki – 1800 111 515","Mitsubishi – 1800-102 2955","Nissan – 1800-209-4080","Porsche – 1800 1020 911","Tata Motors – 1800 22 5552","Toyota – 1800 425 0001","Windshield Experts – 1800 113636","ABN AMRO 1800 11 2224","Axis Bank Ltd. – 1860 425 8888","Bank of Baroda – 1800 22 4447","Bank of India – 1800 22 00 88","Canara Bank – 1800 44 6000","Citibank – 1800 442265","Corporation Bank – 1800 443 555","Development Credit Bank – 1800 22 5769","HDFC Bank – 1800227 227","ICICI Bank – 1800 333 499","ICICI Bank NRI – 1800 22 4848","IDBI Bank – 1800 11 6999","Indian Bank – 1800 425 1400","Indian Overseas Bank – 1800 4251230","ING Vysya – 1800 44 9900","Kotak Mahindra Bank – 1800 22 6022","Lord Krishna Bank– 1800 11 2300","Oriental Bank of Commerce – 1800 180 1235","Punjab National Bank – 1800 122 222","State Bank of India 1800 44 1955","State Bank of Patiala – 1800 112 211","Syndicate Bank 1800 44 6655","Union Bank of India – 1800 22 2244","Apple – 1800 4250744","BenQ – 1800 22 08 08","Bird CellPhones – 1800 11 7700","Blackberry – 1800419 0121","HTC – 1800 113 377","LG – 1860 180 9999","Maxx – 1800 22 6299","Micromax – 1860 500 8286","Motorola MotoAssist – 180011 1211","Nokia – 3030 3838","Sony Ericsson – 3901 1111","Samsung – 1800 110 011","Tata Indicom – 1800 209 7070","Virgin – 1800 209 4444","Acer – 1800 3000 2237","Adrenalin – 1800 444 445","AMD – 1800 425 6664","Apple Computers – 1800 444 683","Canon – 1800 333 366","Cisco Systems – 1800 221 777","Compaq HP – 1800 444 999","Data One Broadband – 1800424 1800","Dell – 1800 444 026","Epson – 1800 44 0011","eSys – 3970 0011","Genesis Tally Academy – 1800 444 888","HCL – 1800 180 8080","HP – 1800 425 4999","IBM – 1800 443 333","Infosys – 1800 930 4048","FedEx – 1800 22 6161","Gati – 1800 180 4284","Goel Packers & Movers – 1800 11 3456","Om deo packers & Movers – 1800 2660 299","Royal Packers & Movers – 1800 11 4321","UPS – 1800 22 7171 ","ABT Courier – 1800 44 8585","AFL Wizz – 1800 22 9696","Agarwal Packers &Movers – 1800 11 4321","Associated Packers P Ltd – 1800 21 4560","DHL – 1800 111 345","DTDC – 1866 383 6606","First Flight – 1800 225 5345","Airtel Digital TV – 1800 102 8080","Tata Sky – 1800 180 6633","Sun Direct – 1800 200 7575","Reliance Big TV – 1800 200 9001","D2H – 1800 102 3111","Dish TV – 1800-180-3474","Barclaycard – 1800-233-7878","Bobcards – 1800-22-5110","HDFC Bank Credit Cards – 1800-345-4332","ICICI Credit Cards – 1800-11-2222","SBI Cards – 1800-180-1290","Tata Card – 1800-180-8282","VISA – 1800-425-444","Edu Plus – 1800 444 000","Hindustan College – 1800 33 4438","NCERT – 1800 11 1265","Vellore Institute of Technology – 1800 441 555","Amity University NCR Delhi – 1800 110 000","Best on Health – 1800 11 8899","Dr Batras – 1800 11 6767","GlaxoSmithKline – 1800 22 8797","Johnson & Johnson – 1800 22 8111","Kaya Skin Clinic – 1800 22 5292","LifeCell – 1800 44 5323","Manmar Technologies – 1800 33 4420","Pfizer – 1800 442 442","Roche Accu-Chek – 1800 11 45 46","Rudraksha – 180021 4708","Varilux Lenses – 1800 44 8383","VLCC – 1800 33 1262","Aiwa/Sony – 180011 1188","Anchor Switches – 1800 22 7979","Blue Star – 1800 22 2200","Bose Audio – 180011 2673","Bru Coffee Vending Machines – 1800 44 7171","Daikin Air Conditioners – 1800 444 222","DishTV – 1800 12 3474","Faber Chimneys – 1800 21 4595","Godrej – 1800 22 5511","Grundfos Pumps –1800 33 4555","LG – 1901 180 9999","Philips – 1800 22 4422","Samsung – 1800 113 444","Sanyo – 1800 11 0101","Voltas – 1800 33 4546","L&T – 1800 419 6666","Lexmark – 1800 22 4477","Marshal’s Point – 1800 33 4488","Microsoft – 1800 111 100","Microsoft Virus Update – 1901 333 334","Seagate – 1800 180 1104","Symantec – 1800 44 5533","TCS – 1800 200 1221","TVS Electronics – 1800 444 566","WeP Peripherals – 1800 44 6446","Wipro – 1800 333 312","xerox – 1800 180 1225","Zenith – 1800 222004",]
        for each in data:
            if query in each.lower():
                final = 1
                fetched.append(each)
        if final == 0:
            return str("Not found")
        else:
            final = ""
            for i in fetched:
                final = final + "\n" + i
            return str(final)

# ----------------- Youtube function -----------------
    def yt(self, text):
        final = ""
        cut = text.split()
        if len(cut) == 1:
            final = "Please provide URL of video."
        elif len(cut) == 2:
            URL = cut[1]
            if "http://" in URL or "https://" in URL:
                response = unirest.get("https://ytgrabber.p.mashape.com/app/get/" + URL[-11::],
                    headers={
                        "X-Mashape-Key": "V96M0xptiXmsh39L6Mw7CES0c7zgp1C7HOLjsnZGls6d3LiDjm",
                        "Accept": "application/json"
                    }
                )
                data = json.dumps(response.body, separators=(',',':'))
                data = (json.loads(data))["link"]
                # vid_title = (json.loads(data))["title"]
                # final = final + str(vid_title) + "\n=========\n\n"
                for each in data:
                    vid_format = each["type"]["format"]
                    vid_quality = each["type"]["quality"]
                    vid_url = each["url"]
                    bitly_url = "https://api-ssl.bitly.com/v3/shorten?longUrl=" + vid_url + "&domain=j.mp&format=json&access_token=b5d0505d7e46e410890e7046886c76df11d51f08"
                    bitly_response = urllib.urlopen(bitly_url);
                    bitly_data = json.loads(bitly_response.read())
                    if bitly_data["status_code"] == 200:
                        short_url = bitly_data["data"]["url"]
                        final = final + ">> Format : " + str(vid_format) + "\n>> Quality : " + str(vid_quality) + "\n>> " + str(short_url) + "\n\n"
            else:
                final = "Invalid URL."
        else:
            final = "Please provide only one URL at a time."
        return str(final)

# ----------------- Chemista function -----------------
    def get_chemist(self, text):
        final = ""
        split = text.split()
        if len(split) == 3:
            city = split[1]
            area = split[2]
            url = "https://api.import.io/store/data/aad88c0a-f44a-47b4-8103-dff743aa5a83/_query?input/webpage/url=http%3A%2F%2Fchemista.in%2Fassets%2Flib%2Fmain.php%3Fcity%3D" + city + "%26area%3D" + area + "&_user=5b5fd39b-293d-467a-96a3-ae991b8af88b&_apikey=5b5fd39b293d467a96a3ae991b8af88bf05390ea32dede72c808e95892bd1eff9549aed258aa36b1c0beca77e7d58f9efd66f8680ba152e7f7599f1e7056cd8f211ae67c876c4107da3a9e19a7b396ff"
            response = urllib.urlopen(url);
            data = json.loads(response.read())
            if len(data["results"]) == 0:
                final = "Invalid Enrollment Number!"
            else:
                all_data = data["results"]
                shuffle(all_data)

                for i in range(2):
                    name = all_data[i]["name"]
                    contact = all_data[i]["contact"]
                    address = all_data[i]["address"]
                    timings = all_data[i]["timings"]
                    final = final + "Name : " + name + "\nContact : " + contact + "\nAddress : " + address + "\nTimings : " + timings + "\n\n"
        else:
            final = "Please enter enrollment number."
        return str(final)

# ----------------- Default function ----------------- 
    def default(self):
        return str("Good to see !")




