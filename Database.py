import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://facial-recognition-b6693-default-rtdb.firebaseio.com/"})

ref =db.reference('People')

data={
    "023455":
        {
             "NAME":"NARENDRA MODI",
            "CONSTITUENCY":"MAVAL",
        },"012345":
        {
             "NAME":"TANUJ BALIVADA",
            "CONSTITUENCY":"MAVAL",
        },
        "123424":
        {
             "NAME":"OMKAR ABANG",
            "CONSTITUENCY":"MAVAL",


        },"123425":
        {
             "NAME":"MANSI PONDKULE",
            "CONSTITUENCY":"MAVAL",
        },
        "123451":
        {
             "NAME":"Ms.RUPALI ZAMBRE",
            "CONSTITUENCY":"MAVAL",


        },"123452":
        {
             "NAME":"Ms.TANVI GHODKE",
            "CONSTITUENCY":"MAVAL",
        },
        "123453":
        {
             "NAME":"Mr.SWAPNIL PURANIK",
            "CONSTITUENCY":"MAVAL",


        },"123454":
        {
             "NAME":"Ms.RENU DANDGE",
            "CONSTITUENCY":"MAVAL",
        },
        "123455":
        {
             "NAME":"Mr.RAHUL SONKAMBLE",
            "CONSTITUENCY":"MAVAL",


        },"123456":
        {
             "NAME":"Mr.CHANDAN PRASAD",
            "CONSTITUENCY":"MAVAL",
        },
        "123457":
        {
             "NAME":"Ms.SHITAL YEWALE",
            "CONSTITUENCY":"MAVAL",


        },"123458":
        {
             "NAME":"Mr.SHAILESH GAWAI",
            "CONSTITUENCY":"MAVAL",
        },
        "123459":
        {
             "NAME":"Ms.ASHWINI BIRADAR",
            "CONSTITUENCY":"MAVAL",


        },"123460":
        {
             "NAME":"Mr.SHRIKANT MAHINDRAKAR",
            "CONSTITUENCY":"MAVAL",
        },
        "123461":
        {
             "NAME":"Mr.SOMESH KALASKAR",
            "CONSTITUENCY":"MAVAL",


        },"123462":
        {
             "NAME":"Dr.SWATI SHIRKE",
            "CONSTITUENCY":"MAVAL",
        },
        "123463":
        {
             "NAME":"Dr.SAGAR PANDE",
            "CONSTITUENCY":"MAVAL",


        },"123464":
        {
             "NAME":"Mr.SOMINATH WAGH",
            "CONSTITUENCY":"MAVAL",
        },
        "123465":
        {
             "NAME":"Mr.SACHIN INGLE",
            "CONSTITUENCY":"MAVAL",


        },"123466":
        {
             "NAME":"Dr.R.G.BIRADAR",
            "CONSTITUENCY":"MAVAL",
        },
        "123467":
        {
             "NAME":"Dr.VIJAY PATIL",
            "CONSTITUENCY":"MAVAL",


        },"123468":
        {
             "NAME":"Dr.YUDHISHTHIR RAUT",
            "CONSTITUENCY":"MAVAL",
        }



}
for key,value in data.items():
    ref.child(key).set(value)
