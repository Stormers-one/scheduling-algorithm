import flask
import pandas as pd
import numpy as np
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = False


def aggregate():
    df = pd.read_csv(
        'https://firebasestorage.googleapis.com/v0/b/odu-komban-ok.appspot.com/o/schedule_suggest%20files%2FDem%20-%20Sheet1.csv?alt=media&token=2eb2793f-ba84-414d-965f-a41f33ebf2c4'
    )
    df["From_loc"] = df["From_loc"]. str. lower()
    df["To_loc"] = df["To_loc"]. str. lower()
    b = pd.DataFrame(df.loc[:, "From_loc"] + " " + df.loc[:, "To_loc"] +
                     " " + df.loc[:, "timing"] + " " + df.loc[:, "date"])
    a = b.iloc[:, 0].unique()
    # print(a)
    dicti = {}
    for i in a:
        if i not in dicti:
            dicti[i] = 0
    # print(dicti)

    for i in range(len(b)):
        for j in a:
            if df['From_loc'][i] in j[0:len(df['From_loc'][i])] and df['To_loc'][i] in j and df['timing'][i] in j and df['date'][i] in j:
                dicti[j] += 1
    # print(dicti)

    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df["number_of_tickets"] = np.zeros(len(df))

    for i in range(len(df)):
        for j in dicti:
            if df['From_loc'][i] in j[0:len(df['From_loc'][i])] and df['To_loc'][i] in j and df['timing'][i] in j and df['date'][i] in j:
                df.at[i, "number_of_tickets"] = dicti[j]

    #df.to_csv('ticketcount.csv', index=False)

    # Capacity check
    #data = pd.read_csv('ticketcount.csv')
    buscount = pd.read_csv(
        'https://firebasestorage.googleapis.com/v0/b/odu-komban-ok.appspot.com/o/schedule_suggest%20files%2Fbuscount.csv?alt=media&token=198d4692-1a81-4e9b-b918-bd8fd147a1da')

    # Count of ticket and route to a dictionary
    fullcount = {}
    for i in range(len(df)):
        f = df['From_loc'][i]+" "+df['To_loc'][i]
        if f not in fullcount:
            fullcount[f] = df['number_of_tickets'][i]
        else:
            fullcount[f] += df['number_of_tickets'][i]
    # print(fullcount)

    # Dictionary with route name and capacity of passengers
    buscap = {}
    for i in fullcount:
        k = 0
        for j in buscount['Route']:
            k += 1
            if i == j:
                buscap[i] = buscount['Count'][k]*40
    # print(buscap)

    column_names = ["Route", "Exceed_Diminish", "Count_exceeded_diminished"]
    cap = pd.DataFrame(columns=column_names)

    k = 0
    for i in buscap:
        if buscap[i] < fullcount[i]:
            cap.at[k, 'Route'] = i
            cap.at[k, "Exceed_Diminish"] = 1
            cap.at[k, "Count_exceeded_diminished"] = fullcount[i]-buscap[i]
            k += 1
        else:
            if fullcount[i] < buscap[i]*0.2:
                cap.at[k, 'Route'] = i
                cap.at[k, "Exceed_Diminish"] = 0
                cap.at[k, "Count_exceeded_diminished"] = buscap[i]-fullcount[i]
                k += 1

    return cap


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/generate-suggest', methods=['GET'])
def api_function():
    res1 = aggregate()
    return res1.to_dict()


app.run()
