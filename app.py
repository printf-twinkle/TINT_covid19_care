from flask import Flask, redirect, render_template, url_for, request
import gspread
from numpy.core.numeric import ones_like
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pandas as pd
import json
from send_data import send_mail, send_post_to_group
from database import add_patient

app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]


# Assign credentials ann path of style sheet
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("automate covid19 care").sheet1
sheet_2 = client.open("automate covid19 care").worksheet("RTPCR")
sheet_3 = client.open("automate covid19 care").worksheet("food")
sheet_4 = client.open("automate covid19 care").worksheet("safehome")
sheet_5 = client.open("automate covid19 care").worksheet("telemedicines")
sheet_6 = client.open("automate covid19 care").worksheet("medicines")
sheet_7 = client.open("automate covid19 care").worksheet("hospitalbeds")
sheet_8 = client.open("automate covid19 care").worksheet("ambulance")

sheets_df = pd.DataFrame(sheet.get_all_records())
sheets_df2 = pd.DataFrame(sheet_2.get_all_records())
sheets_df3 = pd.DataFrame(sheet_3.get_all_records())
sheets_df4 = pd.DataFrame(sheet_4.get_all_records())
sheets_df5 = pd.DataFrame(sheet_5.get_all_records())
sheets_df6 = pd.DataFrame(sheet_6.get_all_records())
sheets_df7 = pd.DataFrame(sheet_7.get_all_records())
sheets_df8 = pd.DataFrame(sheet_8.get_all_records())


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/ambulances")
def ambulance():
    one_time_district = []
    a = sheet_8.get_all_records()
    for i in a:
        if i['District'] not in one_time_district:
            one_time_district.append(i['District'])
    return render_template("ambulance.html", one_time_district=one_time_district)


@app.route("/food")
def food():
    one_time_district = []
    a = sheet_3.get_all_records()
    for i in a:
        if i['District'] not in one_time_district:
            one_time_district.append(i['District'])
    return render_template("food.html", one_time_district=one_time_district)


@app.route("/hospitals")
def hospitals():
    one_time_district = []
    a = sheet_7.get_all_records()
    for i in a:
        if i['District'] not in one_time_district:
            one_time_district.append(i['District'])
    return render_template("hospital.html", one_time_district=one_time_district)


@app.route("/medicines")
def medicines():
    one_time_district = []
    a = sheet_6.get_all_records()
    for i in a:
        if i['District'] not in one_time_district:
            one_time_district.append(i['District'])
    return render_template("medicines.html", one_time_district=one_time_district)


@app.route("/rtpcr")
def rtpcr():
    one_time_district = []
    a = sheet_2.get_all_records()
    for i in a:
        if i['District'] not in one_time_district:
            one_time_district.append(i['District'])
    return render_template("rtpcr.html", one_time_district=one_time_district)


@app.route("/safehomes")
def safehomes():
    one_time_district = []
    a = sheet_4.get_all_records()
    for i in a:
        if i['District'] not in one_time_district:
            one_time_district.append(i['District'])
    return render_template("safehome.html", one_time_district=one_time_district)


@app.route("/telemedicine")
def telemedicine():
    one_time_district = []
    a = sheet_5.get_all_records()
    for i in a:
        one_time_district.append(i)
    return render_template("telemedicines.html", one_time_district=one_time_district)


@app.route("/oxygen")
def oxygen():
    one_time_district = []
    a = sheet.get_all_records()
    for i in a:
        if i['District'] not in one_time_district:
            one_time_district.append(i['District'])
    return render_template("oxygen.html", one_time_district=one_time_district)


@app.route("/oxygen/district/<did>")
def oxygen_per_district(did):
    all_rows = sheets_df
    if did == 'all':
        title = "Display All | TINT"
    else:
        all_rows = sheets_df.loc[(sheets_df['District'] == did)]
        title = "Oxygen"+did+" | TINT"
    length_of_rows = len(all_rows.index)
    return render_template("oxygen_display.html", title=title, data=all_rows, length=length_of_rows)


@app.route("/rtpcr/district/<did>")
def rtpcr_per_district(did):
    all_rows = sheets_df2
    if did == 'all':
        title = "Display All | TINT"
    else:
        all_rows = sheets_df2.loc[(sheets_df2['District'] == did)]
        title = "Rt-pcr"+did+" | TINT"
    length_of_rows = len(all_rows.index)
    return render_template("rtpcr_display.html", title=title, data=all_rows, length=length_of_rows)


@app.route("/safehome/district/<did>")
def safehome_per_district(did):
    all_rows = sheets_df4
    if did == 'all':
        title = "Display All | TINT"
    else:
        all_rows = sheets_df4.loc[(sheets_df4['District'] == did)]
        title = "SafeHome"+did+" | TINT"
    length_of_rows = len(all_rows.index)
    return render_template("safehome_display.html", title=title, data=all_rows, length=length_of_rows)


@app.route("/telemedicines/all")
def telemedicines_per_district():
    all_rows = sheets_df5
    title = "Display All | TINT"
    length_of_rows = len(all_rows.index)
    return render_template("telemedicines_display.html", title=title, data=all_rows, length=length_of_rows)


@app.route("/medicines/district/<did>")
def medicines_per_district(did):
    all_rows = sheets_df6
    if did == 'all':
        title = "Display All | TINT"
    else:
        all_rows = sheets_df6.loc[(sheets_df6['District'] == did)]
        title = "Medicines"+did+" | TINT"
    length_of_rows = len(all_rows.index)
    return render_template("medicines_display.html", title=title, data=all_rows, length=length_of_rows)


@app.route("/hospital/district/<did>")
def hospital_per_district(did):
    all_rows = sheets_df7
    if did == 'all':
        title = "Display All | TINT"
    else:
        all_rows = sheets_df7.loc[(sheets_df7['District'] == did)]
        title = "Hospital"+did+" | TINT"
    length_of_rows = len(all_rows.index)
    return render_template("hospitalbeds_display.html", title=title, data=all_rows, length=length_of_rows)


@app.route("/food/district/<did>")
def food_per_district(did):
    all_rows = sheets_df3
    if did == 'all':
        title = "Display All | TINT"
    else:
        all_rows = sheets_df3.loc[(sheets_df3['District'] == did)]
        title = "Food"+did+" | TINT"
    length_of_rows = len(all_rows.index)
    return render_template("food_display.html", title=title, data=all_rows, length=length_of_rows)


@app.route("/ambulance/district/<did>")
def ambulance_per_district(did):
    all_rows = sheets_df8
    if did == 'all':
        title = "Display All | TINT"
    else:
        all_rows = sheets_df8.loc[(sheets_df8['District'] == did)]
        title = "Ambulance"+did+" | TINT"
    length_of_rows = len(all_rows.index)
    return render_template("ambulance_display.html", title=title, data=all_rows, length=length_of_rows)


@app.route("/chatbotRelay", methods=["POST"])
def get_chatbot_data():
    chatbot_data = request.json
    print(chatbot_data)
    add_patient(chatbot_data)
    send_mail(chatbot_data)
    link = ""
    if(chatbot_data['social_amplify']):
        link = send_post_to_group(chatbot_data)
    return json.dumps({'success': True, "fb_post_link": link}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run(debug=True)
