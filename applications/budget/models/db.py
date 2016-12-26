from gluon.tools import Auth

db = DAL("sqlite://storage.sqlite")

db.define_table("trns",
                Field("name", "string"),
                Field("date", "date"),
                Field("amount","double"),
                format="%(name)s")
db.define_table("repetitivetrns",
                Field("name", "string"),
                Field("rrule", "string"),
                Field("amount","double"),
                format="%(name)s")
