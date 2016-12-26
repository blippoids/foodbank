# -*- coding: utf-8 -*-
# try something like
def list_transactions():
    ab = db(db.tt.id==db.td.tt_id).select(db.td.bleh, db.tt.name)
    return dict(data=ab)
