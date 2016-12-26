# -*- coding: utf-8 -*-
# try something like
def transaction_list():
    data = SQLFORM(db.trns)

    if data.process().accepted:
        response.flash = "inserted"
    return dict(data=data)
